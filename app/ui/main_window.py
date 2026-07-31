from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QHBoxLayout,
	QMainWindow,
	QStackedWidget,
	QWidget, QGridLayout,
)

from app.models.campaign import Campaign
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.theme.sizes import Sizes
from app.ui.panels.character.character_panel import CharacterPanel
from app.ui.panels.inventory import InventoryPanel
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

		self.scene_views = {
			SceneType.BATTLE: self.battle_scene,
			SceneType.MERCHANT: self.merchant_scene,
			SceneType.NARRATION: self.narration_scene,
			SceneType.PUZZLE: self.puzzle_scene,
		}

		for scene_view in self.scene_views.values():
			self.scene_stack.addWidget(scene_view)

	def _create_ui(self) -> None:
		central = QWidget()

		layout = QHBoxLayout(central)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		self.character_panel = CharacterPanel()
		self.inventory_panel = InventoryPanel()

		scene_area = QWidget()

		scene_area_layout = QGridLayout(scene_area)
		scene_area_layout.setContentsMargins(0, 0, 0, 0)
		scene_area_layout.setSpacing(0)

		scene_area_layout.addWidget(
			self.scene_stack,
			0,
			0,
		)
		scene_area_layout.addWidget(
			self.inventory_panel,
			0,
			0,
			alignment=Qt.AlignmentFlag.AlignRight,
		)

		scene_area_layout.setAlignment(
			self.inventory_panel,
			Qt.AlignmentFlag.AlignRight,
		)

		layout.addWidget(self.character_panel)
		layout.addWidget(scene_area, 1)

		self.setCentralWidget(central)

	def refresh_campaign(self) -> None:
		self._show_scene(
			self.campaign.get_active_scene()
		)

		characters = self.campaign.characters

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
			self.inventory_panel.set_character(None)
			return

		self.active_character_id = active_character.id

		self.character_panel.set_character(
			active_character
		)
		self.inventory_panel.set_character(
			active_character
		)

	def set_scene(
			self,
			scene_id: str,
	) -> None:
		scene_data = self.campaign.set_active_scene(
			scene_id
		)

		self._show_scene(scene_data)

	def _show_scene(
			self,
			scene_data: SceneData,
	) -> None:
		scene_view = self.scene_views[
			scene_data.scene_type
		]

		scene_view.set_scene(scene_data)

		self.scene_stack.setCurrentWidget(
			scene_view
		)