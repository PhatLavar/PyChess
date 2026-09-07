# PyChess

PyChess is a local desktop chess game written in Python with pygame-ce. It combines a custom chess engine, a Pygame interface, five computer-player difficulties, and optional Stockfish support.

The project explores how to build a complete chess application: legal moves, special rules, reversible game state, computer search, responsive input, animated rendering, and readable match history. The code is separated into application, engine, and UI layers so each responsibility can be understood and changed independently.

## Current status

The current implementation is being prepared for a first 1.0.0 release. This README does not create or announce a version tag. The automated suite currently contains 58 tests; its coverage is described in the [tests guide](tests/README.md).

## Features

- **Three matchups:** Player–Player, Player–Bot, and Bot–Bot spectator mode.
- **Five difficulties:** Easy, Medium, Hard, Master, and Impossible.
- **Chess rules:** legal-move filtering, check, checkmate, stalemate, castling, en passant, and promotion to queen, rook, bishop, or knight.
- **Draw detection:** supported dead-material patterns, automatic threefold repetition, and an automatic fifty-move threshold.
- **Board interaction:** selected-piece, legal-move, capture, hover, and check highlights.
- **Animation and menus:** piece movement, promotion choices, endgame effects, rematches, and matchup changes after a finished game.
- **Undo:** one move in Player–Player and a player–bot round in Player–Bot; pending promotion can be cancelled.
- **Responsive bot turns:** searches run in background threads using independent position snapshots. Results from an undone or replaced position are discarded.
- **Optional Stockfish:** UCI integration, response timeouts, promotion selection, and built-in fallback.
- **Local match history:** chronological text logs grouped by matchup, with collision-safe filenames.

## Requirements and setup

Development and verification used **Python 3.13.6** and **pygame-ce 2.5.7** on Windows. Other Python versions and operating systems are not yet verified for this project.

From a terminal in the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe chess.py
```

These Windows commands use the environment's interpreter directly, so activating it is optional. If using another environment, install the requirements there and run:

```text
python chess.py
```

Keep the `assets/images/chess_pieces/` folder with the project. Piece images and bundled Stockfish paths resolve relative to the project, so launching the script by its full path from another directory is supported.

Stockfish is optional and its executable is excluded from Git. See the [Stockfish setup guide](assets/stockfish/README.md) to install it or configure an existing executable. Without a usable engine, Impossible mode falls back to the custom Hard bot.

## How to play

1. Choose **Player–Player**, **Player–Bot**, or **Bot–Bot** on the start screen.
2. For a bot matchup, choose a difficulty and select **Select Difficulty**.
3. Click one of the active player's pieces, then a highlighted destination.
4. When a pawn promotes, choose **Q**, **R**, **B**, or **N**.
5. After the game-ending effect, choose **Rematch** or **Change Gamemode**.

The board stays oriented with White at the bottom. In Player–Bot mode, the human plays White. Bot–Bot uses the chosen difficulty for both colors.

| Control | Behavior |
| --- | --- |
| Click a piece, then a destination | Request a legal move. |
| Click the selected piece again | Clear selection. |
| Z in Player–Player | Undo the last completed move. |
| Z in Player–Bot | Undo White's move if Black has not replied; otherwise undo both players' latest moves. |
| Z during pending promotion | Cancel the choice without undoing the opponent's previous move. |
| Close the window | End the application and save an unfinished match if at least one move remains applied. |

Undo is disabled in Bot–Bot and after game over. Input cannot move a piece during animation or the bot's turn.

## Bot behavior

| Difficulty | Approach |
| --- | --- |
| Easy | Immediate scoring for captures, development, central squares, and promotion, with randomness. |
| Medium | Two-ply alpha-beta search with material and development scoring. |
| Hard | Three-ply search plus more positional evaluation. |
| Master | Two-ply search with up to two additional quiescence levels, quiet check evasions, and strategic scoring. |
| Impossible | Stockfish when usable; otherwise a three-ply HardBot fallback. |

A ply is one player's move. Difficulty labels are not Elo ratings, and Master is not guaranteed to outperform Hard in every position. Medium and Hard can select near-best scores. Master and the fallback use zero score tolerance but can still break exact ties randomly. Built-in bots promote to queens; Stockfish can choose another piece.

The [bot guide](chess_engine/bots/README.md) explains implementation boundaries and the [Stockfish guide](assets/stockfish/README.md) explains discovery, timeouts, and fallback.

## Project map

Each maintained folder has its own README with its purpose, immediate files, and links to subfolders.

| Path | Purpose |
| --- | --- |
| [chess.py](chess.py) | Entry point: constructs ChessGame and runs it. |
| [requirements.txt](requirements.txt) | Pins the runtime dependency, pygame-ce. |
| [.gitignore](.gitignore) | Excludes local environments, caches, personal logs, and the Windows Stockfish executable while retaining documentation. |
| [chess_app/](chess_app/README.md) | Application lifecycle, event routing, input, bot coordination, and saving. |
| [chess_engine/](chess_engine/README.md) | Board models, move generation/execution, rules, history, and bots. |
| [chess_ui/](chess_ui/README.md) | Board rendering, highlights, animations, menus, and presentation settings. |
| [assets/](assets/README.md) | Required piece images and optional Stockfish installation. |
| [tests/](tests/README.md) | Automated behavior and regression tests. |
| [match_history/](match_history/README.md) | Locally generated logs and documentation of their format. |
| README.md | This project overview and starting guide. |

Generated folders such as `.venv/`, `__pycache__/`, and Git's internal `.git/` are not project modules and do not receive folder READMEs.

## How the pieces work together

```text
chess.py
  -> ChessGame (application lifecycle)
       -> EventHandler -> InputHandler -> GameState.move
       -> bot worker (position copy) -> result applied to live GameState
       -> GameRenderer -> highlights, animations, menus
       -> MatchHistory -> local text files
