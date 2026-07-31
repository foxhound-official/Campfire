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