from dataclasses import dataclass

from app.models.action_request import (
	ActionRequest,
	ActionRequestStatus,
	ActionType,
)
from app.models.campaign import Campaign
from app.models.character import Character
from app.models.item import (
	Item,
	ItemUseEffect,
)
from app.systems.combat.combat_system import (
	CombatSystem,
)


class ActionExecutionError(Exception):
	pass


@dataclass(frozen=True, slots=True)
class ActionResult:
	request_id: str
	status: ActionRequestStatus
	message: str
	applied_value: int = 0


class ActionProcessor:

	def __init__(
			self,
			campaign: Campaign,
	):
		self.campaign = campaign
		self.combat_system = CombatSystem(campaign)

	def set_campaign(
			self,
			campaign: Campaign,
	) -> None:
		self.campaign = campaign
		self.combat_system.set_campaign(campaign)

	def process(
			self,
			request: ActionRequest,
	) -> ActionResult:
		if (
			request.status
			!= ActionRequestStatus.PENDING
		):
			raise ActionExecutionError(
				"Можно выполнить только ожидающий запрос"
			)

		try:
			if request.action_type == ActionType.USE_ITEM:
				applied_value, message = (
					self._use_item(request)
				)
			else:
				raise ActionExecutionError(
					"Неподдерживаемый тип действия: "
					f"{request.action_type}"
				)

		except ActionExecutionError as error:
			request.status = (
				ActionRequestStatus.FAILED
			)
			request.status_message = str(error)

			return ActionResult(
				request_id=request.id,
				status=request.status,
				message=request.status_message,
			)

		request.status = ActionRequestStatus.ACCEPTED
		request.status_message = message

		return ActionResult(
			request_id=request.id,
			status=request.status,
			message=message,
			applied_value=applied_value,
		)

	def _use_item(
			self,
			request: ActionRequest,
	) -> tuple[int, str]:
		character = self._get_character(
			request.character_id
		)

		if request.item_id is None:
			raise ActionExecutionError(
				"В запросе не указан предмет"
			)

		item = self._get_item(
			character,
			request.item_id,
		)

		if item.quantity <= 0:
			raise ActionExecutionError(
				"Предмет закончился"
			)

		if request.target_id is None:
			raise ActionExecutionError(
				"В запросе не указана цель"
			)

		target = self._get_character(
			request.target_id
		)

		if item.use_effect == ItemUseEffect.HEAL:
			applied_value = self._apply_healing(
				item,
				target,
			)
		else:
			raise ActionExecutionError(
				"Этот предмет нельзя применить"
			)

		item.quantity -= 1

		if item.quantity == 0:
			character.inventory.remove(item)

		return (
			applied_value,
			(
				f"{character.name} применяет "
				f"«{item.name}» на {target.name}. "
				f"Восстановлено здоровья: "
				f"{applied_value}"
			),
		)

	def _apply_healing(
			self,
			item: Item,
			target: Character,
	) -> int:
		if item.effect_value <= 0:
			raise ActionExecutionError(
				"Предмет не содержит лечения"
			)

		if (
			target.health.current
			>= target.health.maximum
		):
			raise ActionExecutionError(
				"У цели уже максимальное здоровье"
			)

		restored_health = (
			self.combat_system.heal_character(
				target.id,
				item.effect_value,
			)
		)

		if restored_health <= 0:
			raise ActionExecutionError(
				"Не удалось восстановить здоровье"
			)

		return restored_health

	def _get_character(
			self,
			character_id: str,
	) -> Character:
		character = self.campaign.find_character(
			character_id
		)

		if character is None:
			raise ActionExecutionError(
				"Персонаж отсутствует в кампании: "
				f"{character_id}"
			)

		return character

	def _get_item(
			self,
			character: Character,
			item_id: str,
	) -> Item:
		for item in character.inventory:
			if item.id == item_id:
				return item

		raise ActionExecutionError(
			f"Предмет отсутствует у {character.name}"
		)