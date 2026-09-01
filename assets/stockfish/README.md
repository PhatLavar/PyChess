# Stockfish Setup

The **Impossible** bot uses Stockfish when a compatible Stockfish executable
is available in this folder.

## Windows installation

1. Visit the official Stockfish download page:
   <https://stockfishchess.org/download/>
2. Under **Windows (x64)**, download the **AVX2** `.zip` archive. This is the
   recommended version for most modern Windows computers.
3. Extract the downloaded archive.
4. Find the Stockfish `.exe` file inside the extracted folder.
5. Rename the executable to:

   ```text
   stockfish.exe
   ```

6. Copy it into this folder. The finished path should be:

   ```text
   PyChess/assets/stockfish/stockfish.exe
   ```

If the AVX2 version does not run on your computer, download the generic
**64-bit** Windows build from the same page instead, then follow the same
extraction and renaming steps.

The executable is intentionally excluded from Git because it is large,
platform-specific, and distributed under the GPLv3 license. When the file is
not installed, Impossible mode uses PyChess's strongest built-in fallback bot.
