# Rule validation

Answers attack, king-safety, special-move, and draw questions for the current state.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports MoveValidator. |
| [move_validator.py](move_validator.py) | Facade exposing the individual validators through one interface. |
| [attack_validator.py](attack_validator.py) | Checks pawn, knight, king, rook, bishop, and queen attacks on a square. |
| [check_validator.py](check_validator.py) | Locates cached king squares and detects check, checkmate, and stalemate. |
| [castling_validator.py](castling_validator.py) | Checks retained rights, home king and rook, empty paths, check, and attacked transit squares. |
| [en_passant_validator.py](en_passant_validator.py) | Recognizes en passant from the current target and previous double-pawn move. |
| [promotion_validator.py](promotion_validator.py) | Checks whether a destination is the active pawn color's promotion rank. |
| [dead_position_validator.py](dead_position_validator.py) | Recognizes bare kings, one minor piece versus a bare king, and bishop-only positions whose bishops all occupy the same square color. |
| [fifty_move_rule.py](fifty_move_rule.py) | Tracks consecutive half-moves without a pawn move or capture; supports undo and automatically draws at 100. |
| [repetition_tracker.py](repetition_tracker.py) | Counts positions using board contents, side to move, castling rights, and legally usable en passant availability; supports undo. |

## How this folder is used

GameState.finish_turn applies the result checks. PyChess automatically ends on threefold repetition and the fifty-move threshold rather than offering a draw-claim interface. Dead-position recognition covers the listed material patterns; it is not a complete solver for every position in which mate is impossible.
