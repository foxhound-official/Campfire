from PySide6.QtWidgets import (
	QPushButton,
	QScrollArea,
	QVBoxLayout,
	QWidget,
)

from app.models.character import Character
from app.ui.panels.character.character_list_item import CharacterListItem


class CharacterList(QWidget):

	def __init__(self):
		super().__init__()

		self.characters: list[Character] = []

		self.layout = QVBoxLayout(self)

		self.scroll = QScrollArea()
		self.scroll.setWidgetResizable(True)

		self.container = QWidget()
		self.items_layout = QVBoxLayout(self.container)

		self.scroll.setWidget(self.container)

		self.add_button = QPushButton("+ Новый персонаж")
		self.add_button.clicked.connect(self.add_character)

		self.layout.addWidget(self.scroll)
		self.layout.addWidget(self.add_button)

	def add_character(self):
		character = Character(
			name="Новый персонаж"
		)

		self.characters.append(character)

		self.items_layout.addWidget(
			CharacterListItem(character.name)
		)
