from pathlib import Path

from app.core.serialization import (
	load_json,
	save_json,
	to_dict,
	from_dict,
)
from app.models.campaign import Campaign


class SaveManager:

	def save_campaign(
			self,
			campaign: Campaign,
			path: str | Path,
	) -> None:
		save_json(
			path,
			to_dict(campaign)
		)

	def load_campaign(
			self,
			path: str | Path,
	) -> Campaign:
		data = load_json(path)

		return from_dict(Campaign, data)
