from PySide6.QtWidgets import QLabel

from app.theme.colors import Colors

class BodyLabel(QLabel):
	def __init__(self, text: str):
		super().__init__(text)

		self.setStyleSheet(
			f"""
			color: {Colors.TEXT};
			font-size: 16px;
			"""
		)