from PySide6.QtWidgets import (
	QDialog,
	QHBoxLayout,
	QLabel,
	QPushButton,
	QVBoxLayout,
	QWidget,
)

from app.theme.spacing import Spacing


class ActionConfirmationDialog(QDialog):

	def __init__(
			self,
			character_name: str,
			item_name: str,
			target_name: str,
			parent: QWidget | None = None,
	):
		super().__init__(parent)

		self.setObjectName(
			"actionConfirmationDialog"
		)
		self.setWindowTitle(
			"Подтверждение действия"
		)
		self.setModal(True)
		self.setMinimumWidth(420)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
		)
		layout.setSpacing(Spacing.MD)

		title_label = QLabel(
			"Подтверждение действия"
		)
		title_label.setObjectName(
			"actionConfirmationTitle"
		)

		action_label = QLabel(
			f"{character_name} хочет применить "
			f"«{item_name}»"
		)
		action_label.setObjectName(
			"actionConfirmationText"
		)
		action_label.setWordWrap(True)

		target_label = QLabel(
			f"Цель: {target_name}"
		)
		target_label.setObjectName(
			"actionConfirmationTarget"
		)
		target_label.setWordWrap(True)

		question_label = QLabel(
			"Отправить запрос ведущему?"
		)
		question_label.setObjectName(
			"actionConfirmationText"
		)

		button_layout = QHBoxLayout()
		button_layout.setSpacing(Spacing.SM)
		button_layout.addStretch()

		cancel_button = QPushButton("Отмена")
		cancel_button.setObjectName(
			"actionConfirmationCancel"
		)
		cancel_button.clicked.connect(
			self.reject
		)

		confirm_button = QPushButton(
			"Отправить"
		)
		confirm_button.setObjectName(
			"actionConfirmationConfirm"
		)
		confirm_button.setDefault(True)
		confirm_button.clicked.connect(
			self.accept
		)

		button_layout.addWidget(cancel_button)
		button_layout.addWidget(confirm_button)

		layout.addWidget(title_label)
		layout.addWidget(action_label)
		layout.addWidget(target_label)
		layout.addWidget(question_label)
		layout.addSpacing(Spacing.SM)
		layout.addLayout(button_layout)