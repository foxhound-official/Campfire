from PySide6.QtWidgets import (
	QHBoxLayout,
	QMainWindow,
	QWidget,
)

from app.models.character import Character
from app.theme.spacing import Spacing
from app.ui.panels.character.character_panel import CharacterPanel
from app.ui.scene_container import SceneContainer
from app.ui.scenes.narration_scene import NarrationScene


class MainWindow(QMainWindow):
	def __init__(self, character: Character):
		super().__init__()

		self.setWindowTitle("Campfire")
		self.setMinimumSize(1100, 700)
		self.resize(1400, 900)

		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		main_layout = QHBoxLayout(central_widget)
		main_layout.setContentsMargins(
			Spacing.SXS,
			Spacing.SXS,
			Spacing.SXS,
			Spacing.SXS,
		)
		main_layout.setSpacing(Spacing.SXS)

		self.character_panel = CharacterPanel(character)

		self.scene_container = SceneContainer()
		self.scene_container.setStyleSheet(
			"""
            background-color: #1D1D1D;
            border-radius: 12px;
            """
		)

		narration_scene = NarrationScene()
		self.scene_container.show_scene(narration_scene)

		main_layout.addWidget(self.character_panel)
		main_layout.addWidget(self.scene_container, 1)
