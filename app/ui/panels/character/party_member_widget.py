from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
	QLabel,
	QProgressBar,
	QVBoxLayout,
	QWidget,
)

from app.models.character import Character
from app.theme.images import load_cover_pixmap, PARTY_PORTRAITS
from app.theme.sizes import Sizes
from app.theme.spacing import Spacing


PARTY_PORTRAITS_PATH = (
	Path(__file__).resolve().parents[3]
	/ "assets"
	/ "portraits"
	/ "party"
)

PARTY_PORTRAIT_EXTENSIONS = (
	".png",
	".webp",
	".jpg",
	".jpeg",
)


class PartyMemberWidget(QWidget):

	def __init__(self, character: Character):
		super().__init__()

		self.setObjectName("partyMember")
		self.setFixedSize(
			Sizes.PARTY_MEMBER_WIDTH,
			Sizes.PARTY_MEMBER_HEIGHT,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(Spacing.XS)

		self.portrait = QLabel()
		self.portrait.setObjectName(
			"partyMemberPortrait"
		)
		self.portrait.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)
		self.portrait.setFixedSize(
			Sizes.PARTY_PORTRAIT_SIZE,
			Sizes.PARTY_PORTRAIT_SIZE,
		)

		self.health = QProgressBar()
		self.health.setObjectName(
			"partyMemberHealth"
		)
		self.health.setTextVisible(False)
		self.health.setFixedSize(
			Sizes.PARTY_MEMBER_WIDTH,
			Sizes.PARTY_HEALTH_HEIGHT,
		)

		layout.addWidget(self.portrait)
		layout.addWidget(self.health)

		self.update_character(character)

	def update_character(
		self,
		character: Character,
	) -> None:
		maximum = max(
			1,
			character.health.maximum,
		)
		current = max(
			0,
			min(
				character.health.current,
				maximum,
			),
		)

		self.health.setRange(0, maximum)
		self.health.setValue(current)

		name = character.name or "Без имени"
		character_class = (
			character.character_class
			or "Класс не указан"
		)

		tooltip = (
			f"{name}\n"
			f"{character_class}, {character.level} ур.\n"
			f"Здоровье: {current} / {maximum}"
		)

		if character.health.temporary > 0:
			tooltip += (
				f"\nВременное здоровье: "
				f"+{character.health.temporary}"
			)

		self.setToolTip(tooltip)

		self.update_portrait(
			character.party_portrait,
			name,
		)

	def update_portrait(
		self,
		portrait_name: str,
		character_name: str,
	) -> None:
		self.portrait.clear()

		initial = (
			character_name.strip()[:1].upper()
			or "?"
		)
		self.portrait.setText(initial)

		if not portrait_name:
			return

		portrait_path = self.find_portrait(
			portrait_name
		)

		if portrait_path is None:
			return

		pixmap = load_cover_pixmap(
			PARTY_PORTRAITS,
			portrait_name,
			self.portrait.size(),
		)

		if pixmap.isNull():
			return

		target_size = self.portrait.size()

		scaled_pixmap = pixmap.scaled(
			target_size,
			Qt.AspectRatioMode.KeepAspectRatioByExpanding,
			Qt.TransformationMode.SmoothTransformation,
		)

		crop_x = max(
			0,
			(
				scaled_pixmap.width()
				- target_size.width()
			) // 2,
		)
		crop_y = max(
			0,
			(
				scaled_pixmap.height()
				- target_size.height()
			) // 2,
		)

		self.portrait.setText("")
		self.portrait.setPixmap(
			scaled_pixmap.copy(
				crop_x,
				crop_y,
				target_size.width(),
				target_size.height(),
			)
		)

	@staticmethod
	def find_portrait(
		portrait_name: str,
	) -> Path | None:
		for extension in PARTY_PORTRAIT_EXTENSIONS:
			portrait_path = (
				PARTY_PORTRAITS_PATH
				/ f"{portrait_name}{extension}"
			)

			if portrait_path.is_file():
				return portrait_path

		return None