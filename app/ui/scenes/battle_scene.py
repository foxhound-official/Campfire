from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout

from app.models.creature import Creature
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.theme.spacing import Spacing
from app.ui.scenes.base_scene import BaseScene
from app.ui.widgets.cards import CreatureCard


class BattleScene(BaseScene):
	MAX_CREATURE_CARDS = 5

	def __init__(self):
		super().__init__("Поле боя")

		self.cards_layout = QHBoxLayout()
		self.cards_layout.setContentsMargins(0, 0, 0, 0)
		self.cards_layout.setSpacing(Spacing.MD)
		self.cards_layout.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		self.creature_cards: list[CreatureCard] = []

		self.content_layout.addStretch()
		self.content_layout.addLayout(self.cards_layout)
		self.content_layout.addStretch()

	def set_scene(
			self,
			scene_data: SceneData,
	) -> None:
		if scene_data.scene_type is not SceneType.BATTLE:
			raise ValueError(
				"BattleScene принимает только боевые сцены"
			)

		super().set_scene(scene_data)

		self.set_creatures(
			scene_data.creatures
		)

	def set_creatures(
			self,
			creatures: list[Creature],
	) -> None:
		self._clear_creature_cards()

		for creature in creatures[
				:self.MAX_CREATURE_CARDS
		]:
			card = CreatureCard(creature)

			self.creature_cards.append(card)
			self.cards_layout.addWidget(card)

	def _clear_creature_cards(self) -> None:
		for card in self.creature_cards:
			self.cards_layout.removeWidget(card)
			card.deleteLater()

		self.creature_cards.clear()