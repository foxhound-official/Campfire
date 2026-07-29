from PySide6.QtWidgets import QLabel

from app.theme.colors import Colors


class TitleLabel(QLabel):
	def __init__(self, text: str):
		super().__init__(text)

		self.setStyleSheet(
			f"""
			color: {Colors.TEXT};
			font-size: 22px;
			font-weight: 700;
			"""
		)


class BodyLabel(QLabel):
	def __init__(self, text: str):
		super().__init__(text)

		self.setStyleSheet(
			f"""
			color: {Colors.TEXT};
			font-size: 16px;
			"""
		)


class CaptionLabel(QLabel):
	def __init__(self, text: str):
		super().__init__(text)

		self.setStyleSheet(
			f"""
			color: {Colors.TEXT_SECONDARY};
			font-size: 13px;
			"""
		)