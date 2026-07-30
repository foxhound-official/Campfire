from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.character import Character
from app.models.creature import Creature
from app.models.scene_type import SceneType


@dataclass(slots=True)
class Campaign(JSONWizard):
	id: str = field(default_factory=lambda: str(uuid4()))

	name: str = "Новая кампания"
	active_scene: SceneType = SceneType.BATTLE

	characters: list[Character] = field(default_factory=list)
	creatures: list[Creature] = field(default_factory=list)

	notes: str = ""

	def find_character(
			self,
			character_id: str | None,
	) -> Character | None:
		if character_id is None:
			return None

		for character in self.characters:
			if character.id == character_id:
				return character

		return None
