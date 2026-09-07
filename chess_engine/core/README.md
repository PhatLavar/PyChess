# Core models

Stores the board and the state of one match.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports Board, GameState, and Piece. |
| [board.py](board.py) | Stores the starting 8×8 board and provides piece access and replacement methods. |
| [game_state.py](game_state.py) | Owns side to move, cached king squares, castling and en passant state, pending promotion, draw trackers, and final result. finish_turn switches players and evaluates game-ending conditions. |
| [piece.py](piece.py) | Lists the twelve supported piece codes used by the renderer and other consumers. |

## How this folder is used

Board setters are low-level operations and do not validate chess rules. Normal gameplay should use the move API. Tests that create custom positions must also update king positions, turn, and special-move state as needed.
