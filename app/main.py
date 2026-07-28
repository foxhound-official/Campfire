import sys

from PySide6.QtWidgets import QApplication

from app.models.character import Character
from app.ui.main_window import MainWindow


def create_demo_character() -> Character:
	return Character(
		character_id="character-001",
		name="Элара",
		character_class="Следопыт",
		level=10,
		current_hp=84,
		max_hp=100,
		armor_class=16,
		initiative=3,
	)


def main() -> None:
	app = QApplication(sys.argv)

	character = create_demo_character()
	window = MainWindow(character)

	window.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()