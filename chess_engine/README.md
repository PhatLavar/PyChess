# Chess engine

Contains board state, legal-move rules, reversible moves, history, and computer players. The engine does not depend on Pygame and can be exercised directly in tests.

[Project overview](../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports GameState as the public starting point for engine users. |

## Subfolders

| Folder | Purpose |
| --- | --- |
| [core/](core/README.md) | Stores the board and the state of one match. |
| [bots/](bots/README.md) | Implements the five difficulty choices behind a shared choose_move(game_state) interface. |
| [moves/](moves/README.md) | Provides the public move facade and separates generation, execution, and logging. |
| [rules/](rules/README.md) | Answers attack, king-safety, special-move, and draw questions for the current state. |
| [utilities/](utilities/README.md) | Contains small helpers and constants without UI responsibilities. |

## How this folder is used

Use GameState.move.handle_piece_move(origin, target) to request a move. The result identifies a completed move, pending promotion, or rejection. Complete pending promotion through the executor. Board coordinates are zero-based (row, column), with (0, 0) = a8 and (7, 7) = h1. Piece codes combine color and type, such as wN; '--' means empty.
