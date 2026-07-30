from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class CharacterFeature(JSONWizard):
	title: str = ""
	icon_name: str = ""
	description: str = ""