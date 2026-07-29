from app.core.serialization import save_json, to_dict
from app.models.character import Character

character = Character(
	name="Альрик",
	race="Человек",
	character_class="Паладин"
)

print(character)

data = to_dict(character)

print(data)

save_json(
	"character.json",
	data
)
