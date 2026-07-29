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

print(type(loaded))

print(type(loaded.characters[0]))
print(type(loaded.characters[0].health))
print(loaded.characters[0].name)

print(type(loaded.characters[1]))
print(type(loaded.characters[1].health))
print(loaded.characters[1].name)