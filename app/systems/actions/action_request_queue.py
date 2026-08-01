from app.models.action_request import (
	ActionRequest,
	ActionRequestStatus,
)
from app.systems.actions.action_processor import (
	ActionProcessor,
	ActionResult,
)


class ActionRequestQueueError(Exception):
	pass


class ActionRequestNotFoundError(
	ActionRequestQueueError
):
	pass


class ActionRequestStateError(
	ActionRequestQueueError
):
	pass


class ActionRequestQueue:

	def __init__(self):
		self._requests: dict[
			str,
			ActionRequest,
		] = {}

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
				!= ActionRequestStatus.PENDING
		):
			raise ActionRequestStateError(
				"В очередь можно добавить только "
				"ожидающий запрос"
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

	def get(
			self,
			request_id: str,
	) -> ActionRequest:
		request = self._requests.get(request_id)

		if request is None:
			raise ActionRequestNotFoundError(
				"Запрос не найден: "
				f"{request_id}"
			)

		return request

	def get_pending(
			self,
	) -> list[ActionRequest]:
		return [
			request
			for request in self._requests.values()
			if (
					request.status
					== ActionRequestStatus.PENDING
			)
		]

	def accept(
			self,
			request_id: str,
			processor: ActionProcessor,
	) -> ActionResult:
		request = self._get_pending(
			request_id
		)

		return processor.process(request)

	def reject(
			self,
			request_id: str,
			message: str = "Запрос отклонён ведущим",
	) -> ActionResult:
		request = self._get_pending(
			request_id
		)

		request.status = ActionRequestStatus.REJECTED
		request.status_message = message

		return ActionResult(
			request_id=request.id,
			status=request.status,
			message=message,
		)

	def _get_pending(
			self,
			request_id: str,
	) -> ActionRequest:
		request = self.get(request_id)

		if (
				request.status
				!= ActionRequestStatus.PENDING
		):
			raise ActionRequestStateError(
				"Запрос уже обработан: "
				f"{request_id}"
			)

		return request

	def has_pending_item_request(
			self,
			character_id: str,
			item_id: str | None,
	) -> bool:
		if item_id is None:
			return False

		return any(
			request.character_id == character_id
			and request.item_id == item_id
			and (
					request.status
					== ActionRequestStatus.PENDING
			)
			for request in self._requests.values()
		)
