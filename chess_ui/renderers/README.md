# Board renderers

Composes the board display from the current match and interaction state.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports GameRenderer. |
| [game_renderer.py](game_renderer.py) | Loads all twelve PNG piece images and draws board squares, highlights, stationary pieces, moving pieces, promotion choices, and endgame UI. |
| [highlight_renderer.py](highlight_renderer.py) | Draws hover, selection, legal-target, capture, and checked-king overlays. |

## How this folder is used

Piece images are resolved relative to the project, not the launch directory. Rendering reads engine state; user actions flow through the application's input handler. A legal en passant target is empty, so its current highlight uses the quiet-move color.
