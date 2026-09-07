import random
import unittest
import subprocess
import sys
from unittest.mock import Mock, patch

from chess_engine import GameState
from chess_engine.bots import BaseBot, HardBot, ImpossibleBot


class ImpossibleBotTests(unittest.TestCase):
    def test_stalled_engine_times_out_and_uses_fallback(self):
        state = GameState()
        move = ((6, 4), (4, 4))
        for respond_to_handshake in (False, True):
            with self.subTest(handshake=respond_to_handshake):
                fallback = Mock()
                fallback.choose_move.return_value = move
                bot = ImpossibleBot(fallback=fallback, move_time_ms=1)
                bot.executable_path = sys.executable
                bot.RESPONSE_TIMEOUT_SECONDS = 0.05
                script = (
                    'import sys\n'
                    'for line in sys.stdin:\n'
                    + (' if line.strip() == "uci": print("uciok", flush=True)\n'
                       ' if line.strip() == "isready": print("readyok", flush=True)\n'
                       if respond_to_handshake else '')
                    + ' if line.strip() == "quit": break\n'
                )
                popen = subprocess.Popen
                processes = []
                def launch(args, **kwargs):
                    process = popen([sys.executable, '-u', '-c', script], **kwargs)
                    processes.append(process)
                    return process
                with patch('chess_engine.bots.impossible_bot.subprocess.Popen', side_effect=launch):
                    try:
                        self.assertEqual(bot.choose_move(state), move)
                        fallback.choose_move.assert_called_once_with(state)
                        self.assertIsNone(bot.process)
                        self.assertIsNotNone(processes[0].poll())
                    finally:
                        bot.close()

    def test_impossible_bot_uses_common_bot_interface(self):
        self.assertIsInstance(ImpossibleBot(), BaseBot)

    def test_starting_position_fen(self):
        state = GameState()

        self.assertEqual(
            ImpossibleBot.to_fen(state),
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR '
            'w KQkq - 0 1',
        )

    def test_uci_move_conversion(self):
        self.assertEqual(
            ImpossibleBot._uci_to_move('e7e5'),
            ((1, 4), (3, 4)),
        )

    def test_fen_tracks_turn_en_passant_and_move_number(self):
        state = GameState()
        state.move.handle_piece_move((6, 4), (4, 4))

        fields = ImpossibleBot.to_fen(state).split()

        self.assertEqual(fields[1], 'b')
        self.assertEqual(fields[3], 'e3')
        self.assertEqual(fields[5], '1')

    def test_missing_stockfish_uses_legal_fallback(self):
        state = GameState()
        fallback = HardBot(depth=1, rng=random.Random(7), choice_window=0)
        bot = ImpossibleBot(fallback=fallback)
        bot.executable_path = None

        self.assertIn(bot.choose_move(state), state.move.get_valid_moves())


if __name__ == '__main__':
    unittest.main()
