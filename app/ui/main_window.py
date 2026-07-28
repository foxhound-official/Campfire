from PySide6.QtWidgets import (
	QHBoxLayout,
	QMainWindow,
	QWidget,
)

from app.ui.scene_container import SceneContainer
from app.ui.scenes.narration_scene import NarrationScene
from app.theme.spacing import Spacing
from app.ui.panels.character.character_panel import CharacterPanel

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Campfire")
		self.resize(1400, 900)

		# Центральная область окна
		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		# Основной горизонтальный Layout
		main_layout = QHBoxLayout()
		main_layout.setContentsMargins(
			Spacing.SXS,
			Spacing.SXS,
			Spacing.SXS,
			Spacing.SXS
		)
		main_layout.setSpacing(Spacing.SXS)
		central_widget.setLayout(main_layout)

		left_panel = CharacterPanel()

		scene_container = SceneContainer()
		scene = NarrationScene()
		scene_container.show_scene(scene)

		# right_panel = SidebarPanel()

		left_panel.setStyleSheet("background-color: #2C2C2C; border-radius: 12px;")
		scene_container.setStyleSheet("background-color: #1D1D1D; border-radius: 12px;")
		# right_panel.setStyleSheet("background-color: transparent;")

		main_layout.addWidget(left_panel)
		main_layout.addWidget(scene_container, 1)
		# main_layout.addWidget(right_panel)
