from app.models.action_target_type import (
	ActionTargetType,
)
from app.models.item import Item
from app.ui.controllers.target_selection_controller import (
	TargetSelectionController,
	TargetSelectionError,
	TargetSelectionState,
	TargetSelectionStateError,
	TargetTypeNotAllowedError,
)


def run_tests() -> None:
	potion = Item(
		name="Лечебное зелье",
		target_types=[
			ActionTargetType.CHARACTER,
		],
	)

	controller = TargetSelectionController()

	assert (
		controller.state
		== TargetSelectionState.IDLE
	)
	assert not controller.is_active

	controller.start(
		character_id="alrik-id",
		item=potion,
	)

	assert (
		controller.state
		== TargetSelectionState.SELECTING
	)
	assert controller.is_active
	assert controller.current_item is potion

	assert controller.can_select(
		ActionTargetType.CHARACTER
	)
	assert not controller.can_select(
		ActionTargetType.CREATURE
	)

	try:
		controller.start(
			character_id="alrik-id",
			item=potion,
		)

	except TargetSelectionStateError:
		pass

	else:
		raise AssertionError(
			"Нельзя запустить второй выбор цели"
		)

	try:
		controller.select_target(
			target_type=ActionTargetType.CREATURE,
			target_id="creature-id",
		)

	except TargetTypeNotAllowedError:
		pass

	else:
		raise AssertionError(
			"Нельзя выбрать недопустимый тип цели"
		)

	selection = controller.select_target(
		target_type=ActionTargetType.CHARACTER,
		target_id="mira-id",
	)

	assert (
		controller.state
		== TargetSelectionState.CONFIRMING
	)
	assert selection.character_id == "alrik-id"
	assert selection.item_id == potion.id
	assert (
		selection.target_type
		== ActionTargetType.CHARACTER
	)
	assert selection.target_id == "mira-id"

	controller.back_to_selection()

	assert (
		controller.state
		== TargetSelectionState.SELECTING
	)
	assert controller.selection is None

	controller.select_target(
		target_type=ActionTargetType.CHARACTER,
		target_id="mira-id",
	)

	completed_selection = controller.complete()

	assert completed_selection.target_id == "mira-id"
	assert (
		controller.state
		== TargetSelectionState.IDLE
	)
	assert not controller.is_active
	assert controller.current_item is None

	controller.start(
		character_id="alrik-id",
		item=potion,
	)

	controller.cancel()

	assert (
		controller.state
		== TargetSelectionState.IDLE
	)

	ordinary_item = Item(
		name="Обычный предмет",
	)

	try:
		controller.start(
			character_id="alrik-id",
			item=ordinary_item,
		)

	except TargetSelectionError:
		pass

	else:
		raise AssertionError(
			"Предмет без типов целей нельзя использовать"
		)


if __name__ == "__main__":
	run_tests()
	print("Target selection controller checks passed")