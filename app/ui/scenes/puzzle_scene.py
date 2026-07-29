from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from app.ui.scenes.base_scene import BaseScene


class PuzzleScene(BaseScene):

	def __init__(self):
		super().__init__("Головоломка")

		self.content_layout.addWidget(
			QLabel("Puzzle Scene"),
			alignment=Qt.AlignmentFlag.AlignCenter,
		)
