from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QProgressBar

from app.ui.widgets.cards.card import Card


class CreatureCard(Card):

	def __init__(
			self,
			name: str,
			current_health: int,
			maximum_health: int,
	):
		super().__init__()

		self.name_label = QLabel(name)
		self.name_label.setObjectName("cardTitle")
		self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.health_bar = QProgressBar()
		self.health_bar.setObjectName("cardHealth")
		self.health_bar.setRange(0, maximum_health)
		self.health_bar.setValue(current_health)
		self.health_bar.setFormat("%v / %m")

		self.content_layout.addWidget(self.name_label)
		self.content_layout.addWidget(self.health_bar)
