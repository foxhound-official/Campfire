from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from app.ui.scenes.base_scene import BaseScene


class BattleScene(BaseScene):

	def __init__(self):
		super().__init__("Поле боя")

		self.content_layout.addWidget(
			QLabel("Battle Scene"),
			alignment=Qt.AlignmentFlag.AlignCenter,
		)
