# Optional Stockfish engine

Provides the conventional local installation directory for the engine used by Impossible mode.

[Project overview](../../README.md) · [Parent folder](../README.md)

## Files

| File | Purpose |
| --- | --- |
| README.md | This folder guide. |
| `stockfish.exe` | Optional, locally installed Windows executable. It is ignored by Git and is not included when cloning the repository. |

## Setup

Download a Stockfish build compatible with your operating system and CPU from the [official download page](https://stockfishchess.org/download/). On Windows, extract the archive, rename the executable to `stockfish.exe`, and place it beside this README. The app must be able to execute it.

You can instead point the application to another executable. In PowerShell, set the variable before starting the game:

```powershell
$env:PYCHESS_STOCKFISH_PATH = "C:\Tools\Stockfish\stockfish.exe"
python chess.py
```

The variable applies to the current shell and processes launched from it. Use your real executable path.

## Discovery order

1. An explicit `ImpossibleBot(executable_path=...)` argument, for code-level use.
2. The `PYCHESS_STOCKFISH_PATH` environment variable.
3. A program named `stockfish` on `PATH`.
4. `stockfish/stockfish.exe` under the project root, if present.
5. `assets/stockfish/stockfish.exe` under the project root.

The first candidate that exists as a file is selected. The two bundled-path candidates do not depend on the launch directory. An existing but incompatible executable can still fail during startup; discovery alone does not verify usability.

## Runtime behavior

The adapter starts a persistent UCI subprocess, configures one thread and a 64 MB hash, and normally requests 500 ms of thinking per move. Startup responses have a five-second deadline; move responses have the requested thinking time plus five seconds. Output is read through a background queue using UTF-8 with replacement for undecodable bytes.

If a handled engine failure or timeout occurs, the adapter closes the process and uses `HardBot(depth=3, choice_window=0)`. Missing engines and unusable returned moves also lead to fallback. Impossible mode therefore does not guarantee Stockfish is active, and there is currently no on-screen engine-status indicator.

Only the current FEN is sent, not the full move history. The app still adjudicates its own repetition and draw rules. Stockfish promotion suffixes are passed back to the application.

The executable is an external dependency, not PyChess source. Consult its accompanying distribution and license information if redistributing it.
