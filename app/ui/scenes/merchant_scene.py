from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from app.ui.scenes.base_scene import BaseScene


class MerchantScene(BaseScene):

	def __init__(self):
		super().__init__("Торговец")

		self.content_layout.addWidget(
			QLabel("Merchant Scene"),
			alignment=Qt.AlignmentFlag.AlignCenter,
		)
