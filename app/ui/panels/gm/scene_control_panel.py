from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
	QComboBox,
	QFrame,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QVBoxLayout,
)

from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.theme.spacing import Spacing


SCENE_TYPE_TITLES = {
	SceneType.BATTLE: "Боевая",
	SceneType.NARRATION: "Повествовательная",
	SceneType.MERCHANT: "Торговая",
	SceneType.PUZZLE: "Головоломка",
}


class SceneControlPanel(QFrame):
	scene_activation_requested = Signal(str)

	def __init__(self):
		super().__init__()

		self._scenes: dict[str, SceneData] = {}
		self._active_scene_id: str | None = None

		self.setObjectName("gmPanel")
		self._create_ui()

	def _create_ui(self) -> None:
		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		layout.setSpacing(Spacing.MD)

		title_label = QLabel("Управление сценой")
		title_label.setObjectName("gmPanelTitle")

		controls_layout = QHBoxLayout()
		controls_layout.setSpacing(Spacing.SM)

		self.scene_selector = QComboBox()
		self.scene_selector.setObjectName(
			"gmSceneSelector"
		)
		self.scene_selector.currentIndexChanged.connect(
			self._show_selected_scene
		)

		self.activate_button = QPushButton(
			"Показать игрокам"
		)
		self.activate_button.setObjectName(
			"gmPrimaryButton"
		)
		self.activate_button.clicked.connect(
			self._request_activation
		)

		controls_layout.addWidget(
			self.scene_selector,
			1,
		)
		controls_layout.addWidget(
			self.activate_button
		)

		self.scene_title_label = QLabel()
		self.scene_title_label.setObjectName(
			"gmScenePreviewTitle"
		)
		self.scene_title_label.setWordWrap(True)

		self.scene_type_label = QLabel()
		self.scene_type_label.setObjectName(
			"gmSceneTypeBadge"
		)

		self.description_label = QLabel()
		self.description_label.setObjectName(
			"gmSceneDescription"
		)
		self.description_label.setWordWrap(True)

		self.background_label = QLabel()
		self.background_label.setObjectName(
			"gmSceneResource"
		)
		self.background_label.setWordWrap(True)

		self.music_label = QLabel()
		self.music_label.setObjectName(
			"gmSceneResource"
		)
		self.music_label.setWordWrap(True)

		layout.addWidget(title_label)
		layout.addLayout(controls_layout)
		layout.addWidget(self.scene_title_label)
		layout.addWidget(self.scene_type_label)
		layout.addWidget(self.description_label, 1)
		layout.addWidget(self.background_label)
		layout.addWidget(self.music_label)

	def set_scenes(
			self,
			scenes: list[SceneData],
			active_scene_id: str | None,
	) -> None:
		self._scenes = {
			scene.id: scene
			for scene in scenes
		}
		self._active_scene_id = active_scene_id

		self.scene_selector.blockSignals(True)
		self.scene_selector.clear()

		active_index = -1

		for index, scene in enumerate(scenes):
			title = scene.title or "Сцена без названия"

			self.scene_selector.addItem(
				title,
				scene.id,
			)

			if scene.id == active_scene_id:
				active_index = index

		self.scene_selector.blockSignals(False)

		if not scenes:
			self._clear()
			return

		if active_index < 0:
			active_index = 0

		self.scene_selector.setCurrentIndex(
			active_index
		)
		self._show_selected_scene(active_index)

	def _show_selected_scene(
			self,
			index: int,
	) -> None:
		scene_id = self.scene_selector.itemData(index)
		scene = self._scenes.get(scene_id)

		if scene is None:
			self._clear()
			return

		scene_type_title = SCENE_TYPE_TITLES.get(
			scene.scene_type,
			scene.scene_type.value,
		)

		self.scene_title_label.setText(
			scene.title or "Сцена без названия"
		)
		self.scene_type_label.setText(
			scene_type_title
		)
		self.description_label.setText(
			scene.description
			or "Описание сцены не указано."
		)
		self.background_label.setText(
			"Фон: "
			f"{scene.background or 'не указан'}"
		)
		self.music_label.setText(
			"Музыка: "
			f"{scene.music or 'не указана'}"
		)

		is_active = scene.id == self._active_scene_id

		self.activate_button.setEnabled(not is_active)
		self.activate_button.setText(
			"Сцена активна"
			if is_active
			else "Показать игрокам"
		)

	def _request_activation(self) -> None:
		scene_id = self.scene_selector.currentData()

		if not scene_id:
			return

		self.scene_activation_requested.emit(
			scene_id
		)

	def _clear(self) -> None:
		self.scene_title_label.setText(
			"В кампании нет сцен"
		)
		self.scene_type_label.clear()
		self.description_label.clear()
		self.background_label.clear()
		self.music_label.clear()
		self.activate_button.setEnabled(False)