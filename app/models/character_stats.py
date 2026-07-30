from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class CharacterStats(JSONWizard):
	strength: int = 0
	agility: int = 0
	intelligence: int = 0
	charisma: int = 0
	endurance: int = 0