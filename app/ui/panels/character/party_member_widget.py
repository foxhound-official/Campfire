from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QMouseEvent, QPainter, QPaintEvent, QColor, QPen
from PySide6.QtWidgets import (
	QLabel,
	QProgressBar,
	QVBoxLayout,
	QWidget,
)

from app.models.character import Character
from app.theme.colors import Colors
from app.theme.images import (
	PARTY_PORTRAITS,
	load_cover_pixmap,
)
from app.theme.radius import Radius
from app.theme.sizes import Sizes
from app.theme.spacing import Spacing


class PartyMemberWidget(QWidget):
	selected = Signal(str)

	def __init__(self, character: Character):
		super().__init__()

		self.character_id = character.id
		self._target_selection_enabled = False

		self.setObjectName("partyMember")
		self.setFixedSize(
			Sizes.PARTY_MEMBER_WIDTH,
			Sizes.PARTY_MEMBER_HEIGHT,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(Spacing.XS)

		self.portrait = PartyPortraitLabel()
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

		# Клики по дочерним элементам обрабатывает
		# сам PartyMemberWidget.
		self.portrait.setAttribute(
			Qt.WidgetAttribute.WA_TransparentForMouseEvents,
			True,
		)
		self.health.setAttribute(
			Qt.WidgetAttribute.WA_TransparentForMouseEvents,
			True,
		)

		layout.addWidget(self.portrait)
		layout.addWidget(self.health)

		self.update_character(character)

	def update_character(
			self,
			character: Character,
	) -> None:
		self.character_id = character.id

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

		self.setToolTip(
			f"{name}\n"
			f"{character_class}, {character.level} ур.\n"
			f"Здоровье: {current} / {maximum}"
		)

		self.update_portrait(
			character.party_portrait
			or character.portrait,
			name,
		)

	def update_portrait(
			self,
			portrait_name: str,
			character_name: str,
	) -> None:
		self.portrait.clear()

		pixmap = load_cover_pixmap(
			PARTY_PORTRAITS,
			portrait_name,
			self.portrait.size(),
		)

		if pixmap.isNull():
			initial = (
					character_name.strip()[:1].upper()
					or "?"
			)
			self.portrait.setText(initial)
			return

		self.portrait.setPixmap(pixmap)

	def set_target_selection_enabled(
			self,
			enabled: bool,
	) -> None:
		self._target_selection_enabled = enabled

		self.portrait.set_target_selection_enabled(
			enabled
		)

		self.setCursor(
			Qt.CursorShape.PointingHandCursor
			if enabled
			else Qt.CursorShape.ArrowCursor
		)

		for widget in (
				self,
				self.portrait,
		):
			style = widget.style()
			style.unpolish(widget)
			style.polish(widget)
			widget.update()

	def mouseReleaseEvent(
			self,
			event: QMouseEvent,
	) -> None:
		if (
				self._target_selection_enabled
				and event.button()
				== Qt.MouseButton.LeftButton
		):
			self.selected.emit(self.character_id)
			event.accept()
			return

		super().mouseReleaseEvent(event)


class PartyPortraitLabel(QLabel):

	def __init__(self):
		super().__init__()

		self._target_selection_enabled = False

	def set_target_selection_enabled(
			self,
			enabled: bool,
	) -> None:
		self._target_selection_enabled = enabled
		self.update()

	def paintEvent(
			self,
			event: QPaintEvent,
	) -> None:
		super().paintEvent(event)

		if not self._target_selection_enabled:
			return

		border_width = 4

		painter = QPainter(self)
		painter.setRenderHint(
			QPainter.RenderHint.Antialiasing
		)
		painter.setBrush(
			Qt.BrushStyle.NoBrush
		)
		painter.setPen(
			QPen(
				QColor(Colors.TARGET_HIGHLIGHT),
				border_width,
			)
		)

		inset = border_width / 2 - 2

		rect = QRectF(self.rect()).adjusted(
			inset,
			inset,
			-inset,
			-inset,
		)

		painter.drawRoundedRect(
			rect,
			Radius.SM,
			Radius.SM,
		)
