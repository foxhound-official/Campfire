from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.character_feature import CharacterFeature
from app.models.character_skills import CharacterSkills
from app.models.character_stats import CharacterStats
from app.models.effect import Effect
from app.models.health import Health
from app.models.item import Item


@dataclass(slots=True)
class Character(JSONWizard):
	id: str = field(default_factory=lambda: str(uuid4()))

	inventory_capacity: int = 12
	inventory: list[Item] = field(default_factory=list)

	name: str = ""
	portrait: str = ""
	party_portrait: str = ""

	race: str = ""
	character_class: str = ""
	level: int = 1

	health: Health = field(
		default_factory=lambda: Health(
			current=1,
			maximum=1
		)
	)

	stats: CharacterStats = field(
		default_factory=CharacterStats
	)

	skills: CharacterSkills = field(
		default_factory=CharacterSkills
	)

	features: list[CharacterFeature] = field(
		default_factory=list
	)

	inventory: list[Item] = field(default_factory=list)
	effects: list[Effect] = field(default_factory=list)

	notes: str = ""
