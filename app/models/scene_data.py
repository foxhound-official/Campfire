from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.creature import Creature
from app.models.scene_type import SceneType


@dataclass(slots=True)
class SceneData(JSONWizard):
	id: str = field(
		default_factory=lambda: str(uuid4())
	)

	scene_type: SceneType = SceneType.BATTLE
	title: str = "Новая сцена"

	background: str = ""
	music: str = ""

	description: str = ""

	creatures: list[Creature] = field(
		default_factory=list
	)

	def find_creature(
			self,
			creature_id: str | None,
	) -> Creature | None:
		if creature_id is None:
			return None

		for creature in self.creatures:
			if creature.id == creature_id:
				return creature

		return None
