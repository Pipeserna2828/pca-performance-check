from datetime import datetime, timezone


class RequestIdGenerator:
    def __init__(self) -> None:
        self._sequence = 0

    def next_id(self) -> str:
        self._sequence += 1
        return f"PPC-{datetime.now(timezone.utc):%Y%m%d}-{self._sequence:04d}"
