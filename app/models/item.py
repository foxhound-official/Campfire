from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class Item(JSONWizard):
	id: str = field(default_factory=lambda: str(uuid4()))

	name: str = ""
	description: str = ""
	image_name: str = ""

	quantity: int = 1