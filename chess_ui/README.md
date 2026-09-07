# Pygame presentation

Draws the board and user interface without owning chess-rule decisions.

[Project overview](../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Marks the UI package. |
| [config.py](config.py) | Defines board dimensions, colors, fonts, layout sizes, animation timing, and the project-relative piece-image directory. |

## Subfolders

| Folder | Purpose |
| --- | --- |
| [animations/](animations/README.md) | Interpolates visual piece movement independently of chess state. |
| [renderers/](renderers/README.md) | Composes the board display from the current match and interaction state. |
| [screens/](screens/README.md) | Displays matchup choices, promotion choices, and finished-match screens. |
| [components/](components/README.md) | Reserved for reusable UI components if the interface grows. |

## How this folder is used

The application constructs UI objects around the current match. Renderers compose the board, highlights, animations, and screens. Coordinates are always shown from White's side. The fixed board is 512×512 pixels.
