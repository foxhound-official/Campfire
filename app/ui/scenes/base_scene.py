from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
	QLabel,
	QStackedLayout,
	QVBoxLayout,
	QWidget,
)

from app.theme.spacing import Spacing


class BaseScene(QWidget):

	def __init__(self, title: str):
		super().__init__()

		self.background = QLabel()
		self.background.setObjectName("sceneBackground")
		self.background.setScaledContents(True)

		self.overlay = QWidget()

		overlay_layout = QVBoxLayout(self.overlay)
		overlay_layout.setContentsMargins(
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
		)
		overlay_layout.setSpacing(Spacing.LG)

		self.banner = QLabel(title)
		self.banner.setObjectName("sceneBanner")
		self.banner.setAlignment(Qt.AlignmentFlag.AlignCenter)

		overlay_layout.addWidget(self.banner)

		self.content = QWidget()

		self.content_layout = QVBoxLayout(self.content)
		self.content_layout.setContentsMargins(0, 0, 0, 0)
		self.content_layout.setSpacing(Spacing.MD)

		overlay_layout.addWidget(self.content, 1)

		stack = QStackedLayout(self)
		stack.setStackingMode(QStackedLayout.StackAll)

		stack.addWidget(self.background)
		stack.addWidget(self.overlay)

	def set_title(self, text: str):
		self.banner.setText(text)

	def set_background(self, path: str):
		self.background.setPixmap(QPixmap(path))
