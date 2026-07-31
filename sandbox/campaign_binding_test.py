import sys

from PySide6.QtWidgets import QApplication

from app.models.campaign import Campaign
from app.models.character import Character
from app.ui.main_window import MainWindow
from app.ui.panels.character.party_member_widget import (
	PartyMemberWidget,
)


def count_party_widgets(window: MainWindow) -> int:
	party_layout = window.character_panel.party_layout

	return sum(
		isinstance(
			party_layout.itemAt(index).widget(),
			PartyMemberWidget,
		)
		for index in range(party_layout.count())
	)


def run_checks() -> None:
	app = QApplication.instance() or QApplication(sys.argv)
	window = MainWindow()

	assert window.character_panel.character is None
	assert window.character_panel.party_members == []
	assert count_party_widgets(window) == 0

	single_character = Character(name="Один")
	single_campaign = Campaign(
		characters=[single_character]
	)

	window.set_campaign(
		single_campaign,
		active_character_id=single_character.id,
	)

	assert (
		window.character_panel.character
		is single_character
	)
	assert count_party_widgets(window) == 1

	five_characters = [
		Character(name=f"Игрок {index}")
		for index in range(1, 6)
	]
	full_campaign = Campaign(
		characters=five_characters
	)

	window.set_campaign(
		full_campaign,
		active_character_id=five_characters[2].id,
	)

	assert (
		window.character_panel.character
		is five_characters[2]
	)
	assert count_party_widgets(window) == 5

	window.select_character(
		five_characters[4].id
	)

	assert (
		window.character_panel.character
		is five_characters[4]
	)

	window.close()
	app.processEvents()

	print("Campaign binding checks passed")


if __name__ == "__main__":
	run_checks()
