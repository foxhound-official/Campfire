from app.models.action_request import (
	ActionRequest,
	ActionRequestStatus,
	ActionType,
)
from app.models.campaign import Campaign
from app.models.character import Character
from app.models.health import Health
from app.models.item import (
	Item,
	ItemUseEffect,
)
from app.systems.actions.action_processor import (
	ActionProcessor,
)
from app.systems.actions.action_request_queue import (
	ActionRequestQueue,
	ActionRequestStateError,
)


def run_tests() -> None:
	potion = Item(
		name="Лечебное зелье",
		quantity=2,
		use_effect=ItemUseEffect.HEAL,
		effect_value=5,
	)

	alrik = Character(
		name="Альрик",
		inventory=[potion],
	)

	mira = Character(
		name="Мира",
		health=Health(
			current=4,
			maximum=12,
		),
	)

	campaign = Campaign(
		characters=[
			alrik,
			mira,
		],
	)

	queue = ActionRequestQueue()
	processor = ActionProcessor(campaign)

	accepted_request = ActionRequest(
		action_type=ActionType.USE_ITEM,
		character_id=alrik.id,
		target_id=mira.id,
		item_id=potion.id,
	)

	queue.submit(accepted_request)

	assert queue.get_pending() == [
		accepted_request
	]

	accepted_result = queue.accept(
		accepted_request.id,
		processor,
	)

	assert (
		accepted_result.status
		== ActionRequestStatus.ACCEPTED
	)
	assert accepted_result.applied_value == 5
	assert mira.health.current == 9
	assert potion.quantity == 1

	rejected_request = ActionRequest(
		action_type=ActionType.USE_ITEM,
		character_id=alrik.id,
		target_id=mira.id,
		item_id=potion.id,
	)

	queue.submit(rejected_request)

	rejected_result = queue.reject(
		rejected_request.id,
		"Зелье сейчас использовать нельзя",
	)

	assert (
		rejected_result.status
		== ActionRequestStatus.REJECTED
	)
	assert mira.health.current == 9
	assert potion.quantity == 1

	mira.health.current = mira.health.maximum

	failed_request = ActionRequest(
		action_type=ActionType.USE_ITEM,
		character_id=alrik.id,
		target_id=mira.id,
		item_id=potion.id,
	)

	queue.submit(failed_request)

	failed_result = queue.accept(
		failed_request.id,
		processor,
	)

	assert (
		failed_result.status
		== ActionRequestStatus.FAILED
	)
	assert potion.quantity == 1
	assert potion in alrik.inventory

	try:
		queue.accept(
			accepted_request.id,
			processor,
		)

	except ActionRequestStateError:
		pass

	else:
		raise AssertionError(
			"Обработанный запрос нельзя "
			"принять повторно"
		)

	assert queue.get_pending() == []


if __name__ == "__main__":
	run_tests()
	print("Action request flow checks passed")