```

The engine owns rules and match state without importing Pygame. The application decides when moves, undo, saving, and background thinking happen. The UI draws the current state and returns menu or promotion choices.

Moves use zero-based `(row, column)` coordinates: `(0, 0)` is a8 and `(7, 7)` is h1. A piece code such as `wN` means a white knight, while `--` is empty. Legal moves contain origin and destination pairs; promotion choice is a separate step.

## Match history

Logs are written below:

```text
match_history/
  player-player/
  player-bot/
  bot-bot/
```

A filename such as `20260907-1224.txt` records the local completion time to the minute. A suffix such as `-2` avoids overwriting another file. Older files directly under `match_history/` may exist from earlier application layouts.

The format contains events such as `[MOVE]`, `[CAPTURE]`, `[CHECK]`, `[CASTLING]`, `[PROMOTION]`, `[UNDO]`, and `[ENDMATCH]`. Moves and later undo actions are retained chronologically. These logs are **not PGN** and cannot be loaded to resume a game.

Closing an unfinished match normally records `TERMINATED`. No file is saved when no completed moves remain applied. A forced process stop or crash may bypass the normal save path. Personal log files are ignored by Git; the folder guides are included.

## Verification

Run the automated suite from the project root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

To check Python compilation:

```powershell
.\.venv\Scripts\python.exe -m compileall -q chess.py chess_app chess_engine chess_ui
```

The suite covers bot selection and turn handling, draw rules, undo, history saving, menu actions, engine timeout fallback, exact root scoring, check evasions, and asset paths.

During the pre-release review, legal moves were also compared with Stockfish in 400 sampled positions and targeted special-move cases. Those comparisons were one-off checks, not part of the committed automated suite. Headless rendering checks do not replace an interactive playthrough.

## Known limitations

- Fixed 512×512 window and White-side orientation; no resizing or board flip.
- The human always plays White against a bot.
- No online multiplayer, chess clock, resignation/draw-offer UI, or in-game pause/settings screen.
- No PGN import/export, position editor, or save-and-resume feature.
- Threefold repetition and the fifty-move threshold are automatic rather than claim-based.
- Dead-position detection handles selected material patterns, not every theoretically dead position.
- Built-in search copies game states and has no overall thinking-time budget or cancellation mechanism. Exact root scores can increase thinking time, although the UI continues processing events.
- Master quiescence is depth-limited, and difficulty strength has not been benchmarked.
- Stockfish receives the current FEN rather than full move history. Its use or fallback is not displayed in the UI.
- Windows is the verified environment; packaging and cross-platform installation need more testing.
- Piece-art provenance and a project license have not yet been documented.

## Possible future improvements

These are ideas, not committed release promises:

- Let the human choose a color and flip or resize the board.
- Add thinking/status indicators and a configurable search budget.
- Improve search performance and compare difficulty levels systematically.
- Add PGN support, replay, and resumable games.
- Add clocks, resignation, draw offers, and optional claim-based draw handling.
- Expand special-move, search, and UI regression coverage and automate checks in CI.
- Improve installation and distribution, with verified asset attribution and licensing.

## Development notes

Change chess rules in `chess_engine/`, application policies in `chess_app/`, and visual presentation in `chess_ui/`. Add a regression test when fixing a behavior bug, and update the relevant folder guide when adding, removing, or moving files.

Version tagging and release publication are separate steps from documentation. Create a 1.0.0 tag only after the intended release changes are reviewed and committed.
