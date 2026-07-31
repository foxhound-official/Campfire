from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.action_target_type import (
	ActionTargetType,
)


class ActionType(str, Enum):
	USE_ITEM = "use_item"


class ActionRequestStatus(str, Enum):
	PENDING = "pending"
	ACCEPTED = "accepted"
	REJECTED = "rejected"
	FAILED = "failed"


@dataclass(slots=True)
class ActionRequest(JSONWizard):
	action_type: ActionType
	character_id: str

	target_type: ActionTargetType | None = None
	target_id: str | None = None
	item_id: str | None = None

	id: str = field(
		default_factory=lambda: str(uuid4())
	)

	status: ActionRequestStatus = (
		ActionRequestStatus.PENDING
	)

	status_message: str = ""