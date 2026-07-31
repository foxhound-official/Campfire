from app.models.campaign import Campaign
from app.models.character import Character
from app.models.creature import Creature
from app.models.scene_data import SceneData


class CombatError(Exception):
	pass


class CombatTargetNotFoundError(CombatError):
	pass


class CombatSceneNotFoundError(CombatError):
	pass


class CombatSystem:

	def __init__(
			self,
			campaign: Campaign,
	):
		self.campaign = campaign

	def set_campaign(
			self,
			campaign: Campaign,
	) -> None:
		self.campaign = campaign

	def damage_character(
			self,
			character_id: str,
			amount: int,
	) -> int:
		character = self._get_character(
			character_id
		)

		return character.health.take_damage(
			amount
		)

	def heal_character(
			self,
			character_id: str,
			amount: int,
	) -> int:
		character = self._get_character(
			character_id
		)

		return character.health.heal(amount)

	def damage_creature(
			self,
			creature_id: str,
			amount: int,
			scene_id: str | None = None,
	) -> int:
		creature = self._get_creature(
			creature_id,
			scene_id,
		)

		return creature.health.take_damage(
			amount
		)

	def heal_creature(
			self,
			creature_id: str,
			amount: int,
			scene_id: str | None = None,
	) -> int:
		creature = self._get_creature(
			creature_id,
			scene_id,
		)

		return creature.health.heal(amount)

	def _get_character(
			self,
			character_id: str,
	) -> Character:
		character = self.campaign.find_character(
			character_id
		)

		if character is None:
			raise CombatTargetNotFoundError(
				"Персонаж отсутствует в кампании: "
				f"{character_id}"
			)

		return character

	def _get_creature(
			self,
			creature_id: str,
			scene_id: str | None,
	) -> Creature:
		scene = self._get_scene(scene_id)

		creature = scene.find_creature(
			creature_id
		)

		if creature is None:
			raise CombatTargetNotFoundError(
				"Существо отсутствует в сцене: "
				f"{creature_id}"
			)

		return creature

	def _get_scene(
			self,
			scene_id: str | None,
	) -> SceneData:
		resolved_scene_id = (
			scene_id
			if scene_id is not None
			else self.campaign.active_scene_id
		)

		scene = self.campaign.find_scene(
			resolved_scene_id
		)

		if scene is None:
			raise CombatSceneNotFoundError(
				"Сцена отсутствует в кампании: "
				f"{resolved_scene_id}"
			)

		return scene
