from datetime import datetime
from pathlib import Path

from chess_app.config import (
    MATCH_HISTORY_FILE_EXTENSION,
    MATCH_HISTORY_FOLDER_NAME,
    MATCH_HISTORY_TIMESTAMP_FORMAT,
)


class MatchHistory:
    """
    Save completed match logs outside the chess engine.
    """

    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    def __init__(self, history_directory=None):
        """
        Configure where completed match logs are stored.

        Args:
            history_directory: Optional directory override, primarily useful
            for tests. By default, logs go into the project's
            `match_history` folder.
        """
        self.history_directory = (
            Path(history_directory)
            if history_directory is not None
            else self.PROJECT_ROOT / MATCH_HISTORY_FOLDER_NAME
        )

    def ensure_directory(self):
        """
        Create the history directory when missing.

        Returns:
            The history directory `Path`. Existing directories are left
            unchanged, so calling this method repeatedly is safe.
        """
        self.history_directory.mkdir(parents=True, exist_ok=True)
        return self.history_directory

    def save(self, move_log, completed_at=None):
        """
        Write all displayed move-log entries into one UTF-8 text file.

        Args:
            move_log: Ordered terminal log strings from the completed match.
            completed_at: Optional datetime override used for deterministic
            tests. The current local datetime is used by default.

        Returns:
            The `Path` of the newly written history file.
        """
        self.ensure_directory()
        timestamp = (completed_at or datetime.now()).strftime(
            MATCH_HISTORY_TIMESTAMP_FORMAT
        )
        history_path = self._get_available_path(timestamp)
        file_contents = '\n'.join(move_log) + '\n'
        history_path.write_text(file_contents, encoding='utf-8')
        return history_path

    def _get_available_path(self, timestamp):
        """
        Return a non-existing path while preserving the timestamp prefix.

        Returns:
            `YYYYMMDD-HHMM.txt` when available. If another match ended in
            the same minute, returns `YYYYMMDD-HHMM-2.txt` and increments
            the suffix as needed so an earlier history is never overwritten.
        """
        base_name = f'{timestamp}{MATCH_HISTORY_FILE_EXTENSION}'
        history_path = self.history_directory / base_name

        if not history_path.exists():
            return history_path

        duplicate_number = 2
        while True:
            duplicate_name = (
                f'{timestamp}-{duplicate_number}'
                f'{MATCH_HISTORY_FILE_EXTENSION}'
            )
            history_path = self.history_directory / duplicate_name

            if not history_path.exists():
                return history_path

            duplicate_number += 1
