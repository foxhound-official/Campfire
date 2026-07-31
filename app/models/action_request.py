from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

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
class ActionRequest:
	action_type: ActionType
	character_id: str
	target_type: ActionTargetType
	target_id: str

	item_id: str | None = None

	id: str = field(
		default_factory=lambda: str(uuid4())
	)

	status: ActionRequestStatus = (
		ActionRequestStatus.PENDING
	)

	status_message: str = ""