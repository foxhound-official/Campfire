from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QProgressBar

from app.models.creature import Creature
from app.theme.images import CREATURE_PORTRAITS
from app.ui.widgets.cards.card import Card


class CreatureCard(Card):

	def __init__(
			self,
			creature: Creature
	):
		super().__init__()

		self.creature = creature
		self.name_label = QLabel()
		self.name_label.setObjectName("cardTitle")
		self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.health_bar = QProgressBar()
		self.health_bar.setObjectName("cardHealth")
		self.health_bar.setFormat("%v / %m")

		self.content_layout.addWidget(self.name_label)
		self.content_layout.addWidget(self.health_bar)

		self.refresh()

	def set_name(self, name: str) -> None:
		self.name_label.setText(name)

	def set_health(
			self,
			current_health: int,
			maximum_health: int,
			temporary_health: int = 0,
	) -> None:
		safe_maximum = max(1, maximum_health)
		safe_current = max(
			0,
			min(current_health, safe_maximum),
		)
		safe_temporary = max(0, temporary_health)

		self.health_bar.setRange(0, safe_maximum)
		self.health_bar.setValue(safe_current)

		if safe_temporary > 0:
			self.health_bar.setFormat(
				f"%v / %m (+{safe_temporary})"
			)
		else:
			self.health_bar.setFormat("%v / %m")

	def refresh(self) -> None:
		health = self.creature.health

		self.set_image(
			CREATURE_PORTRAITS,
			self.creature.portrait,
		)
		self.set_name(self.creature.name)
		self.set_health(
			current_health=health.current,
			maximum_health=health.maximum,
			temporary_health=health.temporary,
		)
