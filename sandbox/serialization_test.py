from app.core.save_manager import SaveManager
from app.models.campaign import Campaign
from app.models.character import Character
from app.models.character_skills import CharacterSkills
from app.models.character_stats import CharacterStats

campaign = Campaign(
	name="Dragon Fall"
)

campaign.characters.append(
	Character(
		name="Альрик",
		race="Человек",
		character_class="Паладин",
		level=4,
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
	)
)

SaveManager().save_campaign(
	campaign,
	"dragon_fall.camp"
)
