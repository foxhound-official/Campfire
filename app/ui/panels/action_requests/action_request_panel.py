from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QScrollArea,
	QVBoxLayout,
	QWidget,
)

from app.models.action_request import (
	ActionRequest,
	ActionType,
)
from app.models.campaign import Campaign
from app.systems.actions.action_processor import (
	ActionProcessor,
	ActionResult,
)
from app.systems.actions.action_request_queue import (
	ActionRequestQueue,
)
from app.theme.spacing import Spacing


class ActionRequestCard(QFrame):

	accepted = Signal(str)
	rejected = Signal(str)

	def __init__(
			self,
			request: ActionRequest,
			description: str,
			parent: QWidget | None = None,
	):
		super().__init__(parent)

		self.request_id = request.id

		self._build_ui(description)

	def _build_ui(
			self,
			description: str,
	) -> None:
		layout = QVBoxLayout(self)

		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		layout.setSpacing(Spacing.SM)

		description_label = QLabel(description)
		description_label.setWordWrap(True)

		button_layout = QHBoxLayout()
		button_layout.setSpacing(Spacing.SM)

		accept_button = QPushButton("Принять")
		reject_button = QPushButton("Отклонить")

		accept_button.clicked.connect(
			self._accept
		)
		reject_button.clicked.connect(
			self._reject
		)

		button_layout.addStretch()
		button_layout.addWidget(reject_button)
		button_layout.addWidget(accept_button)

		layout.addWidget(description_label)
		layout.addLayout(button_layout)

	def _accept(self) -> None:
		self.accepted.emit(self.request_id)

	def _reject(self) -> None:
		self.rejected.emit(self.request_id)


class ActionRequestPanel(QWidget):

	request_processed = Signal(object)

	def __init__(
			self,
			campaign: Campaign,
			request_queue: ActionRequestQueue,
			processor: ActionProcessor,
			parent: QWidget | None = None,
	):
		super().__init__(parent)

		self.campaign = campaign
		self.request_queue = request_queue
		self.processor = processor

		self._build_ui()
		self.refresh()

	def _build_ui(self) -> None:
		main_layout = QVBoxLayout(self)

		main_layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		main_layout.setSpacing(Spacing.MD)

		title_label = QLabel("Запросы игроков")

		self.status_label = QLabel()
		self.status_label.setWordWrap(True)
		self.status_label.hide()

		self.empty_label = QLabel(
			"Новых запросов нет"
		)

		self.request_container = QWidget()
		self.request_layout = QVBoxLayout(
			self.request_container
		)

		self.request_layout.setContentsMargins(
			0,
			0,
			0,
			0,
		)
		self.request_layout.setSpacing(Spacing.SM)
		self.request_layout.addStretch()

		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		scroll_area.setWidget(
			self.request_container
		)

		main_layout.addWidget(title_label)
		main_layout.addWidget(self.status_label)
		main_layout.addWidget(self.empty_label)
		main_layout.addWidget(scroll_area)

	def refresh(self) -> None:
		self._clear_requests()

		pending_requests = (
			self.request_queue.get_pending()
		)

		self.empty_label.setVisible(
			not pending_requests
		)

		for request in pending_requests:
			card = ActionRequestCard(
				request=request,
				description=(
					self._describe_request(request)
				),
			)

			card.accepted.connect(
				self._accept_request
			)
			card.rejected.connect(
				self._reject_request
			)

			self.request_layout.insertWidget(
				self.request_layout.count() - 1,
				card,
			)

	def _accept_request(
			self,
			request_id: str,
	) -> None:
		result = self.request_queue.accept(
			request_id,
			self.processor,
		)

		self._show_result(result)
		self.request_processed.emit(result)
		self.refresh()

	def _reject_request(
			self,
			request_id: str,
	) -> None:
		result = self.request_queue.reject(
			request_id
		)

		self._show_result(result)
		self.request_processed.emit(result)
		self.refresh()

	def _show_result(
			self,
			result: ActionResult,
	) -> None:
		self.status_label.setText(
			result.message
		)
		self.status_label.show()

	def _describe_request(
			self,
			request: ActionRequest,
	) -> str:
		character = self.campaign.find_character(
			request.character_id
		)
		target = self.campaign.find_character(
			request.target_id
		)

		character_name = (
			character.name
			if character is not None
			else "Неизвестный персонаж"
		)
		target_name = (
			target.name
			if target is not None
			else "Неизвестная цель"
		)

		if (
			request.action_type
			== ActionType.USE_ITEM
		):
			item_name = self._find_item_name(
				request
			)

			return (
				f"{character_name} хочет применить "
				f"«{item_name}» на {target_name}"
			)

		return (
			f"{character_name} отправляет "
			"неизвестный запрос"
		)

	def _find_item_name(
			self,
			request: ActionRequest,
	) -> str:
		character = self.campaign.find_character(
			request.character_id
		)

		if character is None:
			return "Неизвестный предмет"

		for item in character.inventory:
			if item.id == request.item_id:
				return item.name

		return "Неизвестный предмет"

	def _clear_requests(self) -> None:
		while self.request_layout.count() > 1:
			item = self.request_layout.takeAt(0)

			widget = item.widget()

			if widget is not None:
				widget.deleteLater()