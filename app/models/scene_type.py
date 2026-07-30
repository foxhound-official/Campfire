from enum import Enum


class SceneType(str, Enum):
	BATTLE = "battle"
	MERCHANT = "merchant"
	NARRATION = "narration"
	PUZZLE = "puzzle"