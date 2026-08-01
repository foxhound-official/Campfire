from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QMainWindow,
	QPushButton,
	QSplitter,
	QTabWidget,
	QVBoxLayout,
	QWidget,
)

from app.models.campaign import Campaign
from app.systems.actions.action_processor import ActionProcessor
from app.systems.actions.action_request_queue import (
	ActionRequestQueue,
)
from app.theme.spacing import Spacing
from app.ui.panels.gm import (
	ActiveCharactersPanel,
	CharacterInspector,
	SceneControlPanel,
)
from gm import ActiveCreaturesPanel


class GMWindow(QMainWindow):
	request_processed = Signal(object)

	def __init__(
			self,
			campaign: Campaign | None = None,
			action_request_queue: ActionRequestQueue | None = None,
	):
		super().__init__()

		self.campaign = (
			campaign
			if campaign is not None
			else Campaign()
		)
		self.action_request_queue = (
			action_request_queue
			if action_request_queue is not None
			else ActionRequestQueue()
		)
		self.action_processor = ActionProcessor(
			self.campaign
		)

		self.setWindowTitle("Campfire — Ведущий")
		self.resize(1600, 950)
		self.setMinimumSize(1200, 760)

		self._create_ui()
		self.refresh_campaign()

	def _create_ui(self) -> None:
		main_tabs = QTabWidget()
		main_tabs.setObjectName("gmMainTabs")

		main_tabs.addTab(
			self._create_session_page(),
			"Сессия",
		)
		main_tabs.addTab(
			self._create_empty_page(
				"Конструкторы",
				"Здесь будут конструкторы сцен, "
				"персонажей, существ и предметов.",
			),
			"Конструкторы",
		)
		main_tabs.addTab(
			self._create_empty_page(
				"Кампании",
				"Здесь будет создание, загрузка "
				"и настройка кампаний.",
			),
			"Кампании",
		)

		self.setCentralWidget(main_tabs)

	def _create_session_page(self) -> QWidget:
		page = QWidget()

		page_layout = QVBoxLayout(page)
		page_layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		page_layout.setSpacing(Spacing.SM)

		page_layout.addWidget(
			self._create_toolbar()
		)

		vertical_splitter = QSplitter(
			Qt.Orientation.Vertical
		)

		workspace_splitter = self._create_workspace()
		bottom_tabs = self._create_bottom_tabs()

		vertical_splitter.addWidget(
			workspace_splitter
		)
		vertical_splitter.addWidget(bottom_tabs)
		vertical_splitter.setSizes([650, 220])
		vertical_splitter.setStretchFactor(0, 1)
		vertical_splitter.setStretchFactor(1, 0)

		page_layout.addWidget(vertical_splitter)

		return page

	def _create_toolbar(self) -> QFrame:
		toolbar = QFrame()
		toolbar.setObjectName("gmToolbar")

		layout = QHBoxLayout(toolbar)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.SM,
			Spacing.MD,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.SM)

		self.campaign_label = QLabel()
		self.campaign_label.setObjectName(
			"gmAppTitle"
		)

		self.scene_label = QLabel()
		self.scene_label.setObjectName(
			"gmSceneName"
		)

		load_button = QPushButton("Загрузить")
		save_button = QPushButton("Сохранить")
		save_button.setObjectName(
			"gmPrimaryButton"
		)

		layout.addWidget(self.campaign_label)
		layout.addWidget(self.scene_label)
		layout.addStretch()
		layout.addWidget(load_button)
		layout.addWidget(save_button)

		return toolbar

	def _create_workspace(self) -> QSplitter:
		workspace = QSplitter(
			Qt.Orientation.Horizontal
		)

		self.characters_panel = (
			ActiveCharactersPanel()
		)
		self.characters_panel.character_selected.connect(
			self._select_character
		)

		scene_area = QSplitter(
			Qt.Orientation.Vertical
		)

		self.scene_control_panel = (
			SceneControlPanel()
		)
		self.scene_control_panel.scene_activation_requested.connect(
			self._activate_scene
		)
		scene_area.addWidget(
			self.scene_control_panel
		)

		self.creatures_panel = ActiveCreaturesPanel()
		scene_area.addWidget(
			self.creatures_panel
		)

		scene_area.setSizes([480, 190])
		scene_area.setStretchFactor(0, 1)
		scene_area.setStretchFactor(1, 0)

		self.inspector = CharacterInspector()

		workspace.addWidget(
			self.characters_panel
		)
		workspace.addWidget(scene_area)
		workspace.addWidget(self.inspector)

		workspace.setSizes([310, 820, 420])
		workspace.setStretchFactor(0, 0)
		workspace.setStretchFactor(1, 1)
		workspace.setStretchFactor(2, 0)

		return workspace

	def _create_bottom_tabs(self) -> QTabWidget:
		tabs = QTabWidget()
		tabs.setObjectName("gmBottomTabs")

		tabs.addTab(
			self._create_tab_placeholder(
				"Активных запросов пока нет"
			),
			"Запросы",
		)
		tabs.addTab(
			self._create_tab_placeholder(
				"Активных запросов на бросок нет"
			),
			"Проверки",
		)
		tabs.addTab(
			self._create_tab_placeholder(
				"Здесь появятся секретные сообщения"
			),
			"Сообщения",
		)
		tabs.addTab(
			self._create_tab_placeholder(
				"Журнал игровой сессии пока пуст"
			),
			"Журнал",
		)
		tabs.addTab(
			self._create_tab_placeholder(
				"Здесь будет управление звуками"
			),
			"Звуки",
		)

		return tabs

	def refresh_campaign(self) -> None:
		self.campaign_label.setText(
			self.campaign.name
			or "Кампания без названия"
		)

		active_scene = (
			self.campaign.get_active_scene()
		)

		self.scene_label.setText(
			"Текущая сцена: "
			f"{active_scene.title or '—'}"
		)

		self.scene_control_panel.set_scenes(
			self.campaign.scenes,
			self.campaign.active_scene_id,
		)

		self.creatures_panel.set_scene(
			active_scene
		)

		self.inspector.clear()

		self.characters_panel.set_characters(
			self.campaign.characters
		)

	def _activate_scene(
			self,
			scene_id: str,
	) -> None:
		self.campaign.set_active_scene(scene_id)
		self.refresh_campaign()

	def _select_character(
			self,
			character_id: str,
	) -> None:
		character = self.campaign.find_character(
			character_id
		)

		if character is None:
			self.inspector.clear()
			return

		self.inspector.set_character(character)

	def _create_panel(
			self,
			title: str,
			description: str,
	) -> QFrame:
		panel = QFrame()
		panel.setObjectName("gmPanel")

		layout = QVBoxLayout(panel)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		layout.setSpacing(Spacing.SM)

		title_label = QLabel(title)
		title_label.setObjectName(
			"gmPanelTitle"
		)

		description_label = QLabel(
			description
		)
		description_label.setObjectName(
			"gmPlaceholder"
		)
		description_label.setWordWrap(True)
		description_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		layout.addWidget(title_label)
		layout.addWidget(
			description_label,
			1,
		)

		return panel

	def _create_tab_placeholder(
			self,
			text: str,
	) -> QWidget:
		page = QWidget()

		layout = QVBoxLayout(page)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)

		label = QLabel(text)
		label.setObjectName("gmPlaceholder")
		label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		layout.addWidget(label)

		return page

	def _create_empty_page(
			self,
			title: str,
			description: str,
	) -> QWidget:
		page = QWidget()

		layout = QVBoxLayout(page)
		layout.setContentsMargins(
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
		)

		layout.addWidget(
			self._create_panel(
				title,
				description,
			)
		)

		return page
