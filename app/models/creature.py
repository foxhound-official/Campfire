from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.health import Health


@dataclass(slots=True)
class Creature(JSONWizard):
	id: str = field(default_factory=lambda: str(uuid4()))

	name: str = ""
	portrait: str = ""

	health: Health = field(
		default_factory=lambda: Health(
			current=1,
			maximum=1,
		)
	)