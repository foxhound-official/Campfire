from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
	QFrame,
	QLabel,
	QScrollArea,
	QVBoxLayout,
	QWidget,
)

from app.models.character import Character
from app.theme.spacing import Spacing
from app.ui.panels.gm.character_card import (
	GMCharacterCard,
)


class ActiveCharactersPanel(QFrame):
	character_selected = Signal(str)

	def __init__(self):
		super().__init__()

		self._cards: dict[str, GMCharacterCard] = {}
		self._selected_character_id: str | None = None

		self.setObjectName("gmPanel")
		self._create_ui()

	def _create_ui(self) -> None:
		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		layout.setSpacing(Spacing.SM)

		title_label = QLabel("Активные персонажи")
		title_label.setObjectName("gmPanelTitle")

		self.empty_label = QLabel(
			"В кампании пока нет персонажей"
		)
		self.empty_label.setObjectName("gmPlaceholder")
		self.empty_label.setWordWrap(True)

		self.scroll_area = QScrollArea()
		self.scroll_area.setObjectName(
			"gmCharacterScroll"
		)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFrameShape(
			QFrame.Shape.NoFrame
		)

		self.cards_container = QWidget()
		self.cards_container.setObjectName(
			"gmCharacterList"
		)

		self.cards_layout = QVBoxLayout(
			self.cards_container
		)
		self.cards_layout.setContentsMargins(0, 0, 0, 0)
		self.cards_layout.setSpacing(Spacing.SM)
		self.cards_layout.addStretch()

		self.scroll_area.setWidget(
			self.cards_container
		)

		layout.addWidget(title_label)
		layout.addWidget(self.empty_label)
		layout.addWidget(self.scroll_area, 1)

	def set_characters(
			self,
			characters: list[Character],
			connected_character_ids: set[str] | None = None,
	) -> None:
		previous_selection = self._selected_character_id
		connected_ids = connected_character_ids or set()

		self._clear_cards()

		for character in characters:
			card = GMCharacterCard(
				character=character,
				connected=(
						character.id in connected_ids
				),
			)
			card.selected.connect(
				self.select_character
			)

			self._cards[character.id] = card

			self.cards_layout.insertWidget(
				self.cards_layout.count() - 1,
				card,
			)

		has_characters = bool(characters)

		self.empty_label.setVisible(
			not has_characters
		)
		self.scroll_area.setVisible(
			has_characters
		)

		selected_id = (
			previous_selection
			if previous_selection in self._cards
			else characters[0].id
			if characters
			else None
		)

		if selected_id is None:
			self._selected_character_id = None
			return

		self.select_character(selected_id)

	def select_character(
			self,
			character_id: str,
	) -> None:
		if character_id not in self._cards:
			return

		self._selected_character_id = character_id

		for card_id, card in self._cards.items():
			card.set_selected(
				card_id == character_id
			)

		self.character_selected.emit(
			character_id
		)

	def _clear_cards(self) -> None:
		while self.cards_layout.count() > 1:
			item = self.cards_layout.takeAt(0)
			widget = item.widget()

			if widget is not None:
				widget.deleteLater()

		self._cards.clear()
