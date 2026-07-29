from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class CharacterListItem(QLabel):

	def __init__(self, name: str):
		super().__init__(name)

		self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
		self.setFixedHeight(36)
