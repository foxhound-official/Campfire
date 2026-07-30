from PySide6.QtWidgets import (
	QMainWindow,
	QWidget,
)
from PySide6.QtWidgets import QHBoxLayout, QStackedWidget

from app.models.character_feature import CharacterFeature
from app.models.character_skills import CharacterSkills
from app.models.character_stats import CharacterStats
from app.theme.sizes import Sizes
from app.ui.scenes import (
	BattleScene,
	MerchantScene,
	NarrationScene,
	PuzzleScene,
)
from app.models.character import Character
from app.ui.panels.character.character_panel import CharacterPanel


class MainWindow(QMainWindow):

	def __init__(self):
		super().__init__()

		self.setWindowTitle("Campfire")
		self.resize(Sizes.WINDOW_WIDTH, Sizes.WINDOW_HEIGHT)

		self._create_scenes()
		self._create_ui()

	def _create_scenes(self):
		self.scene_stack = QStackedWidget()

		self.battle_scene = BattleScene()
		self.merchant_scene = MerchantScene()
		self.narration_scene = NarrationScene()
		self.puzzle_scene = PuzzleScene()

		self.scene_stack.addWidget(self.battle_scene)
		self.scene_stack.addWidget(self.merchant_scene)
		self.scene_stack.addWidget(self.narration_scene)
		self.scene_stack.addWidget(self.puzzle_scene)

		self.scene_stack.setCurrentWidget(self.battle_scene)

	def _create_ui(self):
		central = QWidget()

		layout = QHBoxLayout(central)
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)

		self.character_panel = CharacterPanel()

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
					description="Наносит огненный урон по области.",
				),
				CharacterFeature(
					title="Командное лечение",
					icon_name="team_healing",
					description="Восстанавливает здоровье членам группы.",
				),
			],
		)

		self.character_panel.set_character(alrik)

		party = [
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
		]

		self.character_panel.set_character(alrik)
		self.character_panel.set_party(party)

		layout.addWidget(self.character_panel)
		layout.addWidget(self.scene_stack, 1)

		self.setCentralWidget(central)
