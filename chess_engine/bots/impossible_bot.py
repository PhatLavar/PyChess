import os
from pathlib import Path
import shutil
import subprocess
from queue import Empty, Queue
from threading import Thread
from time import monotonic

from chess_engine.bots.base import BaseBot
from chess_engine.bots.hard_bot import HardBot
from chess_engine.utilities import EMP


class ImpossibleBot(BaseBot):
    """Use Stockfish through UCI, with the strongest custom bot as fallback."""

    ENVIRONMENT_PATH = 'PYCHESS_STOCKFISH_PATH'
    DEFAULT_MOVE_TIME_MS = 500
    RESPONSE_TIMEOUT_SECONDS = 5

    def __init__(self, executable_path=None, move_time_ms=DEFAULT_MOVE_TIME_MS, fallback=None):
        self.executable_path = self._find_executable(executable_path)
        self.move_time_ms = max(1, move_time_ms)
        self.fallback = fallback or HardBot(depth=3, choice_window=0)
        self.process = None
        self.promotion_choice = 'Q'

    @property
    def stockfish_available(self):
        """Return whether a usable Stockfish executable was discovered."""
        return self.executable_path is not None

    def choose_move(self, game_state):
        """Return Stockfish's move, or a legal custom-engine fallback move."""
        self.promotion_choice = 'Q'
        valid_moves = game_state.move.get_valid_moves()
        if not valid_moves:
            return None

        if self.stockfish_available:
            try:
                move = self._choose_stockfish_move(game_state)
                if move in valid_moves:
                    return move
            except (OSError, RuntimeError, ValueError):
                self.close()

        return self.fallback.choose_move(game_state)

    def close(self):
        """Stop the persistent UCI process when one is running."""
        if self.process is None:
            return
        try:
            self._send('quit')
            self.process.wait(timeout=1)
        except (OSError, subprocess.TimeoutExpired):
            self.process.kill()
        finally:
            self.process.wait()
            self.process.stdin.close()
            self.process.stdout.close()
            self.process = None

    def _choose_stockfish_move(self, game_state):
        self._ensure_process()
        self._send(f'position fen {self.to_fen(game_state)}')
        self._send(f'go movetime {self.move_time_ms}')

        deadline = monotonic() + self.move_time_ms / 1000 + self.RESPONSE_TIMEOUT_SECONDS
        while True:
            line = self._read_line(deadline)
            if line == '':
                raise RuntimeError('Stockfish stopped before returning a move')
            if line.startswith('bestmove '):
                uci_move = line.split()[1]
                if uci_move == '(none)':
                    return None
                if len(uci_move) >= 5:
                    self.promotion_choice = uci_move[4].upper()
                return self._uci_to_move(uci_move)

    def _ensure_process(self):
        if self.process is not None and self.process.poll() is None:
            return

        creation_flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        self.process = subprocess.Popen(
            [str(self.executable_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            creationflags=creation_flags,
        )
        self._output = Queue()
        Thread(target=self._collect_output, args=(self.process.stdout, self._output),
               daemon=True).start()
        self._send('uci')
        self._read_until('uciok')
        self._send('setoption name Threads value 1')
        self._send('setoption name Hash value 64')
        self._send('isready')
        self._read_until('readyok')

    def _send(self, command):
        if self.process is None or self.process.stdin is None:
            raise RuntimeError('Stockfish is not running')
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()

    def _read_until(self, expected):
        deadline = monotonic() + self.RESPONSE_TIMEOUT_SECONDS
        while True:
            line = self._read_line(deadline)
            if line == '':
                raise RuntimeError(f'Stockfish stopped before {expected}')
            if line.strip() == expected:
                return

    @staticmethod
    def _collect_output(stream, output):
        try:
            for line in stream:
                output.put(line)
        finally:
            output.put('')

    def _read_line(self, deadline):
        remaining = deadline - monotonic()
        if remaining <= 0:
            raise RuntimeError('Stockfish response timed out')
        try:
            return self._output.get(timeout=remaining)
        except Empty as error:
            raise RuntimeError('Stockfish response timed out') from error

    def _find_executable(self, requested_path):
        candidates = [
            requested_path,
            os.environ.get(self.ENVIRONMENT_PATH),
            shutil.which('stockfish'),
            Path('stockfish') / 'stockfish.exe',
            Path('assets') / 'stockfish' / 'stockfish.exe'
        ]
        for candidate in candidates:
            if candidate and Path(candidate).is_file():
                return Path(candidate).resolve()
        return None

    @classmethod
    def to_fen(cls, game_state):
        """Convert the current PyChess state into a UCI-compatible FEN."""
        rows = []
        for board_row in game_state.board.board:
            empty_count = 0
            fen_row = ''
            for piece in board_row:
                if piece == EMP:
                    empty_count += 1
                    continue
                if empty_count:
                    fen_row += str(empty_count)
                    empty_count = 0
                symbol = piece[1]
                fen_row += symbol.upper() if piece[0] == 'w' else symbol.lower()
            if empty_count:
                fen_row += str(empty_count)
            rows.append(fen_row)

        active_color = 'w' if game_state.white_to_move else 'b'
        castling = cls._castling_fen(game_state)
        en_passant = cls._square_to_uci(game_state.en_passant_target)
        fullmove = len(game_state.move.notation) // 2 + 1
        halfmove = game_state.fifty_move_rule.halfmove_clock
        return f"{'/'.join(rows)} {active_color} {castling} {en_passant} {halfmove} {fullmove}"

    @staticmethod
    def _castling_fen(game_state):
        symbols = ''
        rights = game_state.castling_rights
        if rights['w']['king_side']:
            symbols += 'K'
        if rights['w']['queen_side']:
            symbols += 'Q'
        if rights['b']['king_side']:
            symbols += 'k'
        if rights['b']['queen_side']:
            symbols += 'q'
        return symbols or '-'

    @staticmethod
    def _square_to_uci(square):
        if square is None:
            return '-'
        row, col = square
        return f'{chr(ord("a") + col)}{8 - row}'

    @classmethod
    def _uci_to_move(cls, uci_move):
        if len(uci_move) < 4:
            raise ValueError(f'Invalid UCI move: {uci_move}')
        return cls._uci_to_square(uci_move[:2]), cls._uci_to_square(uci_move[2:4])

    @staticmethod
    def _uci_to_square(square):
        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])
        return row, col

    def __del__(self):
        self.close()
