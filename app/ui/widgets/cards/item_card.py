from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QLabel

from app.models.item import Item
from app.theme.images import ITEM_IMAGES
from app.ui.widgets.cards.card import Card


class ItemCard(Card):
	activated = Signal(str)

	def __init__(self, item: Item):
		super().__init__()

		self.item = item

		self._action_enabled = (
				item.quantity > 0
				and bool(item.target_types)
		)

		self.setCursor(
			Qt.CursorShape.PointingHandCursor
			if self._action_enabled
			else Qt.CursorShape.ArrowCursor
		)

		self.set_image(
			ITEM_IMAGES,
			self.item.image_name,
		)

		self.title_label = QLabel(item.name)
		self.title_label.setObjectName("cardTitle")
		self.title_label.setWordWrap(True)

		self.description_label = QLabel(
			item.description or "Нет описания"
		)
		self.description_label.setObjectName(
			"cardDescription"
		)
		self.description_label.setWordWrap(True)

		self.quantity_label = QLabel(
			f"Количество: {item.quantity}"
		)
		self.quantity_label.setObjectName(
			"itemQuantity"
		)
		self.quantity_label.setVisible(
			item.quantity > 1
		)

		for widget in (
				self.image,
				self.title_label,
				self.description_label,
				self.quantity_label,
		):
			widget.setAttribute(
				Qt.WidgetAttribute.WA_TransparentForMouseEvents,
				True,
			)

		self.content_layout.addWidget(
			self.title_label
		)
		self.content_layout.addWidget(
			self.description_label
		)
		self.content_layout.addWidget(
			self.quantity_label
		)

	def mouseReleaseEvent(
			self,
			event: QMouseEvent,
	) -> None:
		if (
				self._action_enabled
				and event.button()
				is Qt.MouseButton.LeftButton
		):
			self.activated.emit(self.item.id)
			event.accept()
			return

		super().mouseReleaseEvent(event)