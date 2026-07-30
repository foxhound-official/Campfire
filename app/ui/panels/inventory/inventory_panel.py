from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QScrollArea,
	QSizePolicy,
	QVBoxLayout,
	QWidget,
)

from app.models.character import Character
from app.theme.sizes import Sizes
from app.theme.spacing import Spacing
from app.ui.widgets.cards import ItemCard


class InventoryPanel(QFrame):
	ANIMATION_DURATION = 550

	def __init__(self):
		super().__init__()

		self.character: Character | None = None
		self.is_expanded = False

		self.setObjectName("inventoryPanel")
		self.setSizePolicy(
			QSizePolicy.Policy.Fixed,
			QSizePolicy.Policy.Expanding,
		)

		self._create_ui()
		self._create_animation()

		self.setMinimumWidth(
			Sizes.INVENTORY_HANDLE_WIDTH
		)
		self.setMaximumWidth(
			Sizes.INVENTORY_HANDLE_WIDTH
			+ Sizes.INVENTORY_PANEL_WIDTH
		)

		self._update_toggle_button()

	def _create_ui(self) -> None:
		layout = QHBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		self.toggle_button = QPushButton("‹")
		self.toggle_button.setObjectName(
			"inventoryHandle"
		)
		self.toggle_button.setFixedSize(
			Sizes.INVENTORY_HANDLE_WIDTH,
			Sizes.INVENTORY_HANDLE_HEIGHT,
		)
		self.toggle_button.setCursor(
			Qt.CursorShape.PointingHandCursor
		)
		self.toggle_button.clicked.connect(
			self.toggle
		)

		self.content = QFrame()
		self.content.setObjectName("inventoryContent")
		self.content.setMinimumWidth(0)
		self.content.setMaximumWidth(0)

		content_layout = QVBoxLayout(self.content)
		content_layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		content_layout.setSpacing(Spacing.MD)

		self.title_label = QLabel("Инвентарь")
		self.title_label.setObjectName(
			"inventoryTitle"
		)

		self.capacity_label = QLabel()
		self.capacity_label.setObjectName(
			"inventoryCapacity"
		)

		self.scroll_area = QScrollArea()
		self.scroll_area.setMinimumWidth(
			Sizes.CARD_WIDTH
		)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFrameShape(
			QFrame.Shape.NoFrame
		)
		self.scroll_area.setHorizontalScrollBarPolicy(
			Qt.ScrollBarPolicy.ScrollBarAlwaysOff
		)

		self.items_container = QWidget()
		self.items_layout = QVBoxLayout(
			self.items_container
		)
		self.items_layout.setContentsMargins(
			0,
			0,
			0,
			0,
		)
		self.items_layout.setSpacing(Spacing.MD)
		self.items_layout.setAlignment(
			Qt.AlignmentFlag.AlignTop
			| Qt.AlignmentFlag.AlignHCenter
		)

		self.scroll_area.setWidget(
			self.items_container
		)

		content_layout.addWidget(self.title_label)
		content_layout.addWidget(self.capacity_label)
		content_layout.addWidget(
			self.scroll_area,
			1,
		)

		layout.addWidget(
			self.toggle_button,
			alignment=Qt.AlignmentFlag.AlignTop,
		)
		layout.addWidget(self.content)

	def set_character(
			self,
			character: Character | None,
	) -> None:
		self.character = character
		self.refresh()

	def refresh(self) -> None:
		self._clear_items()

		if self.character is None:
			self.title_label.setText("Инвентарь")
			self.capacity_label.setText("0 / 0")
			return

		self.title_label.setText(
			f"Инвентарь — {self.character.name}"
		)
		self.capacity_label.setText(
			f"{len(self.character.inventory)}"
			f" / {self.character.inventory_capacity}"
		)

		for item in self.character.inventory:
			self.items_layout.addWidget(
				ItemCard(item)
			)

	def toggle(self) -> None:
		self.set_expanded(
			not self.is_expanded
		)

	def _clear_items(self) -> None:
		while self.items_layout.count():
			item = self.items_layout.takeAt(0)
			widget = item.widget()

			if widget is not None:
				widget.deleteLater()

	def _create_animation(self) -> None:
		self.width_animation = QPropertyAnimation(
			self.content,
			b"maximumWidth",
			self,
		)
		self.width_animation.setDuration(
			self.ANIMATION_DURATION
		)
		self.width_animation.setEasingCurve(
			QEasingCurve.Type.OutCubic
		)

	def set_expanded(
			self,
			expanded: bool,
	) -> None:
		if self.is_expanded == expanded:
			return

		self.is_expanded = expanded
		self.width_animation.stop()

		start_width = self.content.maximumWidth()
		end_width = (
			Sizes.INVENTORY_PANEL_WIDTH
			if expanded
			else 0
		)

		self._update_toggle_button()

		self.width_animation.setStartValue(
			start_width
		)
		self.width_animation.setEndValue(
			end_width
		)
		self.width_animation.start()

	def _update_toggle_button(self) -> None:
		self.toggle_button.setText(
			"›" if self.is_expanded else "‹"
		)
