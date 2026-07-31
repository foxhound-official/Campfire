from app.models.action_request import (
	ActionRequest,
	ActionType,
)
from app.models.action_target_type import (
	ActionTargetType,
)
from app.models.item import (
	Item,
	ItemUseEffect,
)


def run_tests() -> None:
	potion = Item(
		name="Лечебное зелье",
		use_effect=ItemUseEffect.HEAL,
		effect_value=5,
		target_types=[
			ActionTargetType.CHARACTER,
		],
	)

	request = ActionRequest(
		action_type=ActionType.USE_ITEM,
		character_id="character-id",
		target_type=ActionTargetType.CHARACTER,
		target_id="target-id",
		item_id=potion.id,
	)

	restored_item = Item.from_json(
		potion.to_json()
	)

	assert restored_item.target_types == [
		ActionTargetType.CHARACTER,
	]

	restored_request = ActionRequest.from_json(
		request.to_json()
	)

	assert (
		restored_request.target_type
		== ActionTargetType.CHARACTER
	)
	assert restored_request.target_id == "target-id"
	assert restored_request.item_id == potion.id

	legacy_item = Item.from_json(
		'{"name": "Старый предмет"}'
	)

	assert legacy_item.target_types == []


if __name__ == "__main__":
	run_tests()
	print("Action target type checks passed")