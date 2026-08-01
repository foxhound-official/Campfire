import sys

from PySide6.QtWidgets import QApplication

from app.data.preview_campaign import create_preview_campaign
from app.theme.gm_stylesheet import load_gm_stylesheet
from app.ui.gm_window import GMWindow


def main() -> None:
	app = QApplication(sys.argv)
	app.setStyleSheet(load_gm_stylesheet())

	campaign = create_preview_campaign()

	window = GMWindow(campaign)
	window.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()