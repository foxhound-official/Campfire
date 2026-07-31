import json
from pathlib import Path

from app.models.campaign import (
	CURRENT_SCHEMA_VERSION,
	Campaign,
)


class SaveError(Exception):
	pass


class SaveNotFoundError(SaveError):
	pass


class InvalidSaveError(SaveError):
	pass


class UnsupportedSaveVersionError(SaveError):
	pass


class SaveManager:

	def save_campaign(
			self,
			campaign: Campaign,
			path: str | Path,
	) -> None:
		save_path = Path(path)

		save_path.parent.mkdir(
			parents=True,
			exist_ok=True,
		)

		temporary_path = save_path.with_suffix(
			f"{save_path.suffix}.tmp"
		)

		try:
			json_data = campaign.to_json(
				indent=4,
				ensure_ascii=False,
			)

			temporary_path.write_text(
				json_data,
				encoding="utf-8",
			)

			temporary_path.replace(save_path)

		except Exception as error:
			self._remove_temporary_file(
				temporary_path
			)

			raise SaveError(
				"Не удалось сохранить кампанию: "
				f"{save_path}"
			) from error

	def load_campaign(
			self,
			path: str | Path,
	) -> Campaign:
		save_path = Path(path)

		try:
			json_data = save_path.read_text(
				encoding="utf-8",
			)

		except FileNotFoundError as error:
			raise SaveNotFoundError(
				"Файл сохранения не найден: "
				f"{save_path}"
			) from error

		except OSError as error:
			raise SaveError(
				"Не удалось прочитать сохранение: "
				f"{save_path}"
			) from error

		try:
			raw_data = json.loads(json_data)

		except json.JSONDecodeError as error:
			raise InvalidSaveError(
				"Файл сохранения содержит "
				"повреждённый JSON"
			) from error

		if not isinstance(raw_data, dict):
			raise InvalidSaveError(
				"Корнем файла сохранения "
				"должен быть JSON-объект"
			)

		self._validate_schema_version(raw_data)

		try:
			return Campaign.from_dict(raw_data)

		except Exception as error:
			raise InvalidSaveError(
				"Структура сохранения не "
				"соответствует модели Campaign"
			) from error

	def _validate_schema_version(
			self,
			raw_data: dict,
	) -> None:
		schema_version = raw_data.get(
			"schemaVersion",
			raw_data.get(
				"schema_version",
				1,
			),
		)

		if (
			isinstance(schema_version, bool)
			or not isinstance(schema_version, int)
		):
			raise InvalidSaveError(
				"Версия схемы должна быть "
				"целым числом"
			)

		if schema_version != CURRENT_SCHEMA_VERSION:
			raise UnsupportedSaveVersionError(
				"Неподдерживаемая версия "
				f"сохранения: {schema_version}. "
				"Текущая версия приложения: "
				f"{CURRENT_SCHEMA_VERSION}"
			)

	def _remove_temporary_file(
			self,
			temporary_path: Path,
	) -> None:
		try:
			temporary_path.unlink(
				missing_ok=True
			)
		except OSError:
			pass