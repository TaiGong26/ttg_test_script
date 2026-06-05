from dataclasses import dataclass, field
from typing import Literal

SlotName = Literal["start", "target"]
EXPECTED_DIM = 6


class InvalidSlotError(ValueError):
    pass


class SlotAlreadyRecordedError(RuntimeError):
    pass


@dataclass
class WaypointStore:
    _start: list[float] | None = field(default=None, init=False)
    _target: list[float] | None = field(default=None, init=False)

    @property
    def slots(self) -> tuple[SlotName, ...]:
        return ("start", "target")

    def is_recorded(self, slot: SlotName) -> bool:
        self._validate_slot(slot)
        return getattr(self, f"_{slot}") is not None

    def get(self, slot: SlotName) -> list[float] | None:
        self._validate_slot(slot)
        return getattr(self, f"_{slot}")

    def record(self, slot: SlotName, angles: list[float], force: bool = False) -> None:
        self._validate_slot(slot)
        self._validate_dim(angles)
        if getattr(self, f"_{slot}") is not None and not force:
            raise SlotAlreadyRecordedError(f"{slot} already recorded; pass force=True to overwrite")
        setattr(self, f"_{slot}", list(angles))

    def clear(self, slot: SlotName) -> None:
        self._validate_slot(slot)
        setattr(self, f"_{slot}", None)

    def _validate_slot(self, slot: str) -> None:
        if slot not in self.slots:
            raise InvalidSlotError(f"slot must be one of {self.slots}, got {slot!r}")

    @staticmethod
    def _validate_dim(angles: list[float]) -> None:
        if len(angles) != EXPECTED_DIM:
            raise ValueError(f"angles must have {EXPECTED_DIM} elements, got {len(angles)}")
