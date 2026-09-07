# Runtime assets

Holds piece artwork and the optional external chess engine.

[Project overview](../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |

## Subfolders

| Folder | Purpose |
| --- | --- |
| [images/](images/README.md) | Groups artwork used by the Pygame renderer. |
| [stockfish/](stockfish/README.md) | Provides the conventional local installation directory for the engine used by Impossible mode. |

## How this folder is used

Images are required to start a match. Stockfish is optional: Impossible mode uses a built-in fallback when it is unavailable. PNG files are tracked; the local Windows Stockfish executable is ignored by Git.
