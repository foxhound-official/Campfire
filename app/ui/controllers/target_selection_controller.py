from dataclasses import dataclass
from enum import Enum

from app.models.action_target_type import (
	ActionTargetType,
)
from app.models.item import Item


class TargetSelectionState(str, Enum):
	IDLE = "idle"
	SELECTING = "selecting"
	CONFIRMING = "confirming"


class TargetSelectionError(Exception):
	pass


class TargetSelectionStateError(
		TargetSelectionError
):
	pass


class TargetTypeNotAllowedError(
		TargetSelectionError
):
	pass


@dataclass(frozen=True, slots=True)
class TargetSelection:
	character_id: str
	item_id: str
	target_type: ActionTargetType
	target_id: str


class TargetSelectionController:

	def __init__(self):
		self._state = TargetSelectionState.IDLE

		self._character_id: str | None = None
		self._item: Item | None = None

		self._allowed_target_types: tuple[
			ActionTargetType,
			...
		] = ()

		self._selection: TargetSelection | None = None

	@property
	def state(self) -> TargetSelectionState:
		return self._state

	@property
	def is_active(self) -> bool:
		return self._state != TargetSelectionState.IDLE

	@property
	def current_item(self) -> Item | None:
		return self._item

	@property
	def allowed_target_types(
			self,
	) -> tuple[ActionTargetType, ...]:
		return self._allowed_target_types

	@property
	def selection(self) -> TargetSelection | None:
		return self._selection

	def start(
			self,
			character_id: str,
			item: Item,
	) -> None:
		if self.is_active:
			raise TargetSelectionStateError(
				"Выбор цели уже запущен"
			)

		if not character_id:
			raise TargetSelectionError(
				"Не указан персонаж, использующий предмет"
			)

		if not item.target_types:
			raise TargetSelectionError(
				"Для предмета не указаны допустимые цели"
			)

		self._character_id = character_id
		self._item = item
		self._allowed_target_types = tuple(
			item.target_types
		)

		self._selection = None
		self._state = TargetSelectionState.SELECTING

	def can_select(
			self,
			target_type: ActionTargetType,
	) -> bool:
		return (
			self._state
			== TargetSelectionState.SELECTING
			and target_type
			in self._allowed_target_types
		)

	def select_target(
			self,
			target_type: ActionTargetType,
			target_id: str,
	) -> TargetSelection:
		if (
			self._state
			!= TargetSelectionState.SELECTING
		):
			raise TargetSelectionStateError(
				"Сейчас цель выбрать нельзя"
			)

		if (
			target_type
			not in self._allowed_target_types
		):
			raise TargetTypeNotAllowedError(
				"Этот тип цели недоступен "
				"для выбранного предмета"
			)

		if not target_id:
			raise TargetSelectionError(
				"Не указан идентификатор цели"
			)

		if (
			self._character_id is None
			or self._item is None
		):
			raise TargetSelectionStateError(
				"Данные выбора цели потеряны"
			)

		self._selection = TargetSelection(
			character_id=self._character_id,
			item_id=self._item.id,
			target_type=target_type,
			target_id=target_id,
		)

		self._state = (
			TargetSelectionState.CONFIRMING
		)

		return self._selection

	def back_to_selection(self) -> None:
		if (
			self._state
			!= TargetSelectionState.CONFIRMING
		):
			raise TargetSelectionStateError(
				"Нет выбранной цели для изменения"
			)

		self._selection = None
		self._state = TargetSelectionState.SELECTING

	def complete(self) -> TargetSelection:
		if (
			self._state
			!= TargetSelectionState.CONFIRMING
			or self._selection is None
		):
			raise TargetSelectionStateError(
				"Выбор цели ещё не завершён"
			)

		selection = self._selection
		self._reset()

		return selection

	def cancel(self) -> None:
		self._reset()

	def _reset(self) -> None:
		self._state = TargetSelectionState.IDLE

		self._character_id = None
		self._item = None
		self._allowed_target_types = ()
		self._selection = None