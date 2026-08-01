from app.models.campaign import Campaign
from app.models.character import Character
from app.models.character_feature import CharacterFeature
from app.models.character_skills import CharacterSkills
from app.models.character_stats import CharacterStats
from app.models.creature import Creature
from app.models.health import Health
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType


def create_preview_campaign() -> Campaign:
	scenes = [
		SceneData(
			scene_type=SceneType.NARRATION,
			title="У костра",
			description=(
				"Герои отдыхают у костра перед "
				"дорогой через тёмный лес."
			),
			music="forest_ambient.mp3",
		),
		SceneData(
			scene_type=SceneType.BATTLE,
			title="Засада в лесу",
			description=(
				"На тропе появляются противники. "
				"Начинается бой."
			),
			music="forest_battle.mp3",
			creatures=[
				Creature(
					name="Гоблин",
					portrait="creature_goblin",
					health=Health(
						current=7,
						maximum=10,
					),
				),
				Creature(
					name="Орк",
					portrait="creature_orc",
					health=Health(
						current=18,
						maximum=24,
						temporary=3,
					),
				),
				Creature(
					name="Волк",
					portrait="creature_wolf",
					health=Health(
						current=9,
						maximum=12,
					),
				),
			],
		),
		SceneData(
			scene_type=SceneType.MERCHANT,
			title="Лавка странника",
			description=(
				"Перед героями открывается небольшая "
				"лавка бродячего торговца."
			),
		),
		SceneData(
			scene_type=SceneType.PUZZLE,
			title="Каменная дверь",
			description=(
				"Проход закрыт древней дверью "
				"с неизвестным механизмом."
			),
		),
	]

	return Campaign(
		name="Предпросмотр интерфейса",
		characters=[
			Character(
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
							"Альрик обрушивает огонь на выбранную "
							"область и наносит урон всем противникам."
						),
					),
					CharacterFeature(
						title="Командное лечение",
						icon_name="team_healing",
						description=(
							"Восстанавливает здоровье союзникам "
							"и помогает удержать строй."
						),
					),
				],
			),
			Character(
				name="Мира",
				portrait="character_mira",
				party_portrait="party_mira",
				character_class="Следопыт",
				level=3,
				health=Health(
					current=16,
					maximum=16,
				),
				stats=CharacterStats(
					strength=-1,
					agility=3,
					intelligence=1,
					charisma=0,
					endurance=1,
				),
				skills=CharacterSkills(
					awareness=5,
					stealth=4,
					mechanics=1,
					magic=0,
					medicine=2,
					intimidation=-1,
					acrobatics=3,
					athletics=1,
					sleight_of_hand=2,
					persuasion=0,
					training=3,
					survival=5,
				),
				features=[
					CharacterFeature(
						title="Меткий выстрел",
						description=(
							"Прицельная атака, особенно эффективная "
							"против удалённой цели."
						),
					),
					CharacterFeature(
						title="Следопыт",
						description=(
							"Мира умеет находить следы и уверенно "
							"ориентируется в дикой местности."
						),
					),
				],
			),
			Character(
				name="Торвин",
				portrait="character_torvin",
				party_portrait="party_torvin",
				character_class="Воин",
				level=4,
				health=Health(
					current=21,
					maximum=28,
				),
				stats=CharacterStats(
					strength=4,
					agility=0,
					intelligence=-1,
					charisma=1,
					endurance=3,
				),
				skills=CharacterSkills(
					awareness=2,
					stealth=-1,
					mechanics=2,
					magic=-2,
					medicine=0,
					intimidation=5,
					acrobatics=0,
					athletics=5,
					sleight_of_hand=-1,
					persuasion=1,
					training=1,
					survival=3,
				),
				features=[
					CharacterFeature(
						title="Несокрушимый",
						description=(
							"Торвин лучше переносит тяжёлые удары "
							"и физические нагрузки."
						),
					),
					CharacterFeature(
						title="Боевой натиск",
						description=(
							"Мощная атака, способная отбросить "
							"или вывести противника из равновесия."
						),
					),
				],
			),
			Character(
				name="Элиан",
				portrait="character_elian",
				party_portrait="party_elian",
				character_class="Маг",
				level=3,
				health=Health(
					current=1,
					maximum=14,
				),
				stats=CharacterStats(
					strength=-2,
					agility=1,
					intelligence=4,
					charisma=2,
					endurance=-1,
				),
				skills=CharacterSkills(
					awareness=4,
					stealth=1,
					mechanics=0,
					magic=6,
					medicine=2,
					intimidation=0,
					acrobatics=-1,
					athletics=-2,
					sleight_of_hand=1,
					persuasion=3,
					training=0,
					survival=1,
				),
				features=[
					CharacterFeature(
						title="Магический щит",
						description=(
							"Создаёт временный барьер, поглощающий "
							"часть входящего урона."
						),
					),
					CharacterFeature(
						title="Знание тайного",
						description=(
							"Элиан распознаёт магические явления, "
							"символы и зачарованные предметы."
						),
					),
				],
			),
		],
		active_scene_id=scenes[0].id,
		scenes=scenes,
	)

