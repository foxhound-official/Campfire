from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFormLayout,
	QFrame,
	QHBoxLayout,
	QLabel,
	QProgressBar,
	QStackedWidget,
	QVBoxLayout,
	QWidget, QScrollArea,
)

from app.models.character import Character
from app.theme.images import (
	CHARACTER_PORTRAITS,
	load_cover_pixmap,
)
from app.theme.spacing import Spacing


class CharacterInspector(QFrame):

	def __init__(self):
		super().__init__()

		self.setObjectName("gmPanel")

		self._create_ui()
		self.clear()

	def _create_ui(self) -> None:
		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		layout.setSpacing(Spacing.SM)

		title_label = QLabel("Инспектор")
		title_label.setObjectName("gmPanelTitle")

		self.pages = QStackedWidget()

		empty_page = QWidget()
		empty_layout = QVBoxLayout(empty_page)

		empty_label = QLabel(
			"Выберите персонажа или существо "
			"для просмотра его параметров."
		)
		empty_label.setObjectName("gmPlaceholder")
		empty_label.setWordWrap(True)
		empty_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		empty_layout.addWidget(empty_label)

		self.character_page = (
			self._create_character_page()
		)

		self.pages.addWidget(empty_page)
		self.pages.addWidget(self.character_page)

		layout.addWidget(title_label)
		layout.addWidget(self.pages, 1)

	def _create_character_page(self) -> QWidget:
		page = QWidget()

		page_layout = QVBoxLayout(page)
		page_layout.setContentsMargins(0, 0, 0, 0)

		scroll_area = QScrollArea()
		scroll_area.setObjectName("gmInspectorScroll")
		scroll_area.setWidgetResizable(True)
		scroll_area.setFrameShape(QFrame.Shape.NoFrame)

		content = QWidget()

		layout = QVBoxLayout(content)
		layout.setContentsMargins(
			0,
			0,
			Spacing.SM,
			0,
		)
		layout.setSpacing(Spacing.MD)

		header_layout = QHBoxLayout()
		header_layout.setSpacing(Spacing.MD)

		self.portrait_label = QLabel()
		self.portrait_label.setObjectName(
			"gmInspectorPortrait"
		)
		self.portrait_label.setFixedSize(108, 144)
		self.portrait_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		identity_layout = QVBoxLayout()
		identity_layout.setSpacing(Spacing.XS)

		self.name_label = QLabel()
		self.name_label.setObjectName("gmInspectorName")
		self.name_label.setWordWrap(True)

		self.meta_label = QLabel()
		self.meta_label.setObjectName("gmCharacterMeta")
		self.meta_label.setWordWrap(True)

		self.level_label = QLabel()
		self.level_label.setObjectName("gmLevelBadge")
		self.level_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)

		identity_layout.addWidget(self.name_label)
		identity_layout.addWidget(self.meta_label)
		identity_layout.addWidget(
			self.level_label,
			0,
			Qt.AlignmentFlag.AlignLeft,
		)
		identity_layout.addStretch()

		header_layout.addWidget(self.portrait_label)
		header_layout.addLayout(identity_layout, 1)

		stats_section, self.stat_labels = (
			self._create_values_section(
				title="Основные характеристики",
				fields=(
					("strength", "Сила"),
					("agility", "Ловкость"),
					("intelligence", "Интеллект"),
					("charisma", "Харизма"),
					("endurance", "Выносливость"),
				),
			)
		)

		skills_section, self.skill_labels = (
			self._create_values_section(
				title="Доп. характеристики",
				fields=(
					("awareness", "Внимательность"),
					("stealth", "Скрытность"),
					("mechanics", "Механика"),
					("magic", "Магия"),
					("medicine", "Медицина"),
					("intimidation", "Запугивание"),
					("acrobatics", "Акробатика"),
					("athletics", "Атлетика"),
					("sleight_of_hand", "Ловкость рук"),
					("persuasion", "Убеждение"),
					("training", "Дрессировка"),
					("survival", "Выживание"),
				),
			)
		)

		layout.addLayout(header_layout)
		layout.addWidget(self._create_health_section())
		layout.addWidget(stats_section)
		layout.addWidget(skills_section)
		layout.addWidget(self._create_features_section())
		layout.addStretch()

		scroll_area.setWidget(content)
		page_layout.addWidget(scroll_area)

		return page

	def _create_health_section(self) -> QFrame:
		section = QFrame()
		section.setObjectName("gmInspectorSection")

		layout = QVBoxLayout(section)
		layout.setContentsMargins(
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.XS)

		title_label = QLabel("Здоровье")
		title_label.setObjectName(
			"gmInspectorSectionTitle"
		)

		self.health_bar = QProgressBar()
		self.health_bar.setObjectName(
			"gmInspectorHealth"
		)

		self.temporary_health_label = QLabel()
		self.temporary_health_label.setObjectName(
			"gmInspectorValue"
		)

		layout.addWidget(title_label)
		layout.addWidget(self.health_bar)
		layout.addWidget(self.temporary_health_label)

		return section

	def _create_values_section(
			self,
			title: str,
			fields: tuple[tuple[str, str], ...],
	) -> tuple[QFrame, dict[str, QLabel]]:
		section = QFrame()
		section.setObjectName("gmInspectorSection")

		layout = QVBoxLayout(section)
		layout.setContentsMargins(
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.SM)

		title_label = QLabel(title)
		title_label.setObjectName(
			"gmInspectorSectionTitle"
		)

		values_layout = QFormLayout()
		values_layout.setContentsMargins(0, 0, 0, 0)
		values_layout.setHorizontalSpacing(Spacing.MD)
		values_layout.setVerticalSpacing(Spacing.SM)

		value_labels: dict[str, QLabel] = {}

		for field_name, field_title in fields:
			caption_label = QLabel(field_title)
			caption_label.setObjectName(
				"gmInspectorCaption"
			)

			value_label = QLabel()
			value_label.setObjectName(
				"gmInspectorValue"
			)
			value_label.setAlignment(
				Qt.AlignmentFlag.AlignRight
			)

			value_labels[field_name] = value_label

			values_layout.addRow(
				caption_label,
				value_label,
			)

		layout.addWidget(title_label)
		layout.addLayout(values_layout)

		return section, value_labels

	def _create_features_section(self) -> QFrame:
		section = QFrame()
		section.setObjectName("gmInspectorSection")

		layout = QVBoxLayout(section)
		layout.setContentsMargins(
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.SM)

		title_label = QLabel("Особенности")
		title_label.setObjectName(
			"gmInspectorSectionTitle"
		)

		self.features_layout = QVBoxLayout()
		self.features_layout.setContentsMargins(
			0,
			0,
			0,
			0,
		)
		self.features_layout.setSpacing(Spacing.SM)

		layout.addWidget(title_label)
		layout.addLayout(self.features_layout)

		return section

	def _create_health_section(self) -> QFrame:
		section = QFrame()
		section.setObjectName(
			"gmInspectorSection"
		)

		layout = QVBoxLayout(section)
		layout.setContentsMargins(
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.XS)

		title_label = QLabel("Здоровье")
		title_label.setObjectName(
			"gmInspectorCaption"
		)

		self.health_bar = QProgressBar()
		self.health_bar.setObjectName(
			"gmInspectorHealth"
		)

		self.temporary_health_label = QLabel()
		self.temporary_health_label.setObjectName(
			"gmInspectorValue"
		)

		layout.addWidget(title_label)
		layout.addWidget(self.health_bar)
		layout.addWidget(
			self.temporary_health_label
		)

		return section

	def _create_stats_section(self) -> QFrame:
		section = QFrame()
		section.setObjectName(
			"gmInspectorSection"
		)

		layout = QFormLayout(section)
		layout.setContentsMargins(
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setHorizontalSpacing(Spacing.MD)
		layout.setVerticalSpacing(Spacing.SM)

		self.stat_labels: dict[str, QLabel] = {}

		for field_name, title in (
				("strength", "Сила"),
				("agility", "Ловкость"),
				("intelligence", "Интеллект"),
				("charisma", "Харизма"),
				("endurance", "Выносливость"),
		):
			caption_label = QLabel(title)
			caption_label.setObjectName(
				"gmInspectorCaption"
			)

			value_label = QLabel()
			value_label.setObjectName(
				"gmInspectorValue"
			)
			value_label.setAlignment(
				Qt.AlignmentFlag.AlignRight
			)

			self.stat_labels[field_name] = (
				value_label
			)

			layout.addRow(
				caption_label,
				value_label,
			)

		return section

	def set_character(
			self,
			character: Character,
	) -> None:
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

		identity_parts = [
			value
			for value in (
				character.race,
				character.character_class,
			)
			if value
		]

		self.name_label.setText(name)

		self.meta_label.setText(
			" • ".join(identity_parts)
			or "Раса и класс не указаны"
		)

		self.level_label.setText(
			f"Уровень {character.level}"
		)

		self.health_bar.setRange(
			0,
			maximum,
		)
		self.health_bar.setValue(current)
		self.health_bar.setFormat(
			f"{current} / {maximum} HP"
		)

		self.temporary_health_label.setText(
			"Временные HP: "
			f"{character.health.temporary}"
		)

		for field_name, label in self.skill_labels.items():
			value = getattr(
				character.skills,
				field_name,
			)
			label.setText(f"{value:+d}")

		self._set_features(character)

		pixmap = load_cover_pixmap(
			CHARACTER_PORTRAITS,
			character.portrait,
			self.portrait_label.size(),
		)

		if pixmap.isNull():
			self.portrait_label.setPixmap(
				pixmap
			)
			self.portrait_label.setText(
				name.strip()[:1].upper() or "?"
			)
		else:
			self.portrait_label.setText("")
			self.portrait_label.setPixmap(
				pixmap
			)

		self.pages.setCurrentIndex(1)

	def _set_features(
			self,
			character: Character,
	) -> None:
		while self.features_layout.count():
			item = self.features_layout.takeAt(0)
			widget = item.widget()

			if widget is not None:
				widget.deleteLater()

		if not character.features:
			empty_label = QLabel(
				"Особенности не указаны"
			)
			empty_label.setObjectName(
				"gmInspectorCaption"
			)

			self.features_layout.addWidget(
				empty_label
			)
			return

		for feature in character.features:
			feature_frame = QFrame()
			feature_frame.setObjectName(
				"gmFeatureItem"
			)

			layout = QVBoxLayout(feature_frame)
			layout.setContentsMargins(
				Spacing.SM,
				Spacing.SM,
				Spacing.SM,
				Spacing.SM,
			)
			layout.setSpacing(Spacing.XS)

			title_label = QLabel(
				feature.title or "Без названия"
			)
			title_label.setObjectName(
				"gmFeatureTitle"
			)
			title_label.setWordWrap(True)

			layout.addWidget(title_label)

			if feature.description:
				description_label = QLabel(
					feature.description
				)
				description_label.setObjectName(
					"gmFeatureDescription"
				)
				description_label.setWordWrap(True)

				layout.addWidget(
					description_label
				)

			self.features_layout.addWidget(
				feature_frame
			)

	def clear(self) -> None:
		self.pages.setCurrentIndex(0)
