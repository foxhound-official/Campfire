from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.character import Character
from app.models.creature import Creature
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType

CURRENT_SCHEMA_VERSION = 1

@dataclass(slots=True)
class Campaign(JSONWizard):
	schema_version: int = CURRENT_SCHEMA_VERSION

	id: str = field(default_factory=lambda: str(uuid4()))

	name: str = "Новая кампания"
	active_scene: SceneType = SceneType.BATTLE

	active_scene_id: str | None = None
	scenes: list[SceneData] = field(default_factory=list)

	characters: list[Character] = field(default_factory=list)
	creatures: list[Creature] = field(default_factory=list)

	notes: str = ""

	def __post_init__(self) -> None:
		if not self.scenes:
			self.scenes.append(
				SceneData(
					scene_type=self.active_scene,
					title="Поле боя",
					creatures=self.creatures,
				)
			)

		active_scene = self.find_scene(
			self.active_scene_id
		)

		if active_scene is None:
			active_scene = self.scenes[0]
			self.active_scene_id = active_scene.id

		self._sync_legacy_scene_fields(
			active_scene
		)

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

	def find_scene(
			self,
			scene_id: str | None,
	) -> SceneData | None:
		if scene_id is None:
			return None

		for scene in self.scenes:
			if scene.id == scene_id:
				return scene

		return None

	def get_active_scene(self) -> SceneData:
		scene = self.find_scene(
			self.active_scene_id
		)

		if scene is None:
			raise ValueError(
				"Активная сцена отсутствует в кампании"
			)

		return scene

	def set_active_scene(
			self,
			scene_id: str,
	) -> SceneData:
		scene = self.find_scene(scene_id)

		if scene is None:
			raise ValueError(
				f"Сцена с id={scene_id!r} не найдена"
			)

		self.active_scene_id = scene.id
		self._sync_legacy_scene_fields(scene)

		return scene

	def _sync_legacy_scene_fields(
			self,
			scene: SceneData,
	) -> None:
		self.active_scene = scene.scene_type
		self.creatures = scene.creatures