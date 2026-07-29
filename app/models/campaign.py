from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from dataclass_wizard import JSONWizard

from app.models.character import Character


@dataclass(slots=True)
class Campaign(JSONWizard):
	id: str = field(default_factory=lambda: str(uuid4()))

	name: str = "Новая кампания"

	characters: list[Character] = field(default_factory=list)

	notes: str = ""
