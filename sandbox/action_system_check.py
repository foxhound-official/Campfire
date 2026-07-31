from app.systems.combat.combat_system import (
	CombatSystem,
	CombatTargetNotFoundError,
)
from app.models.action_request import (
	ActionRequest,
	ActionRequestStatus,
	ActionType,
)
from app.models.campaign import Campaign
from app.models.character import Character
from app.models.creature import Creature
from app.models.health import Health
from app.models.item import Item
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType


def run_tests() -> None:
	potion = Item(
		name="Лечебное зелье",
		quantity=2,
	)

	character = Character(
		name="Альрик",
		health=Health(
			current=6,
			maximum=10,
			temporary=2,
		),
		inventory=[potion],
	)

	target = Character(
		name="Мира",
		health=Health(
			current=4,
			maximum=12,
		),
	)

	creature = Creature(
		name="Гоблин",
		health=Health(
			current=8,
			maximum=8,
		),
	)

	scene = SceneData(
		scene_type=SceneType.BATTLE,
		title="Тестовый бой",
		creatures=[creature],
	)

	campaign = Campaign(
		characters=[
			character,
			target,
		],
		scenes=[scene],
		active_scene_id=scene.id,
	)

	combat = CombatSystem(campaign)

	request = ActionRequest(
		action_type=ActionType.USE_ITEM,
		character_id=character.id,
		target_id=target.id,
		item_id=potion.id,
	)

	assert (
		request.status
		== ActionRequestStatus.PENDING
	)

	restored_request = (
		ActionRequest.from_json(
			request.to_json()
		)
	)

	assert restored_request.id == request.id
	assert (
		restored_request.action_type
		== ActionType.USE_ITEM
	)
	assert (
		restored_request.target_id
		== target.id
	)

	restored_health = combat.heal_character(
		target.id,
		5,
	)

	assert restored_health == 5
	assert target.health.current == 9

	applied_damage = combat.damage_creature(
		creature.id,
		3,
	)

	assert applied_damage == 3
	assert creature.health.current == 5

	try:
		combat.damage_character(
			"missing-character",
			1,
		)

	except CombatTargetNotFoundError:
		pass

	else:
		raise AssertionError(
			"Ожидалась ошибка отсутствующей цели"
		)


if __name__ == "__main__":
	run_tests()
	print("Action system checks passed")