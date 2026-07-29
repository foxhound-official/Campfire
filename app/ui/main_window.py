from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QMainWindow,
	QWidget, QHBoxLayout,
)

from app.models.character import Character
from app.ui.panels.character.character_panel import CharacterPanel


class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.setWindowTitle("Campfire")
		self.resize(1400, 900)

		central = QWidget()

		layout = QHBoxLayout(central)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		self.character_panel = CharacterPanel()

		character = Character(
			name="Альрик",
			race="Человек",
			character_class="Паладин",
		)

		self.character_panel.set_character(character)

		self.workspace = QWidget()

		layout.addWidget(self.character_panel)
		layout.addWidget(self.workspace, 1)

		self.setCentralWidget(central)
