from PySide6.QtWidgets import QHBoxLayout

from app.theme.spacing import Spacing
from app.widgets.card import Card
from app.widgets.label import BodyLabel


class InfoCard(Card):
	def __init__(self, title: str, value: str):
		super().__init__()

		self.layout.setContentsMargins(
			Spacing.M,
			Spacing.SXS,
			Spacing.M,
			Spacing.SXS
		)

		row = QHBoxLayout()

		self.title = BodyLabel(title)
		self.value = BodyLabel(value)

		row.addWidget(self.title)
		row.addStretch()
		row.addWidget(self.value)

		self.layout.addLayout(row)