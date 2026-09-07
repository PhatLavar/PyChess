# Application coordination

Connects the Pygame window, chess engine, bots, user input, and match-history storage. This is the place to change application behavior rather than chess rules or drawing styles.

[Project overview](../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports ChessGame for the root entry point. |
| [chess_game.py](chess_game.py) | Owns the frame loop, match creation, game modes, bot turns, undo policy, rematches, shutdown, and history-saving coordination. Bot searches run on snapshots in background threads; completed results are applied on the UI thread. |
| [config.py](config.py) | Defines the frame-rate limit, bot delay, and history directory, timestamp, extension, and separator settings. |
| [event_handler.py](event_handler.py) | Routes window-close, mouse, and Z-key events to menus, board input, undo, and endgame actions. |
| [input_handler.py](input_handler.py) | Translates board clicks into moves, tracks selection and legal targets, handles promotion choices, and starts animations. |
| [match_history.py](match_history.py) | Writes UTF-8 event logs into mode-specific directories and adds numeric suffixes when timestamps collide. |

## How this folder is used

A frame processes events, polls any pending bot result, draws the current screen, and limits the frame rate. The main thread owns the live GameState; workers receive independent copies. Undo or a replaced match makes old bot results ineligible. Bot resource cleanup waits for an active search before closing that bot.
