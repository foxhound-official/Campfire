from app.models.campaign import Campaign
from app.models.creature import Creature
from app.models.scene_data import SceneData
from app.models.scene_type import SceneType


def run_checks() -> None:
	forest_scene = SceneData(
		scene_type=SceneType.BATTLE,
		title="Лесной тракт",
		background="forest_road.png",
		music="forest_battle.ogg",
		creatures=[
			Creature(name="Гоблин"),
		],
	)

	crypt_scene = SceneData(
		scene_type=SceneType.BATTLE,
		title="Затопленная крипта",
		background="flooded_crypt.png",
		music="crypt_battle.ogg",
		creatures=[
			Creature(name="Скелет"),
		],
	)

	campaign = Campaign(
		name="Проверка сцен",
		scenes=[
			forest_scene,
			crypt_scene,
		],
	)

	assert (
		campaign.get_active_scene()
		is forest_scene
	)

	campaign.set_active_scene(
		crypt_scene.id
	)

	assert (
		campaign.get_active_scene()
		is crypt_scene
	)
	assert campaign.active_scene_id == crypt_scene.id
	assert campaign.creatures is crypt_scene.creatures

	json_data = campaign.to_json()
	restored_campaign = Campaign.from_json(
		json_data
	)

	restored_scene = (
		restored_campaign.get_active_scene()
	)

	assert restored_scene.title == (
		"Затопленная крипта"
	)
	assert restored_scene.creatures[0].name == (
		"Скелет"
	)
	assert restored_scene.music == (
		"crypt_battle.ogg"
	)

	print("Scene data checks passed")


if __name__ == "__main__":
	run_checks()