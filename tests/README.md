# Automated tests

Uses Python's unittest framework to exercise rules, bots, application behavior, and history storage.

[Project overview](../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Marks the test package. |
| [test_bot_gameplay.py](test_bot_gameplay.py) | Checks mode selection, bot delays, background results, automatic turns, undo, and discarding a stale result. |
| [test_dead_position.py](test_dead_position.py) | Checks supported insufficient-material patterns and non-dead counterexamples. |
| [test_easy_bot.py](test_easy_bot.py) | Checks the common bot interface and easy-bot move behavior. |
| [test_fifty_move_rule.py](test_fifty_move_rule.py) | Checks the half-move threshold, resets, undo, and game-ending behavior. |
| [test_game_over_gamemode.py](test_game_over_gamemode.py) | Checks endgame menu actions, mode selection, and difficulty navigation. |
| [test_hard_bot.py](test_hard_bot.py) | Checks HardBot configuration and tactical move selection. |
| [test_impossible_bot.py](test_impossible_bot.py) | Checks FEN conversion, UCI coordinate conversion, fallback, and startup/search timeouts with a deliberately unresponsive subprocess. |
| [test_master_bot.py](test_master_bot.py) | Checks MasterBot configuration and a legal tactical choice. |
| [test_match_history_saving.py](test_match_history_saving.py) | Checks save conditions, output folders, timestamps, and termination history. |
| [test_medium_bot.py](test_medium_bot.py) | Checks MediumBot configuration, legal opening moves, and avoiding a queen loss. |
| [test_release_regressions.py](test_release_regressions.py) | Covers promotion cancellation, exact root scoring, quiet check evasions, chronological undo history, and assets found from another working directory. |
| [test_threefold_repetition.py](test_threefold_repetition.py) | Checks repeated-position detection and undo behavior. |

## How this folder is used

From the project root, run `python -m unittest discover -s tests` using the environment where requirements.txt was installed. The suite currently has 58 tests. It needs pygame-ce; Stockfish timeout tests use a fake Python subprocess rather than requiring the real engine. Passing tests do not prove every chess position or visual interaction correct.
