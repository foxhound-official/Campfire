from enum import Enum


class ActionTargetType(str, Enum):
	CHARACTER = "character"
	CREATURE = "creature"
	SCENE_OBJECT = "scene_object"