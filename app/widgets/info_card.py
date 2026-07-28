from PySide6.QtWidgets import QHBoxLayout

from app.theme.spacing import Spacing
from app.widgets.card import Card
from app.widgets.label import BodyLabel


class InfoCard(Card):
	def __init__(self, title: str, value: str):
		super().__init__()

		self.content_layout.setContentsMargins(
			Spacing.M,
			Spacing.SXS,
			Spacing.M,
			Spacing.SXS,
		)

		row = QHBoxLayout()
		row.setContentsMargins(0, 0, 0, 0)

		self.title_label = BodyLabel(title)
		self.value_label = BodyLabel(value)

		row.addWidget(self.title_label)
		row.addStretch()
		row.addWidget(self.value_label)

		self.content_layout.addLayout(row)

	def set_value(self, value: str) -> None:
		self.value_label.setText(value)