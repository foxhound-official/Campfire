from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.action_target_type import (
	ActionTargetType,
)


class ItemUseEffect(str, Enum):
	NONE = "none"
	HEAL = "heal"


@dataclass(slots=True)
class Item(JSONWizard):
	id: str = field(
		default_factory=lambda: str(uuid4())
	)

	name: str = ""
	description: str = ""
	image_name: str = ""

	quantity: int = 1

	use_effect: ItemUseEffect = ItemUseEffect.NONE
	effect_value: int = 0

	target_types: list[ActionTargetType] = field(
		default_factory=list
	)