# Menus and modal screens

Displays matchup choices, promotion choices, and finished-match screens.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| [__init__.py](__init__.py) | Exports StartMenuUI, PromotionUI, and GameOverUI. |
| [start_menu_ui.py](start_menu_ui.py) | Displays player–player, player–bot, and bot–bot choices, followed by the five bot difficulties. |
| [promotion_ui.py](promotion_ui.py) | Draws queen, rook, bishop, and knight buttons and translates a click into a promotion type. |
| [game_over_ui.py](game_over_ui.py) | Displays the timed endgame effect, result, rematch button, and mode/difficulty changes; reuses StartMenuUI for difficulty selection. |

## How this folder is used

Screens return actions to the application rather than creating matches themselves. The endgame effect precedes the result buttons. Mode switching is available through the finished-match screen; there is no in-game pause or settings menu.
