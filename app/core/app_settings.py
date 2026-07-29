from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppSettings:
	master_volume: int = 100
	music_volume: int = 100

	autosave_enabled: bool = True
	autosave_interval: int = 5

	theme: str = "dark"

	last_campaign: str = ""

	@property
	def file_path(self) -> Path:
		return Path("settings.json")
