from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QProgressBar,
	QVBoxLayout,
)

from app.models.character import Character
from app.theme.images import (
	CHARACTER_PORTRAITS,
	PARTY_PORTRAITS,
	load_cover_pixmap,
)
from app.theme.spacing import Spacing


class GMCharacterCard(QFrame):
	selected = Signal(str)

	def __init__(
			self,
			character: Character,
			connected: bool = False,
	):
		super().__init__()

		self.character_id = character.id

		self.setObjectName("gmCharacterCard")
		self.setProperty("selected", False)
		self.setCursor(
			Qt.CursorShape.PointingHandCursor
		)

		self._create_ui()
		self.update_character(character)
		self.set_connected(connected)

	def _create_ui(self) -> None:
		layout = QHBoxLayout(self)
		layout.setContentsMargins(
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.SM)

		self.portrait_label = QLabel()
		self.portrait_label.setObjectName(
			"gmCharacterPortrait"
		)
		self.portrait_label.setFixedSize(52, 52)
		self.portrait_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		content_layout = QVBoxLayout()
		content_layout.setContentsMargins(0, 0, 0, 0)
		content_layout.setSpacing(Spacing.XS)

		header_layout = QHBoxLayout()
		header_layout.setContentsMargins(0, 0, 0, 0)
		header_layout.setSpacing(Spacing.XS)

		self.name_label = QLabel()
		self.name_label.setObjectName(
			"gmCharacterName"
		)

		self.level_label = QLabel()
		self.level_label.setObjectName(
			"gmCharacterMeta"
		)

		header_layout.addWidget(self.name_label, 1)
		header_layout.addWidget(self.level_label)

		self.health_bar = QProgressBar()
		self.health_bar.setObjectName(
			"gmCharacterHealth"
		)

		self.connection_label = QLabel()

		content_layout.addLayout(header_layout)
		content_layout.addWidget(self.health_bar)
		content_layout.addWidget(
			self.connection_label
		)

		layout.addWidget(self.portrait_label)
		layout.addLayout(content_layout, 1)

		for widget in (
				self.portrait_label,
				self.name_label,
				self.level_label,
				self.health_bar,
				self.connection_label,
		):
			widget.setAttribute(
				Qt.WidgetAttribute.WA_TransparentForMouseEvents,
				True,
			)

	def update_character(
			self,
			character: Character,
	) -> None:
		self.character_id = character.id

		name = character.name or "Без имени"
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

		self.name_label.setText(name)
		self.level_label.setText(
			f"{character.level} ур."
		)

		self.health_bar.setRange(0, maximum)
		self.health_bar.setValue(current)
		self.health_bar.setFormat(
			f"{current} / {maximum} HP"
		)

		if character.party_portrait:
			portrait_folder = PARTY_PORTRAITS
			portrait_name = (
				character.party_portrait
			)
		else:
			portrait_folder = (
				CHARACTER_PORTRAITS
			)
			portrait_name = character.portrait

		pixmap = load_cover_pixmap(
			portrait_folder,
			portrait_name,
			self.portrait_label.size(),
		)

		if pixmap.isNull():
			self.portrait_label.setPixmap(pixmap)
			self.portrait_label.setText(
				name.strip()[:1].upper() or "?"
			)
		else:
			self.portrait_label.setText("")
			self.portrait_label.setPixmap(
				pixmap
			)

	def set_connected(
			self,
			connected: bool,
	) -> None:
		self.connection_label.setObjectName(
			"gmConnectionOnline"
			if connected
			else "gmConnectionOffline"
		)

		self.connection_label.setText(
			"● Подключён"
			if connected
			else "● Не подключён"
		)

		style = self.connection_label.style()
		style.unpolish(self.connection_label)
		style.polish(self.connection_label)

	def set_selected(
			self,
			selected: bool,
	) -> None:
		self.setProperty("selected", selected)

		style = self.style()
		style.unpolish(self)
		style.polish(self)
		self.update()

	def mouseReleaseEvent(
			self,
			event: QMouseEvent,
	) -> None:
		if (
				event.button()
				== Qt.MouseButton.LeftButton
		):
			self.selected.emit(
				self.character_id
			)
			event.accept()
			return

		super().mouseReleaseEvent(event)