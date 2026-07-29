from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QMainWindow,
	QWidget, QHBoxLayout,
)

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

		self.workspace = QWidget()

		layout.addWidget(self.character_panel)
		layout.addWidget(self.workspace, 1)

		self.setCentralWidget(central)
