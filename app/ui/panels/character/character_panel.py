from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
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
from pathlib import Path
from PySide6.QtWidgets import QFileDialog

from app.models.campaign import Campaign
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
		self.portrait.setCursor(Qt.CursorShape.PointingHandCursor)
		self.portrait.mousePressEvent = self.on_portrait_clicked

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

		self.update_portrait()

		self.name.setText(character.name)
		self.race.setText(character.race)
		self.character_class.setText(character.character_class)

		self.level.setValue(character.level)

		self.update_health()
		self.update_effects()

		if character.portrait:
			pixmap = QPixmap(character.portrait)

			if not pixmap.isNull():
				self.portrait.setPixmap(
					pixmap.scaled(
						self.portrait.size(),
						Qt.AspectRatioMode.KeepAspectRatio,
						Qt.TransformationMode.SmoothTransformation,
					)
				)

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

		self.update_portrait()

		for effect in self.character.effects:
			self.effects.addItem(effect.name)

	def on_name_changed(self, text: str):
		if self.character is None:
			return

		self.character.name = text

		row = self.characters.currentRow()

		if row >= 0:
			self.characters.item(row).setText(text)

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

	def clear(self) -> None:
		self.character = None

		self.name.clear()
		self.race.clear()
		self.character_class.clear()

		self.level.setValue(1)

		self.health.setValue(0)
		self.health.setFormat("0 / 0")

		self.effects.clear()

		self.portrait.clear()
		self.portrait.setText("Портрет")

	def on_portrait_clicked(self, event) -> None:

		if self.character is None:
			return

		filename, _ = QFileDialog.getOpenFileName(
			self,
			"Выберите портрет",
			"",
			"Изображения (*.png *.jpg *.jpeg *.webp)"
		)

		if not filename:
			return

		self.character.portrait = filename

		self.update_portrait()

	def update_portrait(self) -> None:

		self.portrait.clear()

		if self.character is None:
			self.portrait.setText("Портрет")
			return

		path = Path(self.character.portrait)

		if not path.exists():
			self.portrait.setText("Портрет")
			return

		pixmap = QPixmap(str(path))

		self.portrait.setPixmap(
			pixmap.scaled(
				self.portrait.size(),
				Qt.AspectRatioMode.KeepAspectRatio,
				Qt.TransformationMode.SmoothTransformation,
			)
		)
