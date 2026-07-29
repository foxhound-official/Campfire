from pathlib import Path

from app.models.campaign import Campaign


class SaveManager:

	def save_campaign(
			self,
			campaign: Campaign,
			path: str | Path,
	) -> None:
		path = Path(path)

		path.parent.mkdir(
			parents=True,
			exist_ok=True
		)

		path.write_text(
			campaign.to_json(indent=4, ensure_ascii=False),
			encoding="utf-8"
		)

	def load_campaign(
			self,
			path: str | Path,
	) -> Campaign:
		path = Path(path)

		return Campaign.from_json(
			path.read_text(encoding="utf-8")
		)
