from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout

from app.ui.scenes.base_scene import BaseScene
from app.ui.widgets.cards import CreatureCard


class BattleScene(BaseScene):

	def __init__(self):
		super().__init__("Поле боя")

		self.content_layout.addWidget(
			QLabel("Battle Scene"),
			alignment=Qt.AlignmentFlag.AlignCenter,
		)

		cards_layout = QHBoxLayout()

		creatures = [
			("Гоблин", 7, 7),
			("Орк", 15, 15),
			("Скелет", 9, 13),
			("Волк", 8, 11),
			("Культист", 6, 9),
		]

		for name, current_health, maximum_health in creatures:
			card = CreatureCard(
				name=name,
				current_health=current_health,
				maximum_health=maximum_health,
			)

			cards_layout.addWidget(card)

		cards_layout.addStretch()

		self.content_layout.addLayout(cards_layout)
