from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
	QFrame,
	QLabel,
	QLineEdit,
	QListWidget,
	QProgressBar,
	QSpinBox,
	QVBoxLayout, QHBoxLayout,
)
from pathlib import Path
from PySide6.QtWidgets import QFileDialog

from app.models.character import Character
from app.theme.sizes import Sizes
from app.theme.spacing import Spacing


class CharacterPanel(QFrame):

	def __init__(self):
		super().__init__()

		self.setFixedWidth(Sizes.CHARACTER_PANEL_WIDTH)

		# Title

		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
		)

		layout.setSpacing(Spacing.MD)

		title = QLabel("Персонаж")
		layout.addWidget(title)

		# Portrait

		self.portrait = QLabel("Нажмите, чтобы выбрать изображение")

		self.portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.portrait.setFixedHeight(Sizes.PORTRAIT_HEIGHT)
		self.portrait.setFrameShape(QFrame.Shape.Box)
		self.portrait.setCursor(Qt.CursorShape.PointingHandCursor)
		self.portrait.mousePressEvent = self.on_portrait_clicked
		self.portrait.setScaledContents(False)

		layout.addWidget(self.portrait)

		# Description

		layout.addWidget(QLabel("Имя"))
		self.name = QLineEdit()
		self.name.textEdited.connect(self.on_name_changed)
		layout.addWidget(self.name)

		layout.addWidget(QLabel("Раса"))
		self.race = QLineEdit()
		self.race.textEdited.connect(self.on_race_changed)
		layout.addWidget(self.race)

		layout.addWidget(QLabel("Класс"))
		self.character_class = QLineEdit()
		self.character_class.textEdited.connect(self.on_class_changed)
		layout.addWidget(self.character_class)

		# Level

		row = QHBoxLayout()

		row.addWidget(QLabel("Уровень"))

		self.level = QSpinBox()
		self.level.setRange(1, 20)
		self.level.valueChanged.connect(self.on_level_changed)

		row.addWidget(self.level)

		layout.addLayout(row)

		# Health

		layout.addWidget(QLabel("Здоровье"))

		hp_row = QHBoxLayout()

		self.current_hp = QSpinBox()
		self.current_hp.setMaximum(9999)

		self.maximum_hp = QSpinBox()
		self.maximum_hp.setMaximum(9999)

		hp_row.addWidget(self.current_hp)
		hp_row.addWidget(QLabel("/"))
		hp_row.addWidget(self.maximum_hp)

		layout.addLayout(hp_row)

		self.health = QProgressBar()
		layout.addWidget(self.health)

		# Abilities and skills

		layout.addWidget(QLabel("Навыки"))

		self.skills = QListWidget()

		layout.addWidget(self.skills)

		layout.addStretch()

		# Game Party

		layout.addStretch()

		layout.addWidget(QLabel("Пати"))

		self.party = QListWidget()
		self.party.setMaximumHeight(Sizes.PARTY_HEIGHT)

		layout.addWidget(self.party)

	def set_character(self, character: Character) -> None:
		self.character = character

		self.update_portrait()

		self.name.setText(character.name)
		self.race.setText(character.race)
		self.character_class.setText(character.character_class)

		self.level.setValue(character.level)

		self.update_health()
		# self.update_skills()

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

	def update_skills(self):

		self.skills.clear()

		if self.character is None:
			return

		for skill in self.character.skills:
			self.skills.addItem(skill.name)

			self.skills.item(
				self.skills.count() - 1
			).setToolTip(skill.description)

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
		self.portrait.setText("Нажмите, чтобы выбрать изображение")

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
			self.portrait.setText("Нажмите, чтобы выбрать изображение")
			return

		path = Path(self.character.portrait)

		if not path.exists():
			self.portrait.setText("Нажмите, чтобы выбрать изображение")
			return

		pixmap = QPixmap(str(path))

		self.portrait.setPixmap(
			pixmap.scaled(
				self.portrait.size(),
				Qt.AspectRatioMode.KeepAspectRatio,
				Qt.TransformationMode.SmoothTransformation,
			)
		)
