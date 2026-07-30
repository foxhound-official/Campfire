import sys

from PySide6.QtWidgets import QApplication

from app.models.campaign import Campaign
from app.models.character import Character
from app.models.character_feature import CharacterFeature
from app.models.character_skills import CharacterSkills
from app.models.character_stats import CharacterStats
from app.models.creature import Creature
from app.models.health import Health
from app.models.scene_type import SceneType
from app.theme.stylesheet import load_stylesheet
from app.ui.main_window import MainWindow


def create_preview_campaign() -> Campaign:
	alrik = Character(
		name="Альрик",
		race="Человек",
		character_class="Паладин",
		level=4,
		party_portrait="alrik",
		stats=CharacterStats(
			strength=3,
			agility=-1,
			intelligence=0,
			charisma=2,
			endurance=1,
		),
		skills=CharacterSkills(
			awareness=3,
			stealth=5,
			mechanics=1,
			magic=1,
			medicine=0,
			intimidation=6,
			acrobatics=-1,
			athletics=2,
			sleight_of_hand=4,
			persuasion=3,
			training=1,
			survival=1,
		),
		features=[
			CharacterFeature(
				title="Огненный шторм",
				icon_name="fire_storm",
				description=(
					"Наносит огненный урон "
					"по области."
				),
			),
			CharacterFeature(
				title="Командное лечение",
				icon_name="team_healing",
				description=(
					"Восстанавливает здоровье "
					"членам группы."
				),
			),
		],
	)

	return Campaign(
		name="Предпросмотр интерфейса",
		active_scene=SceneType.PUZZLE,
		characters=[
			alrik,
			Character(
				name="Мира",
				character_class="Следопыт",
				level=3,
				party_portrait="mira",
			),
			Character(
				name="Торвин",
				character_class="Воин",
				level=4,
				party_portrait="torvin",
			),
			Character(
				name="Элиан",
				character_class="Маг",
				level=3,
				party_portrait="elian",
			),
		],
		creatures=[
			Creature(
				name="Гоблин",
				health=Health(
					current=7,
					maximum=7,
					temporary=3,
				),
			),
			Creature(
				name="Орк",
				health=Health(
					current=15,
					maximum=15,
				),
			),
			Creature(
				name="Скелет",
				health=Health(
					current=9,
					maximum=13,
				),
			),
			Creature(
				name="Волк",
				health=Health(
					current=8,
					maximum=11,
					temporary=3,
				),
			),
			Creature(
				name="Культист",
				health=Health(
					current=6,
					maximum=9,
				),
			),
		],
	)


def main() -> None:
	app = QApplication(sys.argv)
	app.setStyleSheet(load_stylesheet())

	campaign = create_preview_campaign()

	window = MainWindow(
		campaign=campaign,
		active_character_id=(
			campaign.characters[0].id
		),
	)
	window.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
