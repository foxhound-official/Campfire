from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class Item(JSONWizard):
	pass
