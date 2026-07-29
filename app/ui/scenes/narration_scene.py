from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from app.ui.scenes.base_scene import BaseScene


class NarrationScene(BaseScene):

	def __init__(self):
		super().__init__("История")

		self.content_layout.addWidget(
			QLabel("Narration Scene"),
			alignment=Qt.AlignmentFlag.AlignCenter,
		)
