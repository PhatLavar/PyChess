# Shared engine helpers

Contains small helpers and constants without UI responsibilities.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Re-exports commonly used constants and helpers. |
| [constants.py](constants.py) | Defines empty-square encoding, movement offsets, and starting/target squares for castling. |
| [color_helpers.py](color_helpers.py) | Converts side-to-move flags into colors and returns an opposing color. |
| [piece_helpers.py](piece_helpers.py) | Extracts piece color/type and checks board bounds. |
| [promotion_helpers.py](promotion_helpers.py) | Returns promotion rank, color, and a full promoted-piece code. |

## How this folder is used

Use these helpers to keep piece encoding and coordinate conventions consistent across the engine. They do not validate or execute complete moves.
