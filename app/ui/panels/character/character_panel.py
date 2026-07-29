from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout

from app.models.character import Character
from app.theme.colors import Colors
from app.theme.spacing import Spacing
from app.ui.widgets.card import Card
from app.ui.widgets.info_card import InfoCard
from app.ui.widgets.label import CaptionLabel, TitleLabel


class CharacterPanel(QFrame):
	def __init__(self, character: Character):
		super().__init__()

		self.setObjectName("CharacterPanel")
		self.setMinimumWidth(280)
		self.setMaximumWidth(360)

		self.setStyleSheet(
			f"""
            QFrame#CharacterPanel {{
                background-color: {Colors.WINDOW};
            }}
            """
		)

		main_layout = QVBoxLayout(self)
		main_layout.setContentsMargins(
			Spacing.XXS,
			Spacing.XXS,
			Spacing.XXS,
			Spacing.XXS,
		)
		main_layout.setSpacing(Spacing.SXS)
		main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		self.character_card = Card()

		self.name_label = TitleLabel("")
		self.details_label = CaptionLabel("")

		self.health_card = InfoCard("❤️ Здоровье", "")
		self.armor_card = InfoCard("🛡 Броня", "")
		self.initiative_card = InfoCard("⚡ Инициатива", "")

		self.character_card.content_layout.addWidget(self.name_label)
		self.character_card.content_layout.addWidget(self.details_label)
		self.character_card.content_layout.addSpacing(Spacing.S)

		self.character_card.content_layout.addWidget(self.health_card)
		self.character_card.content_layout.addWidget(self.armor_card)
		self.character_card.content_layout.addWidget(
			self.initiative_card
		)

		main_layout.addWidget(self.character_card)

		self.set_character(character)

	def set_character(self, character: Character) -> None:
		self.character = character

		self.name_label.setText(character.name)

		self.details_label.setText(
			f"{character.character_class} · "
			f"{character.level} уровень"
		)

		self.health_card.set_value(
			f"{character.current_hp} / {character.max_hp}"
		)

		self.armor_card.set_value(str(character.armor_class))

		initiative_prefix = "+" if character.initiative >= 0 else ""
		self.initiative_card.set_value(
			f"{initiative_prefix}{character.initiative}"
		)