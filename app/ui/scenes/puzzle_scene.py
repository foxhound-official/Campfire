from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class PuzzleScene(QWidget):

	def __init__(self):
		super().__init__()

		layout = QVBoxLayout(self)

		layout.addWidget(
			QLabel("Puzzle Scene")
		)
