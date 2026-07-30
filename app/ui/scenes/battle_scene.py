from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout

from app.models.creature import Creature
from app.models.health import Health
from app.theme.spacing import Spacing
from app.ui.scenes.base_scene import BaseScene
from app.ui.widgets.cards import CreatureCard


class BattleScene(BaseScene):
	MAX_CREATURE_CARDS = 5

	def __init__(self):
		super().__init__("Поле боя")

		self.content_layout.addWidget(
			QLabel("Battle Scene"),
			alignment=Qt.AlignmentFlag.AlignCenter,
		)

		cards_layout = QHBoxLayout()
		cards_layout.setContentsMargins(0, 0, 0, 0)
		cards_layout.setSpacing(Spacing.MD)

		self.creature_cards: list[CreatureCard] = []

		self.creatures: list[Creature] = [
			Creature(
				name="Гоблин",
				health=Health(current=7, maximum=7, temporary=3),
			),
			Creature(
				name="Орк",
				health=Health(current=15, maximum=15),
			),
			Creature(
				name="Скелет",
				health=Health(current=9, maximum=13),
			),
			Creature(
				name="Волк",
				health=Health(current=8, maximum=11, temporary=3),
			),
			Creature(
				name="Культист",
				health=Health(current=6, maximum=9),
			),
		]

		cards_layout.addStretch()

		for creature in self.creatures[:self.MAX_CREATURE_CARDS]:
			card = CreatureCard(creature)

			self.creature_cards.append(card)
			cards_layout.addWidget(card)

		cards_layout.addStretch()

		self.content_layout.addStretch()
		self.content_layout.addLayout(cards_layout)
		self.content_layout.addStretch()
