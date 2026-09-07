# Piece animation

Interpolates visual piece movement independently of chess state.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports MoveAnimation. |
| [move_animation.py](move_animation.py) | Queues one or more piece animations, interpolates screen positions, skips their stationary destinations while active, and removes completed animations. |

## How this folder is used

The application applies a move first, then queues its animation. Castling queues both king and rook. Undo stops animations. Animation does not change whose turn it is or decide legality.
