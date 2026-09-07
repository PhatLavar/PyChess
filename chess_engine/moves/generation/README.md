# Move generation

Builds candidate moves, then removes those that leave the moving king in check.

[Project overview](../../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports MoveGenerator. |
| [move_generator.py](move_generator.py) | Dispatches by piece type and filters pseudo-legal candidates using temporary simulation and own-king safety checks. |
| [move_simulation.py](move_simulation.py) | Temporarily moves pieces, handles en passant removal and king-square changes, then restores the position. This is a safety probe, not a complete turn executor. |
| [pawn_move_generator.py](pawn_move_generator.py) | Generates single and initial double pushes, diagonal captures, and available en passant destinations. |
| [sliding_move_generator.py](sliding_move_generator.py) | Walks rook, bishop, and queen rays; also supplies bounded directional steps for knights and kings. |
| [knight_move_generator.py](knight_move_generator.py) | Generates the eight possible knight offsets through the shared directional helper. |
| [king_move_generator.py](king_move_generator.py) | Generates king steps and asks the castling validator about both castling destinations. |

## How this folder is used

A move is ((origin_row, origin_col), (target_row, target_col)). Promotion alternatives share one origin/target pair; the chosen piece is supplied separately. Legal-move queries temporarily mutate and restore state, so workers must not query the live UI state concurrently.
