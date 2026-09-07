# Move subsystem

Provides the public move facade and separates generation, execution, and logging.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports Move. |
| [move.py](move.py) | Connects MoveGenerator, MoveExecutor, and MoveLogger; exposes move requests, legal moves, undo, structured notation, and event logs. |

## Subfolders

| Folder | Purpose |
| --- | --- |
| [generation/](generation/README.md) | Builds candidate moves, then removes those that leave the moving king in check. |
| [execution/](execution/README.md) | Applies legal moves and keeps board state, special rights, counters, and history synchronized. |
| [history/](history/README.md) | Separates reversible move records from human-readable events. |

## How this folder is used

Generation answers which moves are legal. Execution changes the position and records the result. History provides separate chronological events and the active-move records needed for undo. A promotion request remains pending until a piece type is chosen.
