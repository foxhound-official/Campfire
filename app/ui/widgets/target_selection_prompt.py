from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
	QFrame,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QSizePolicy,
)

from app.theme.spacing import Spacing


class TargetSelectionPrompt(QFrame):
	cancelled = Signal()

	def __init__(self):
		super().__init__()

		self.setObjectName("targetSelectionPrompt")
		self.setAttribute(
			Qt.WidgetAttribute.WA_StyledBackground,
			True,
		)
		self.setSizePolicy(
			QSizePolicy.Policy.Maximum,
			QSizePolicy.Policy.Fixed,
		)

		layout = QHBoxLayout(self)
		layout.setContentsMargins(
			Spacing.MD,
			Spacing.SM,
			Spacing.SM,
			Spacing.SM,
		)
		layout.setSpacing(Spacing.MD)

		self.message_label = QLabel()
		self.message_label.setObjectName(
			"targetSelectionMessage"
		)

		self.cancel_button = QPushButton(
			"Отмена"
		)
		self.cancel_button.setObjectName(
			"targetSelectionCancel"
		)
		self.cancel_button.clicked.connect(
			self.cancelled.emit
		)

		layout.addWidget(self.message_label)
		layout.addWidget(self.cancel_button)

		self.hide()

	def show_for_item(
			self,
			item_name: str,
	) -> None:
		self.message_label.setText(
			f"Выберите цель для «{item_name}»"
		)

		self.cancel_button.show()
		self.show()
		self.raise_()

	def show_status(
			self,
			message: str,
	) -> None:
		self.message_label.setText(message)
		self.cancel_button.hide()

		self.show()
		self.raise_()
