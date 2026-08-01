from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QProgressBar,
	QVBoxLayout,
)

from app.models.creature import Creature
from app.theme.images import (
	CREATURE_PORTRAITS,
	load_cover_pixmap,
)
from app.theme.spacing import Spacing


class GMCreatureCard(QFrame):
	def __init__(
			self,
			creature: Creature,
	):
		super().__init__()

		self.setObjectName("gmCreatureCard")
		self.setFixedWidth(190)

		self._create_ui()
		self.set_creature(creature)

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
			"gmCreaturePortrait"
		)
		self.portrait_label.setFixedSize(56, 56)
		self.portrait_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		content_layout = QVBoxLayout()
		content_layout.setContentsMargins(0, 0, 0, 0)
		content_layout.setSpacing(Spacing.XS)

		self.name_label = QLabel()
		self.name_label.setObjectName(
			"gmCreatureName"
		)
		self.name_label.setWordWrap(True)

		self.health_bar = QProgressBar()
		self.health_bar.setObjectName(
			"gmCreatureHealth"
		)

		content_layout.addWidget(self.name_label)
		content_layout.addStretch()
		content_layout.addWidget(self.health_bar)

		layout.addWidget(self.portrait_label)
		layout.addLayout(content_layout, 1)

	def set_creature(
			self,
			creature: Creature,
	) -> None:
		name = creature.name or "Без названия"

		maximum = max(
			1,
			creature.health.maximum,
		)
		current = max(
			0,
			min(
				creature.health.current,
				maximum,
			),
		)
		temporary = max(
			0,
			creature.health.temporary,
		)

		self.name_label.setText(name)

		self.health_bar.setRange(0, maximum)
		self.health_bar.setValue(current)

		if temporary > 0:
			self.health_bar.setFormat(
				f"{current} / {maximum} (+{temporary})"
			)
		else:
			self.health_bar.setFormat(
				f"{current} / {maximum}"
			)

		pixmap = load_cover_pixmap(
			CREATURE_PORTRAITS,
			creature.portrait,
			self.portrait_label.size(),
		)

		if pixmap.isNull():
			self.portrait_label.clear()
			self.portrait_label.setText(
				name.strip()[:1].upper() or "?"
			)
		else:
			self.portrait_label.setText("")
			self.portrait_label.setPixmap(pixmap)