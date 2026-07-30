from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
	QAbstractItemView,
	QFrame,
	QHBoxLayout,
	QHeaderView,
	QLabel,
	QListWidget,
	QProgressBar,
	QSizePolicy,
	QTreeWidget,
	QTreeWidgetItem,
	QVBoxLayout,
)

from app.models.character import Character
from app.theme.fonts import Fonts
from app.theme.sizes import Sizes
from app.theme.spacing import Spacing


class CharacterPanel(QFrame):

	def __init__(self):
		super().__init__()

		self.character: Character | None = None

		self.setFixedWidth(Sizes.CHARACTER_PANEL_WIDTH)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
		)
		layout.setSpacing(Spacing.MD)

		# Portrait

		self.portrait = QLabel(
			"Портрет\nне выбран"
		)
		self.portrait.setObjectName("characterPortrait")
		self.portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.portrait.setFixedSize(
			Sizes.PORTRAIT_WIDTH,
			Sizes.PORTRAIT_HEIGHT,
		)
		self.portrait.setWordWrap(True)

		layout.addWidget(
			self.portrait,
			alignment=Qt.AlignmentFlag.AlignHCenter,
		)

		# Character identity

		identity_frame, identity_layout = self.create_section()

		self.name = QLabel("Персонаж не выбран")
		self.name.setObjectName("characterName")
		self.name.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)
		self.name.setWordWrap(True)

		identity_layout.addWidget(self.name)

		meta_layout = QHBoxLayout()
		meta_layout.setContentsMargins(0, 0, 0, 0)
		meta_layout.setSpacing(Spacing.MD)

		# Race

		race_layout = QVBoxLayout()
		race_layout.setContentsMargins(0, 0, 0, 0)
		race_layout.setSpacing(Spacing.XS)

		race_title = QLabel("Раса")
		race_title.setObjectName("identityCaption")

		self.race = QLabel("-")
		self.race.setObjectName("identityValue")
		self.race.setWordWrap(True)

		race_layout.addWidget(race_title)
		race_layout.addWidget(self.race)

		# Class and level

		class_layout = QVBoxLayout()
		class_layout.setContentsMargins(0, 0, 0, 0)
		class_layout.setSpacing(Spacing.XS)

		class_title = QLabel("Класс")
		class_title.setObjectName("identityCaption")

		class_row = QHBoxLayout()
		class_row.setContentsMargins(0, 0, 0, 0)
		class_row.setSpacing(Spacing.SM)

		self.character_class = QLabel("-")
		self.character_class.setObjectName("identityValue")
		self.character_class.setWordWrap(True)

		self.level = QLabel("-")
		self.level.setObjectName("levelBadge")
		self.level.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.level.setFixedSize(
			Sizes.LEVEL_BADGE_SIZE,
			Sizes.LEVEL_BADGE_SIZE,
		)
		self.level.setToolTip("Уровень персонажа")

		class_row.addWidget(self.character_class, stretch=1)
		class_row.addWidget(self.level)

		class_layout.addWidget(class_title)
		class_layout.addLayout(class_row)

		meta_layout.addLayout(race_layout, stretch=1)
		meta_layout.addLayout(class_layout, stretch=1)

		identity_layout.addLayout(meta_layout)
		layout.addWidget(identity_frame)

		# Health

		health_frame, health_layout = self.create_section()

		health_title_row = QHBoxLayout()
		health_title_row.setContentsMargins(0, 0, 0, 0)
		health_title_row.addWidget(
			self.create_title("Здоровье")
		)
		health_title_row.addStretch()

		self.temporary_health = QLabel()
		self.temporary_health.setObjectName("temporaryHealth")
		self.temporary_health.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.temporary_health.hide()

		health_title_row.addWidget(self.temporary_health)

		health_layout.addLayout(health_title_row)

		self.health = QProgressBar()
		self.health.setObjectName("characterHealth")
		self.health.setTextVisible(True)
		self.health.setRange(0, 1)
		self.health.setValue(0)
		self.health.setFormat("0 / 0")

		health_layout.addWidget(self.health)
		layout.addWidget(health_frame)

		# Main stats

		stats_frame, stats_layout = self.create_section()

		stats_title = self.create_title("Характеристики")
		stats_title.setSizePolicy(
			QSizePolicy.Policy.Preferred,
			QSizePolicy.Policy.Fixed,
		)

		stats_layout.addWidget(stats_title)

		stats_row = QHBoxLayout()
		stats_row.setContentsMargins(0, 0, 0, 0)
		stats_row.setSpacing(Spacing.XS)

		self.stat_values: dict[str, QLabel] = {}

		stats = (
			("strength", "СИЛ", "Сила"),
			("agility", "ЛОВ", "Ловкость"),
			("intelligence", "УМ", "Интеллект"),
			("charisma", "ХАР", "Харизма"),
			("endurance", "ВЫН", "Выносливость"),
		)

		for key, short_name, full_name in stats:
			stat_frame = QFrame()
			stat_frame.setObjectName("statCell")
			stat_frame.setToolTip(full_name)

			stat_layout = QVBoxLayout(stat_frame)
			stat_layout.setContentsMargins(
				Spacing.XS,
				Spacing.SM,
				Spacing.XS,
				Spacing.SM,
			)
			stat_layout.setSpacing(Spacing.XS)

			name_label = QLabel(short_name)
			name_label.setObjectName("statName")
			name_label.setAlignment(
				Qt.AlignmentFlag.AlignCenter
			)

			value_label = QLabel("0")
			value_label.setObjectName("statValue")
			value_label.setAlignment(
				Qt.AlignmentFlag.AlignCenter
			)

			self.stat_values[key] = value_label

			stat_layout.addWidget(name_label)
			stat_layout.addWidget(value_label)

			stats_row.addWidget(
				stat_frame,
				stretch=1,
			)

		stats_layout.addLayout(stats_row)

		self.skill_table = QTreeWidget()
		self.skill_table.setObjectName("characterSkills")
		self.skill_table.setColumnCount(4)
		self.skill_table.setHeaderHidden(True)
		self.skill_table.setRootIsDecorated(False)
		self.skill_table.setIndentation(0)
		self.skill_table.setUniformRowHeights(True)

		self.skill_table.setSelectionMode(
			QAbstractItemView.SelectionMode.NoSelection
		)
		self.skill_table.setFocusPolicy(
			Qt.FocusPolicy.NoFocus
		)
		self.skill_table.setHorizontalScrollBarPolicy(
			Qt.ScrollBarPolicy.ScrollBarAlwaysOff
		)
		self.skill_table.setVerticalScrollBarPolicy(
			Qt.ScrollBarPolicy.ScrollBarAlwaysOff
		)

		header = self.skill_table.header()
		header.setStretchLastSection(False)
		header.setMinimumSectionSize(20)

		header.setSectionResizeMode(
			0,
			QHeaderView.ResizeMode.Stretch,
		)
		header.setSectionResizeMode(
			1,
			QHeaderView.ResizeMode.Fixed,
		)
		header.setSectionResizeMode(
			2,
			QHeaderView.ResizeMode.Stretch,
		)
		header.setSectionResizeMode(
			3,
			QHeaderView.ResizeMode.Fixed,
		)

		self.skill_table.setColumnWidth(1, 34)
		self.skill_table.setColumnWidth(3, 34)

		self.skill_values: dict[
			str,
			tuple[QTreeWidgetItem, int],
		] = {}

		skill_rows = (
			(
				("awareness", "Внимательность"),
				("acrobatics", "Акробатика"),
			),
			(
				("stealth", "Скрытность"),
				("athletics", "Атлетика"),
			),
			(
				("mechanics", "Механика"),
				("sleight_of_hand", "Ловкость рук"),
			),
			(
				("magic", "Магия"),
				("persuasion", "Убеждение"),
			),
			(
				("medicine", "Медицина"),
				("training", "Дрессировка"),
			),
			(
				("intimidation", "Запугивание"),
				("survival", "Выживание"),
			),
		)

		for left_skill, right_skill in skill_rows:
			left_key, left_name = left_skill
			right_key, right_name = right_skill

			item = QTreeWidgetItem(
				[
					left_name,
					"0",
					right_name,
					"0",
				]
			)

			item.setTextAlignment(
				1,
				Qt.AlignmentFlag.AlignCenter,
			)
			item.setTextAlignment(
				3,
				Qt.AlignmentFlag.AlignCenter,
			)

			self.skill_table.addTopLevelItem(item)

			self.skill_values[left_key] = (item, 1)
			self.skill_values[right_key] = (item, 3)

		self.skill_table.doItemsLayout()

		skill_table_height = (
				self.skill_table.frameWidth() * 2
		)

		for row in range(
				self.skill_table.topLevelItemCount()
		):
			row_height = (
				self.skill_table.sizeHintForRow(row)
			)

			if row_height > 0:
				skill_table_height += row_height

		self.skill_table.setFixedHeight(
			skill_table_height
		)
		self.skill_table.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Fixed,
		)

		stats_layout.addWidget(self.skill_table)
		layout.addWidget(stats_frame)

		# Character features

		features_frame, features_layout = (
			self.create_section()
		)

		features_title = self.create_title(
			"Особенности"
		)
		features_title.setSizePolicy(
			QSizePolicy.Policy.Preferred,
			QSizePolicy.Policy.Fixed,
		)

		features_layout.addWidget(
			features_title,
			alignment=Qt.AlignmentFlag.AlignTop,
		)

		self.features = QListWidget()
		self.features.setObjectName(
			"characterFeatures"
		)
		self.features.setSelectionMode(
			QAbstractItemView.SelectionMode.NoSelection
		)
		self.features.setFocusPolicy(
			Qt.FocusPolicy.NoFocus
		)
		self.features.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Expanding,
		)

		features_layout.addWidget(
			self.features,
			stretch=1,
		)

		layout.addWidget(
			features_frame,
			stretch=1,
		)

		# Party

		party_frame, party_layout = self.create_section()

		party_title = self.create_title("Пати")
		party_title.setSizePolicy(
			QSizePolicy.Policy.Preferred,
			QSizePolicy.Policy.Fixed,
		)

		party_layout.addWidget(
			party_title,
			alignment=Qt.AlignmentFlag.AlignTop,
		)

		self.party = QListWidget()
		self.party.setMinimumHeight(
			Sizes.PARTY_MIN_HEIGHT
		)
		self.party.setSizePolicy(
			QSizePolicy.Policy.Expanding,
			QSizePolicy.Policy.Expanding,
		)

		party_layout.addWidget(
			self.party,
			stretch=1,
		)

		layout.addWidget(
			party_frame,
			stretch=1,
		)

	def set_character(self, character: Character) -> None:
		self.character = character
		self.refresh()

	def refresh(self) -> None:
		if self.character is None:
			return

		self.name.setText(
			self.character.name or "Без имени"
		)
		self.race.setText(
			self.character.race or "-"
		)
		self.character_class.setText(
			self.character.character_class or "-"
		)
		self.level.setText(
			str(self.character.level)
		)

		self.update_portrait()
		self.update_health()
		self.update_stats()
		self.update_skills()

	def update_health(self) -> None:
		if self.character is None:
			return

		character_health = self.character.health

		maximum = max(
			1,
			character_health.maximum,
		)
		current = max(
			0,
			character_health.current,
		)
		temporary = max(
			0,
			character_health.temporary,
		)

		self.health.setRange(0, maximum)
		self.health.setValue(current)
		self.health.setFormat(
			f"{current} / {maximum}"
		)

		if temporary > 0:
			self.temporary_health.setText(
				f"+{temporary} врем."
			)
			self.temporary_health.setToolTip(
				f"Временное здоровье: {temporary}"
			)
			self.temporary_health.show()
		else:
			self.temporary_health.hide()

	def update_stats(self) -> None:
		if self.character is None:
			return

		for key, label in self.stat_values.items():
			value = getattr(
				self.character.stats,
				key,
			)

			label.setText(
				self.format_modifier(value)
			)

	def update_skills(self) -> None:
		if self.character is None:
			return

		for key, item_data in self.skill_values.items():
			item, column = item_data

			value = getattr(
				self.character.skills,
				key,
			)

			item.setText(
				column,
				self.format_modifier(value),
			)

	def clear(self) -> None:
		self.character = None

		self.name.setText("Персонаж не выбран")
		self.race.setText("—")
		self.character_class.setText("—")
		self.level.setText("—")

		self.health.setRange(0, 1)
		self.health.setValue(0)
		self.health.setFormat("0 / 0")

		self.temporary_health.hide()

		for label in self.stat_values.values():
			label.setText("0")

		for item, column in self.skill_values.values():
			item.setText(column, "0")

		self.portrait.clear()
		self.set_portrait_placeholder()

	def update_portrait(self) -> None:
		self.portrait.clear()

		if self.character is None:
			self.set_portrait_placeholder()
			return

		portrait_path = self.character.portrait

		if not portrait_path:
			self.set_portrait_placeholder()
			return

		path = Path(portrait_path)

		if not path.is_file():
			self.set_portrait_placeholder()
			return

		pixmap = QPixmap(str(path))

		if pixmap.isNull():
			self.set_portrait_placeholder()
			return

		scaled_pixmap = pixmap.scaled(
			self.portrait.size(),
			Qt.AspectRatioMode.KeepAspectRatioByExpanding,
			Qt.TransformationMode.SmoothTransformation,
		)

		crop_x = max(
			0,
			(scaled_pixmap.width() - self.portrait.width()) // 2,
		)
		crop_y = max(
			0,
			(scaled_pixmap.height() - self.portrait.height()) // 2,
		)

		cropped_pixmap = scaled_pixmap.copy(
			crop_x,
			crop_y,
			self.portrait.width(),
			self.portrait.height(),
		)

		self.portrait.setPixmap(cropped_pixmap)

	def set_portrait_placeholder(self) -> None:
		self.portrait.setText(
			"Портрет\nне выбран"
		)

	def create_section(self) -> tuple[QFrame, QVBoxLayout]:
		frame = QFrame()

		section_layout = QVBoxLayout(frame)
		section_layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		section_layout.setSpacing(Spacing.SM)

		return frame, section_layout

	def create_title(self, text: str) -> QLabel:
		label = QLabel(text)
		label.setObjectName("sectionTitle")

		font = QFont()
		font.setPointSize(Fonts.SUBTITLE)
		font.setBold(True)

		label.setFont(font)

		return label

	@staticmethod
	def format_modifier(value: int) -> str:
		if value > 0:
			return f"+{value}"

		return str(value)
