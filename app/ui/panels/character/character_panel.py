from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFrame,
	QLabel,
	QVBoxLayout,
)

from app.theme.colors import Colors
from app.theme.spacing import Spacing

from app.widgets.card import Card
from app.widgets.label import TitleLabel
from app.widgets.info_card import InfoCard


class CharacterPanel(QFrame):
	def __init__(self):
		super().__init__()

		self.setStyleSheet(
			f"""
			background-color: {Colors.PANEL};
			"""
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.XXS,
			Spacing.XXS,
			Spacing.XXS,
			Spacing.XXS
		)
		layout.setSpacing(Spacing.SXS)
		layout.setAlignment(Qt.AlignmentFlag.AlignTop)

		self.character_card = Card()

		self.character_card.layout.addWidget(
			InfoCard("❤️ Здоровье", "84 / 100")
		)

		self.character_card.layout.addWidget(
			InfoCard("🛡 Броня", "16")
		)

		self.character_card.layout.addWidget(
			InfoCard("⚡ Инициатива", "+3")
		)

		self.character_card.layout.addWidget(
			InfoCard("🏃 Скорость", "30 футов")
		)

		layout.addWidget(self.character_card)