from PySide6.QtWidgets import QFrame, QVBoxLayout

from app.theme.colors import Colors
from app.theme.radius import BorderRadius
from app.theme.spacing import Spacing


class Card(QFrame):
	def __init__(self):
		super().__init__()

		self.setStyleSheet(
			f"""
			QFrame {{
				background-color: {Colors.SURFACE};
				border-radius: {BorderRadius.SXS};
			}}
			"""
		)

		self.layout = QVBoxLayout(self)

		self.layout.setContentsMargins(
			Spacing.M,
			Spacing.M,
			Spacing.M,
			Spacing.M
		)

		self.layout.setSpacing(Spacing.SXS)