"""JSON-backed image allowances by Discord user and Thailand date."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import os
import tempfile
from threading import Lock


THAILAND = timezone(timedelta(hours=7))
DAILY_IMAGE_LIMIT = 80
# All instances in the bot process share a lock for read/update/write operations.
_USAGE_LOCK = Lock()


class DailyQuota:
    def __init__(self, path="data/usage.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _day(now=None):
        return (now or datetime.now(THAILAND)).astimezone(THAILAND).date().isoformat()

    def _read(self, day):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {"day": day, "users": {}}
        # Do not silently erase usage if the file has been damaged or edited badly.
        if (
            not isinstance(data, dict)
            or not isinstance(data.get("day"), str)
            or not isinstance(data.get("users"), dict)
            or any(type(used) is not int or not 0 <= used <= DAILY_IMAGE_LIMIT
                   for used in data["users"].values())
        ):
            raise ValueError("Invalid daily usage JSON file")
        if data["day"] != day:
            return {"day": day, "users": {}}
        return data

    def _write(self, data):
        # Replace only after the complete JSON is saved, avoiding partial files.
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent,
                prefix=".usage-", suffix=".tmp", delete=False,
            ) as stream:
                temporary = Path(stream.name)
                json.dump(data, stream, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def remaining(self, user_id, *, now=None):
        with _USAGE_LOCK:
            data = self._read(self._day(now))
            return DAILY_IMAGE_LIMIT - data["users"].get(str(user_id), 0)

    def reserve(self, user_id, count, *, now=None):
        """Count an entire accepted batch; return (accepted, remaining).

        A new Thailand date starts at zero without relying on a running timer.
        Reservations count attempts, including downstream processing failures.
        """
        if type(count) is not int or count < 1:
            raise ValueError("Image count must be a positive integer")
        with _USAGE_LOCK:
            data = self._read(self._day(now))
            used = data["users"].get(str(user_id), 0)
            if used + count > DAILY_IMAGE_LIMIT:
                return False, DAILY_IMAGE_LIMIT - used
            data["users"][str(user_id)] = used + count
            self._write(data)
            return True, DAILY_IMAGE_LIMIT - used - count
