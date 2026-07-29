from dataclasses import dataclass


@dataclass(slots=True)
class Health:
	current: int
	maximum: int
	temporary: int = 0
