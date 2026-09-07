# Move history and notation

Separates reversible move records from human-readable events.

[Project overview](../../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports MoveLogger. |
| [move_logger.py](move_logger.py) | Facade that delegates structured records, event formatting, and square-name conversion. |
| [history_logger.py](history_logger.py) | Appends dictionaries containing origins, destinations, captures, and any castling, en passant, or promotion data required by undo. |
| [record_logger.py](record_logger.py) | Formats and prints move, capture, check, promotion, castling, undo, and end-match events while appending them to the event list. |
| [notation_converter.py](notation_converter.py) | Converts internal coordinates into square names such as e4. |

## How this folder is used

notation is a stack of currently applied moves. move_log is chronological and retains moves that were later undone along with their undo events. The notation name does not mean SAN or PGN: saved history is a custom text format. File writing belongs to chess_app.match_history.
