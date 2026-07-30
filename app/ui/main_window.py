from PySide6.QtWidgets import (
	QHBoxLayout,
	QMainWindow,
	QStackedWidget,
	QWidget,
)

from app.models.campaign import Campaign
from app.models.scene_type import SceneType
from app.theme.sizes import Sizes
from app.ui.panels.character.character_panel import CharacterPanel
from app.ui.scenes import (
	BattleScene,
	MerchantScene,
	NarrationScene,
	PuzzleScene,
)


class MainWindow(QMainWindow):

	def __init__(
			self,
			campaign: Campaign | None = None,
			active_character_id: str | None = None,
	):
		super().__init__()

		self.campaign = (
			campaign
			if campaign is not None
			else Campaign()
		)
		self.active_character_id = active_character_id

		self.setWindowTitle("Campfire")
		self.resize(
			Sizes.WINDOW_WIDTH,
			Sizes.WINDOW_HEIGHT,
		)

		self._create_scenes()
		self._create_ui()
		self.refresh_campaign()

	def _create_scenes(self) -> None:
		self.scene_stack = QStackedWidget()

		self.battle_scene = BattleScene()
		self.merchant_scene = MerchantScene()
		self.narration_scene = NarrationScene()
		self.puzzle_scene = PuzzleScene()

		self.scenes = {
			SceneType.BATTLE: self.battle_scene,
			SceneType.MERCHANT: self.merchant_scene,
			SceneType.NARRATION: self.narration_scene,
			SceneType.PUZZLE: self.puzzle_scene,
		}

		for scene in self.scenes.values():
			self.scene_stack.addWidget(scene)

	def _create_ui(self) -> None:
		central = QWidget()

		layout = QHBoxLayout(central)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		self.character_panel = CharacterPanel()

		layout.addWidget(self.character_panel)
		layout.addWidget(self.scene_stack, 1)

		self.setCentralWidget(central)

	def refresh_campaign(self) -> None:
		self.set_scene(
			self.campaign.active_scene
		)

		characters = self.campaign.characters

		self.battle_scene.set_creatures(
			self.campaign.creatures
		)

		self.character_panel.set_party(characters)

		active_character = (
			self.campaign.find_character(
				self.active_character_id
			)
		)

		if active_character is None and characters:
			active_character = characters[0]

		if active_character is None:
			self.active_character_id = None
			return

		self.active_character_id = active_character.id

		self.character_panel.set_character(
			active_character
		)

	def set_scene(
			self,
			scene_type: SceneType,
	) -> None:
		self.campaign.active_scene = scene_type

		self.scene_stack.setCurrentWidget(
			self.scenes[scene_type]
		)
