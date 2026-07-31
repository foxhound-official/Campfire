from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
	QFrame,
	QLabel,
	QVBoxLayout, QGraphicsDropShadowEffect,
)

from app.theme.images import load_cover_pixmap
from app.theme.sizes import Sizes
from app.theme.spacing import Spacing


class Card(QFrame):

	def __init__(self):
		super().__init__()

		self.setObjectName("card")
		self.setFixedWidth(Sizes.CARD_WIDTH)

		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(18)
		self.shadow.setOffset(0, 20)
		self.shadow.setColor(QColor(24, 14, 8, 120))

		self.setGraphicsEffect(self.shadow)

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
		self.image.setFixedSize(
			Sizes.CARD_IMAGE_WIDTH,
			Sizes.CARD_IMAGE_HEIGHT,
		)
		self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.image.setText("Нет изображения")

		self.layout.addWidget(self.image)

		self.content_layout = QVBoxLayout()
		self.content_layout.setContentsMargins(0, 0, 0, 0)
		self.content_layout.setSpacing(Spacing.SM)

		self.layout.addLayout(self.content_layout)

	def set_image(
			self,
			folder: str,
			image_name: str,
	) -> None:
		pixmap = load_cover_pixmap(
			folder,
			image_name,
			self.image.size(),
		)

		self.image.clear()

		if pixmap.isNull():
			self.image.setText("Нет изображения")
			return

		self.image.setPixmap(pixmap)
