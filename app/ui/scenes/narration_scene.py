from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy

from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.ui.scenes.base_scene import BaseScene


class NarrationScene(BaseScene):

	def __init__(self):
		super().__init__("История")

		self.text = QLabel()
		self.text.setObjectName("narrationText")
		self.text.setWordWrap(True)
		self.text.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)
		self.text.setMaximumWidth(950)
		self.text.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Preferred,
		)

		self.content_layout.addWidget(
			self.text,
			alignment=Qt.AlignmentFlag.AlignCenter,
		)

	def set_scene(
			self,
			scene_data: SceneData,
	) -> None:
		if (
			scene_data.scene_type
			is not SceneType.NARRATION
		):
			raise ValueError(
				"NarrationScene принимает только "
				"повествовательные сцены"
			)

		super().set_scene(scene_data)

		self.text.setText(
			scene_data.description
		)