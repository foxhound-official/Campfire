from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
	QHBoxLayout,
	QMainWindow,
	QStackedWidget,
	QWidget, QGridLayout,
	QDialog, QMessageBox
)

from app.core.music_player import MusicPlayer
from app.core.sound_player import SoundPlayer
from app.models.action_target_type import ActionTargetType
from app.models.campaign import Campaign
from app.models.item import Item
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.systems.actions.action_request_queue import (
	ActionRequestQueue,
	ActionRequestQueueError,
)
from app.theme.sizes import Sizes
from app.models.action_request import (
	ActionRequest,
	ActionType,
)
from app.ui.controllers.target_selection_controller import TargetSelectionController, TargetSelectionError
from app.ui.panels.character.character_panel import CharacterPanel
from app.ui.panels.inventory import InventoryPanel
from app.ui.dialogs import ActionConfirmationDialog
from app.ui.scenes import (
	BattleScene,
	MerchantScene,
	NarrationScene,
	PuzzleScene,
)
from app.ui.widgets.target_selection_prompt import TargetSelectionPrompt


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
		self.music_player = MusicPlayer(self)
		self.sound_player = SoundPlayer(self)
		self.target_selection = TargetSelectionController()
		self.action_request_queue = ActionRequestQueue()
		self._active_action_item: Item | None = None

		self.setWindowTitle("Campfire")
		self.resize(
			Sizes.WINDOW_WIDTH,
			Sizes.WINDOW_HEIGHT,
		)
		self._create_scenes()
		self._create_ui()
		self._connect_target_selection()
		self._configure_sounds()
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
		self.target_prompt = TargetSelectionPrompt()

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

		scene_area_layout.addWidget(
			self.target_prompt,
			0,
			0,
			alignment=(
					Qt.AlignmentFlag.AlignHCenter
					| Qt.AlignmentFlag.AlignBottom
			),
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

		self.music_player.play(
			scene_data.music
		)

	def _configure_sounds(self) -> None:
		self.sound_player.register(
			"button_click",
			"app/assets/sounds/button_click.wav",
			volume=0.35,
		)
		self.sound_player.register(
			"inventory_open",
			"app/assets/sounds/inventory_open.wav",
			volume=0.55,
		)
		self.sound_player.register(
			"inventory_close",
			"app/assets/sounds/inventory_close.wav",
			volume=0.55,
		)

		self.inventory_panel.expanded_changed.connect(
			self._play_inventory_sound
		)

	def _play_inventory_sound(
			self,
			expanded: bool,
	) -> None:
		sound_name = (
			"inventory_open"
			if expanded
			else "inventory_close"
		)

		print("sound played:" + sound_name)

		self.sound_player.play(sound_name)

	def _connect_target_selection(self) -> None:
		self.character_panel.party_member_selected.connect(
			lambda character_id: self._select_target(
				ActionTargetType.CHARACTER,
				character_id,
			)
		)

		self.battle_scene.creature_selected.connect(
			lambda creature_id: self._select_target(
				ActionTargetType.CREATURE,
				creature_id,
			)
		)

		self.inventory_panel.item_activated.connect(
			self._activate_inventory_item
		)

		self.cancel_target_selection_shortcut = QShortcut(
			QKeySequence("Escape"),
			self,
		)

		self.cancel_target_selection_shortcut.activated.connect(
			self.cancel_target_selection
		)

		self.target_prompt.cancelled.connect(
			self.cancel_target_selection
		)

	def start_item_target_selection(
			self,
			item: Item,
	) -> None:
		if self.active_character_id is None:
			return

		if self.target_selection.is_active:
			self.target_selection.cancel()

		try:
			self.target_selection.start(
				character_id=self.active_character_id,
				item=item,
			)

		except TargetSelectionError as error:
			print("Не удалось начать выбор цели:", error)
			return

		self._active_action_item = item

		self.inventory_panel.set_expanded(False)

		self.target_prompt.show_for_item(
			item.name
		)

		self._update_target_selection_ui()

	def cancel_target_selection(self) -> None:
		self.target_selection.cancel()
		self._active_action_item = None
		self.target_prompt.hide()
		self._update_target_selection_ui()

	def _select_target(
			self,
			target_type: ActionTargetType,
			target_id: str,
	) -> None:
		if not self.target_selection.can_select(
				target_type
		):
			return

		target_name = self._get_target_name(
			target_type,
			target_id,
		)

		if target_name is None:
			return

		try:
			selection = (
				self.target_selection.select_target(
					target_type=target_type,
					target_id=target_id,
				)
			)

		except TargetSelectionError as error:
			print(
				"Не удалось выбрать цель:",
				error,
			)
			return

		self.target_prompt.hide()
		self._update_target_selection_ui()

		character = self.campaign.find_character(
			self.active_character_id
		)
		item = self._active_action_item

		if character is None or item is None:
			self.cancel_target_selection()
			return

		dialog = ActionConfirmationDialog(
			character_name=character.name,
			item_name=item.name,
			target_name=target_name,
			parent=self,
		)

		result = dialog.exec()

		if result != QDialog.DialogCode.Accepted:
			self.cancel_target_selection()
			return

		request = ActionRequest(
			action_type=ActionType.USE_ITEM,
			character_id=character.id,
			item_id=item.id,
			target_type=selection.target_type,
			target_id=selection.target_id,
		)

		try:
			self.action_request_queue.submit(request)

		except ActionRequestQueueError as error:
			self.cancel_target_selection()

			QMessageBox.warning(
				self,
				"Не удалось отправить запрос",
				str(error),
			)
			return

		self.cancel_target_selection()

		self.target_prompt.show_status(
			"Запрос отправлен ведущему"
		)

		QTimer.singleShot(
			2200,
			self._hide_request_status,
		)

		print(
			"Запрос отправлен:",
			request.id,
			request.status.value,
		)

	def _update_target_selection_ui(self) -> None:
		self.character_panel.set_character_targets_enabled(
			self.target_selection.can_select(
				ActionTargetType.CHARACTER
			)
		)

		self.battle_scene.set_creature_targets_enabled(
			self.target_selection.can_select(
				ActionTargetType.CREATURE
			)
		)

	def _activate_inventory_item(
			self,
			item_id: str,
	) -> None:
		character = self.campaign.find_character(
			self.active_character_id
		)

		if character is None:
			return

		item = next(
			(
				item
				for item in character.inventory
				if item.id == item_id
			),
			None,
		)

		if item is None:
			return

		self.start_item_target_selection(item)

	def _get_target_name(
			self,
			target_type: ActionTargetType,
			target_id: str,
	) -> str | None:
		if target_type is ActionTargetType.CHARACTER:
			character = self.campaign.find_character(
				target_id
			)

			return (
				character.name
				if character is not None
				else None
			)

		if target_type is ActionTargetType.CREATURE:
			scene = self.campaign.get_active_scene()

			creature = scene.find_creature(
				target_id
			)

			return (
				creature.name
				if creature is not None
				else None
			)

		return None

	def _hide_request_status(self) -> None:
		if not self.target_selection.is_active:
			self.target_prompt.hide()
