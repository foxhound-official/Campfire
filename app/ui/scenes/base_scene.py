from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
	QLabel,
	QStackedLayout,
	QVBoxLayout,
	QWidget,
)

from app.models.scene_data import SceneData
from app.theme.spacing import Spacing


class BaseScene(QWidget):

	def __init__(self, title: str):
		super().__init__()

		self.scene_data: SceneData | None = None

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

		# Overlay должен находиться поверх фона
		stack.setCurrentWidget(self.overlay)

	def set_scene(
			self,
			scene_data: SceneData,
	) -> None:
		self.scene_data = scene_data

		self.set_title(scene_data.title)
		self.set_background(scene_data.background)

	def set_title(self, text: str) -> None:
		self.banner.setText(text)

	def set_background(self, path: str) -> None:
		if not path:
			self.background.clear()
			return

		self.background.setPixmap(QPixmap(path))
