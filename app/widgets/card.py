from PySide6.QtWidgets import QFrame, QVBoxLayout

from app.theme.colors import Colors
from app.theme.radius import Radius
from app.theme.spacing import Spacing


class Card(QFrame):
	def __init__(self):
		super().__init__()

		self.setStyleSheet(
			f"""
			QFrame {{
				background-color: {Colors.SURFACE};
				border-radius: {Radius.MEDIUM};
			}}
			"""
		)

		self.content_layout = QVBoxLayout(self)

		self.content_layout.setContentsMargins(
			Spacing.M,
			Spacing.M,
			Spacing.M,
			Spacing.M
		)

		self.content_layout.setSpacing(Spacing.SXS)