from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFrame,
	QLabel,
	QVBoxLayout,
)

from app.theme.sizes import Sizes
from app.theme.spacing import Spacing


class Card(QFrame):

	def __init__(self):
		super().__init__()

		self.setObjectName("card")

		self.setFixedWidth(180)

		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		self.layout.setSpacing(Spacing.SM)

		self.image = QLabel()
		self.image.setObjectName("cardImage")
		self.image.setFixedHeight(Sizes.PORTRAIT_HEIGHT // 2)
		self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.image.setText("Нет изображения")

		self.layout.addWidget(self.image)

		self.content_layout = QVBoxLayout()
		self.content_layout.setContentsMargins(0, 0, 0, 0)
		self.content_layout.setSpacing(Spacing.SM)

		self.layout.addLayout(self.content_layout)
