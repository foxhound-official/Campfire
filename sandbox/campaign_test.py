from app.core.save_manager import SaveManager
from app.models.campaign import Campaign
from app.models.character import Character

campaign = Campaign(
	name="Dragon Fall"
)

campaign.characters.append(
	Character(
		name="Альрик",
		race="Человек",
		character_class="Паладин"
	)
)

campaign.characters.append(
	Character(
		name="Владосек",
		race="Демон ебучий",
		character_class="Нэ людына"
	)
)

manager = SaveManager()

manager.save_campaign(
	campaign,
	"dragon_fall.camp"
)

loaded = manager.load_campaign(
	"dragon_fall.camp"
)

print(loaded)
