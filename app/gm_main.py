import sys

from PySide6.QtWidgets import QApplication

from app.theme.stylesheet import load_stylesheet
from app.ui.gm_window import GMWindow


def main() -> None:
	app = QApplication(sys.argv)
	app.setStyleSheet(load_stylesheet())

	window = GMWindow()
	window.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()