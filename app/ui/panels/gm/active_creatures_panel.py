from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QScrollArea,
	QVBoxLayout,
	QWidget,
)

from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.theme.spacing import Spacing
from app.ui.panels.gm.creature_card import (
	GMCreatureCard,
)


class ActiveCreaturesPanel(QFrame):
	def __init__(self):
		super().__init__()

		self.setObjectName("gmPanel")
		self._create_ui()

	def _create_ui(self) -> None:
		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
			Spacing.MD,
		)
		layout.setSpacing(Spacing.SM)

		self.title_label = QLabel(
			"Существа на сцене"
		)
		self.title_label.setObjectName(
			"gmPanelTitle"
		)

		self.empty_label = QLabel()
		self.empty_label.setObjectName(
			"gmPlaceholder"
		)
		self.empty_label.setAlignment(
			Qt.AlignmentFlag.AlignCenter
		)
		self.empty_label.setWordWrap(True)

		self.scroll_area = QScrollArea()
		self.scroll_area.setObjectName(
			"gmCreatureScroll"
		)
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setFrameShape(
			QFrame.Shape.NoFrame
		)
		self.scroll_area.setVerticalScrollBarPolicy(
			Qt.ScrollBarPolicy.ScrollBarAlwaysOff
		)
		self.scroll_area.setHorizontalScrollBarPolicy(
			Qt.ScrollBarPolicy.ScrollBarAsNeeded
		)

		self.cards_container = QWidget()
		self.cards_container.setObjectName(
			"gmCreatureList"
		)

		self.cards_layout = QHBoxLayout(
			self.cards_container
		)
		self.cards_layout.setContentsMargins(
			0,
			0,
			0,
			0,
		)
		self.cards_layout.setSpacing(Spacing.SM)
		self.cards_layout.addStretch()

		self.scroll_area.setWidget(
			self.cards_container
		)

		layout.addWidget(self.title_label)
		layout.addWidget(self.empty_label, 1)
		layout.addWidget(self.scroll_area, 1)

	def set_scene(
			self,
			scene: SceneData,
	) -> None:
		self._clear_cards()

		if scene.scene_type != SceneType.BATTLE:
			self.title_label.setText(
				"Существа на сцене"
			)
			self.empty_label.setText(
				"В этой сцене существа не используются"
			)
			self.empty_label.show()
			self.scroll_area.hide()
			return

		creatures = scene.creatures

		self.title_label.setText(
			f"Существа на сцене · {len(creatures)}"
		)

		for creature in creatures:
			card = GMCreatureCard(creature)

			self.cards_layout.insertWidget(
				self.cards_layout.count() - 1,
				card,
				)

		has_creatures = bool(creatures)

		self.empty_label.setText(
			"На боевой сцене пока нет существ"
		)
		self.empty_label.setVisible(
			not has_creatures
		)
		self.scroll_area.setVisible(
			has_creatures
		)

	def _clear_cards(self) -> None:
		while self.cards_layout.count() > 1:
			item = self.cards_layout.takeAt(0)
			widget = item.widget()

			if widget is not None:
				widget.deleteLater()