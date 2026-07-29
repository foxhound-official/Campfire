from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFormLayout,
	QFrame,
	QLabel,
	QLineEdit,
	QListWidget,
	QProgressBar,
	QSpinBox,
	QVBoxLayout,
)

from app.models.character import Character


class CharacterPanel(QFrame):
	WIDTH = 320

	def __init__(self):
		super().__init__()

		self.setFixedWidth(self.WIDTH)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(12, 12, 12, 12)
		layout.setSpacing(12)

		title = QLabel("Персонаж")
		layout.addWidget(title)

		self.portrait = QLabel("Портрет")
		self.portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.portrait.setFixedHeight(220)
		self.portrait.setFrameShape(QFrame.Shape.Box)

		layout.addWidget(self.portrait)

		form = QFormLayout()
		form.setSpacing(8)

		self.name = QLineEdit()
		self.race = QLineEdit()
		self.character_class = QLineEdit()

		self.level = QSpinBox()
		self.level.setMinimum(1)
		self.level.setMaximum(20)

		form.addRow("Имя", self.name)
		form.addRow("Раса", self.race)
		form.addRow("Класс", self.character_class)
		form.addRow("Уровень", self.level)

		layout.addLayout(form)

		layout.addWidget(QLabel("Здоровье"))

		self.health = QProgressBar()
		self.health.setRange(0, 100)
		self.health.setValue(100)

		layout.addWidget(self.health)

		layout.addWidget(QLabel("Эффекты"))

		self.effects = QListWidget()

		layout.addWidget(self.effects)

		layout.addStretch()

		self.character: Character | None = None

		self.name.textEdited.connect(self.on_name_changed)
		self.race.textEdited.connect(self.on_race_changed)
		self.character_class.textEdited.connect(self.on_class_changed)
		self.level.valueChanged.connect(self.on_level_changed)

	def set_character(self, character: Character) -> None:
		self.character = character

		self.name.setText(character.name)
		self.race.setText(character.race)
		self.character_class.setText(character.character_class)

		self.level.setValue(character.level)

		self.update_health()
		self.update_effects()

	def update_health(self) -> None:
		if self.character is None:
			return

		maximum = max(1, self.character.health.maximum)

		percent = int(
			self.character.health.current /
			maximum *
			100
		)

		self.health.setValue(percent)

		self.health.setFormat(
			f"{self.character.health.current} / {maximum}"
		)

	def update_effects(self) -> None:
		self.effects.clear()

		if self.character is None:
			return

		for effect in self.character.effects:
			self.effects.addItem(effect.name)

	def on_name_changed(self, text: str):
		if self.character is None:
			return

		self.character.name = text

	def on_race_changed(self, text: str):
		if self.character is None:
			return

		self.character.race = text

	def on_class_changed(self, text: str):
		if self.character is None:
			return

		self.character.character_class = text

	def on_level_changed(self, value: int):
		if self.character is None:
			return

		self.character.level = value
