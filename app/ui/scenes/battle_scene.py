from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class BattleScene(QWidget):

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout(self)

		layout.addWidget(
			QLabel("Battle Scene")
		)
