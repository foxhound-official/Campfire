import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

JSON_OPTIONS = {
	"ensure_ascii": False,
	"indent": 4,
}


def to_dict(obj: Any) -> dict:
	if not is_dataclass(obj):
		raise TypeError(f"{type(obj).__name__} is not a dataclass")

	return asdict(obj)


def save_json(path: str | Path, data: dict) -> None:
	path = Path(path)

	path.parent.mkdir(parents=True, exist_ok=True)

	with path.open("w", encoding="utf-8") as file:
		json.dump(
			data,
			file,
			**JSON_OPTIONS
		)


def load_json(path: str | Path) -> dict:
	path = Path(path)

	with path.open("r", encoding="utf-8") as file:
		return json.load(file)
