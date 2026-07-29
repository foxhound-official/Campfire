from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class Health(JSONWizard):
	current: int
	maximum: int
	temporary: int = 0
