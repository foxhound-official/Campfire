from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass(slots=True)
class CharacterSkills(JSONWizard):
	awareness: int = 0
	stealth: int = 0
	mechanics: int = 0
	magic: int = 0
	medicine: int = 0
	intimidation: int = 0

	acrobatics: int = 0
	athletics: int = 0
	sleight_of_hand: int = 0
	persuasion: int = 0
	training: int = 0
	survival: int = 0