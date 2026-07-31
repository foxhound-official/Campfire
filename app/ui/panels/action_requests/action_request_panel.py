from app.models.action_request import (
	ActionRequest,
	ActionRequestStatus,
)


class ActionRequestQueueError(Exception):
	pass


class ActionRequestQueue:

	def __init__(self):
		self._requests: dict[str, ActionRequest] = {}

	def submit(
			self,
			request: ActionRequest,
	) -> None:
		if request.id in self._requests:
			raise ActionRequestQueueError(
				"Запрос уже находится в очереди"
			)

		if (
			request.status
			is not ActionRequestStatus.PENDING
		):
			raise ActionRequestQueueError(
				"Отправить можно только ожидающий запрос"
			)

		if self.has_pending_item_request(
			character_id=request.character_id,
			item_id=request.item_id,
		):
			raise ActionRequestQueueError(
				"Запрос по этому предмету уже ожидает "
				"решения ведущего"
			)

		self._requests[request.id] = request

	def get_pending(
			self,
	) -> list[ActionRequest]:
		return [
			request
			for request in self._requests.values()
			if (
				request.status
				is ActionRequestStatus.PENDING
			)
		]

	def has_pending_item_request(
			self,
			character_id: str,
			item_id: str | None,
	) -> bool:
		return any(
			request.character_id == character_id
			and request.item_id == item_id
			and (
				request.status
				is ActionRequestStatus.PENDING
			)
			for request in self._requests.values()
		)