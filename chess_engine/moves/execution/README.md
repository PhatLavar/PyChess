# Move execution and undo

Applies legal moves and keeps board state, special rights, counters, and history synchronized.

[Project overview](../../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports MoveExecutor. |
| [move_executor.py](move_executor.py) | Validates move requests, chooses a specialized executor, completes promotion, and exposes undo outcomes. |
| [normal_executor.py](normal_executor.py) | Applies ordinary moves and captures, updates special state and the half-move clock, evaluates the turn, and records it. |
| [castling_executor.py](castling_executor.py) | Moves both king and rook, updates castling rights, and records the turn. |
| [en_passant_executor.py](en_passant_executor.py) | Moves the capturing pawn and removes the adjacent pawn from its separate capture square. |
| [promotion_executor.py](promotion_executor.py) | Stores a pending promotion request and later replaces the pawn with the selected piece before completing the turn. |
| [state_updater.py](state_updater.py) | Shares king-square updates, castling-right snapshots, rook/king rights removal, and en passant state updates. |
| [undo_executor.py](undo_executor.py) | Cancels pending promotion or restores the last completed move, including special moves, rights, counters, and repetition state; appends a chronological undo event. |

## How this folder is used

The engine undoes one completed move at a time. The application decides whether a user action should undo a complete player–bot round. A pending promotion is cancelled separately. Undo is blocked after game over. Keep the structured notation stack and the chronological event log distinct: undo pops the former and appends to the latter.
