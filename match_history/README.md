# Saved match history

Stores local UTF-8 event logs written when a match finishes or the window closes after at least one completed move.

[Project overview](../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| `*.txt` (generated locally) | One timestamped match event log per file; see the format notes below. |

## Subfolders

| Folder | Purpose |
| --- | --- |
| [player-player/](player-player/README.md) | Contains saved event logs for Player–Player matches. |
| [player-bot/](player-bot/README.md) | Contains saved event logs for Player–Bot matches. |
| [bot-bot/](bot-bot/README.md) | Contains saved event logs for Bot–Bot matches. |

## How this folder is used

Current files are grouped by matchup. Older timestamped .txt files directly in this folder are historical output from earlier layouts. Names use YYYYMMDD-HHMM.txt in local time, with -2, -3, etc. for collisions. Each file contains chronological events and the result; a normal early window close records TERMINATED. These are not PGN files or resumable saves. A match with no remaining applied moves is not saved. Personal .txt files are ignored by Git, while these guides are included.
