from PySide6.QtWidgets import (
	QLabel,
	QMainWindow,
	QVBoxLayout,
	QWidget,
)

from app.theme.spacing import Spacing


class GMWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.setWindowTitle("Campfire — Ведущий")
		self.resize(1100, 700)

		self._create_ui()

	def _create_ui(self) -> None:
		central_widget = QWidget()

		layout = QVBoxLayout(central_widget)
		layout.setContentsMargins(
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
			Spacing.LG,
		)
		layout.setSpacing(Spacing.MD)

		title_label = QLabel("Панель ведущего")
		title_label.setObjectName("gmTitle")

		empty_label = QLabel(
			"Ожидающих запросов пока нет"
		)
		empty_label.setObjectName("gmEmptyState")

		layout.addWidget(title_label)
		layout.addWidget(empty_label)
		layout.addStretch()

		self.setCentralWidget(central_widget)