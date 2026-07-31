import sys

from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication

from app.models.action_target_type import ActionTargetType
from app.models.campaign import Campaign
from app.models.character import Character
from app.models.character_feature import CharacterFeature
from app.models.character_skills import CharacterSkills
from app.models.character_stats import CharacterStats
from app.models.creature import Creature
from app.models.health import Health
from app.models.item import Item
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType
from app.theme.stylesheet import load_stylesheet
from app.ui.main_window import MainWindow


def create_preview_campaign() -> Campaign:
	alrik = Character(
		name="Альрик",
		portrait="character_alrik",
		party_portrait="party_alrik",
		race="Человек",
		character_class="Паладин",
		level=4,
		health=Health(
			current=18,
			maximum=24,
		),
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
					"Наносит огненный урон по области."
				),
			),
			CharacterFeature(
				title="Командное лечение",
				icon_name="team_healing",
				description=(
					"Восстанавливает здоровье членам группы."
				),
			),
		],
		inventory_capacity=6,
		inventory=[
			Item(
				name="Лечебное зелье",
				description=(
					"Восстанавливает здоровье персонажа."
				),
				image_name="item_healing_potion",
				quantity=2,
				target_types=[
					ActionTargetType.CHARACTER,
					ActionTargetType.CREATURE,
				],
			),
			Item(
				name="Серебряный ключ",
				description=(
					"Холодный ключ с гербом крепости."
				),
				image_name="item_silver_key",
				target_types=[
					ActionTargetType.CREATURE,
				],
			),
			Item(
				name="Свиток огненной волны",
				description=(
					"Одноразовое заклинание по области."
				),
				image_name="item_fire_wave_scroll",
				target_types=[
					ActionTargetType.CHARACTER,
				],
			),
		],
	)
	return Campaign(
		name="Предпросмотр интерфейса",
		characters=[
			alrik,
			Character(
				name="Мира",
				portrait="mira",
				party_portrait="party_mira",
				character_class="Следопыт",
				level=3,
				health=Health(
					current=16,
					maximum=16,
				),
			),
			Character(
				name="Торвин",
				portrait="torvin",
				party_portrait="party_torvin",
				character_class="Воин",
				level=4,
				health=Health(
					current=21,
					maximum=28,
				),
			),
			Character(
				name="Элиан",
				portrait="elian",
				party_portrait="party_elian",
				character_class="Маг",
				level=3,
				health=Health(
					current=1,
					maximum=14,
				),
			),
		],
		creatures=[
			Creature(
				name="Гоблин",
				portrait="creature_goblin",
				health=Health(
					current=7,
					maximum=7,
					temporary=4,
				),
			),
			Creature(
				name="Орк",
				portrait="creature_orc",
				health=Health(
					current=15,
					maximum=15,
				),
			),
			Creature(
				name="Скелет",
				portrait="creature_skeleton",
				health=Health(
					current=9,
					maximum=13,
				),
			),
			Creature(
				name="Волк",
				portrait="creature_wolf",
				health=Health(
					current=8,
					maximum=11,
					temporary=3,
				),
			),
			Creature(
				name="Культист",
				portrait="creature_cultist",
				health=Health(
					current=6,
					maximum=9,
				),
			),
		],
		scenes=[
			SceneData(
				scene_type=SceneType.NARRATION,
				title="Лес перед бурей",
				music=(
					"app/assets/music/"
					"forest_ambient.ogg"
				),
				description=(
					"Дорога постепенно исчезает под корнями "
					"старых деревьев. Впереди слышится треск "
					"веток, а между стволами мелькают силуэты."
				),
			),
			SceneData(
				scene_type=SceneType.BATTLE,
				title="Засада на лесном тракте",
				music=(
					"app/assets/music/"
					"forest_battle.ogg"
				),
				creatures=[
					Creature(
						name="Гоблин",
						portrait="creature_goblin",
						health=Health(
							current=7,
							maximum=7,
						),
					),
					Creature(
						name="Орк",
						portrait="creature_orc",
						health=Health(
							current=15,
							maximum=15,
						),
					),
					Creature(
						name="Волк",
						portrait="creature_wolf",
						health=Health(
							current=8,
							maximum=11,
						),
					),
				],
			),
		],
	)


def main() -> None:
	app = QApplication(sys.argv)
	app.setStyleSheet(load_stylesheet())

	campaign = create_preview_campaign()
	window = MainWindow(
		campaign=campaign,
		active_character_id=campaign.characters[0].id,
	)
	narration_scene, battle_scene = campaign.scenes

	narration_shortcut = QShortcut(
		QKeySequence("1"),
		window,
	)
	narration_shortcut.activated.connect(
		lambda: window.set_scene(
			narration_scene.id
		)
	)

	battle_shortcut = QShortcut(
		QKeySequence("2"),
		window,
	)
	battle_shortcut.activated.connect(
		lambda: window.set_scene(
			battle_scene.id
		)
	)

	window.setWindowTitle(
		"Campfire — 1: история, 2: бой"
	)

	window.show()

	sys.exit(app.exec())


if __name__ == "__main__":
	main()
