# Computer players

Implements the five difficulty choices behind a shared choose_move(game_state) interface.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports BaseBot and the five concrete bot classes. |
| [base.py](base.py) | Defines the abstract interface returning an origin/target move or None. |
| [easy_bot.py](easy_bot.py) | Scores immediate captures, central squares, development, and promotion; randomly selects among similarly scored moves. |
| [medium_bot.py](medium_bot.py) | Uses a two-ply alpha-beta search with material and development evaluation. Each root candidate receives a full-window score before near-best selection. |
| [hard_bot.py](hard_bot.py) | Extends MediumBot with a default three-ply search and positional evaluation for pawns, pieces, rooks, and king placement. |
| [master_bot.py](master_bot.py) | Extends HardBot with a default two-ply search plus two levels of quiescence, strategic evaluation, and no near-best score tolerance. Quiescence considers all legal evasions when checked. |
| [impossible_bot.py](impossible_bot.py) | Finds and manages Stockfish through UCI, converts positions to FEN and returned moves to coordinates, enforces response deadlines, handles promotion choice, and falls back to HardBot. |

## How this folder is used

The application runs thinking off the UI thread. Built-in search copies states and can be expensive; depth is measured in half-moves (plies). Medium and Hard allow near-best randomness. Master still randomly breaks exact ties despite its zero choice window. Built-in bots promote to queens; Stockfish may select an underpromotion. Difficulty names are descriptive, not measured ratings. See the [Stockfish setup guide](../../assets/stockfish/README.md).
