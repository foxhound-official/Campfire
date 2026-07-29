from dataclasses import dataclass, field
from uuid import uuid4

from app.models.effect import Effect
from app.models.health import Health
from app.models.item import Item


@dataclass(slots=True)
class Character:
	id: str = field(default_factory=lambda: str(uuid4()))

	name: str = ""
	portrait: str = ""

	race: str = ""
	character_class: str = ""
	level: int = 1

	health: Health = field(
		default_factory=lambda: Health(
			current=1,
			maximum=1
		)
	)

	inventory: list[Item] = field(default_factory=list)
	effects: list[Effect] = field(default_factory=list)

	notes: str = ""
