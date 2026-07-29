from __future__ import annotations

import json
from dataclasses import asdict, fields, is_dataclass
from pathlib import Path
from typing import Any, Type, TypeVar

T = TypeVar("T")


def to_dict(obj: Any) -> dict:
	if not is_dataclass(obj):
		raise TypeError(f"{type(obj).__name__} is not a dataclass")

	return asdict(obj)


def from_dict(cls: Type[T], data: dict) -> T:
	field_names = {field.name for field in fields(cls)}

	filtered = {
		key: value
		for key, value in data.items()
		if key in field_names
	}

	return cls(**filtered)


def save_json(path: str | Path, data: dict) -> None:
	path = Path(path)

	path.parent.mkdir(parents=True, exist_ok=True)

	with path.open("w", encoding="utf-8") as file:
		json.dump(
			data,
			file,
			ensure_ascii=False,
			indent=4
		)


def load_json(path: str | Path) -> dict:
	path = Path(path)

	with path.open("r", encoding="utf-8") as file:
		return json.load(file)
