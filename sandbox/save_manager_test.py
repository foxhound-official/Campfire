import json
from collections.abc import Callable
from pathlib import Path
from tempfile import TemporaryDirectory

from app.core.save_manager import (
	InvalidSaveError,
	SaveManager,
	SaveNotFoundError,
	UnsupportedSaveVersionError,
)
from app.models.campaign import (
	CURRENT_SCHEMA_VERSION,
)
from sandbox.campaign_preview import (
	create_preview_campaign,
)


def assert_raises(
		error_type: type[Exception],
		action: Callable[[], object],
) -> None:
	try:
		action()

	except error_type:
		return

	raise AssertionError(
		f"Ожидалась ошибка {error_type.__name__}"
	)


def run_tests() -> None:
	manager = SaveManager()
	original_campaign = create_preview_campaign()

	with TemporaryDirectory() as directory:
		save_path = (
			Path(directory)
			/ "test_campaign.json"
		)

		manager.save_campaign(
			original_campaign,
			save_path,
		)

		assert save_path.is_file()

		temporary_path = save_path.with_suffix(
			f"{save_path.suffix}.tmp"
		)

		assert not temporary_path.exists()

		loaded_campaign = manager.load_campaign(
			save_path
		)

		assert (
			loaded_campaign.to_dict()
			== original_campaign.to_dict()
		)

		assert (
			loaded_campaign.active_scene_id
			== original_campaign.active_scene_id
		)

		raw_data = json.loads(
			save_path.read_text(
				encoding="utf-8",
			)
		)

		raw_data["schemaVersion"] = (
			CURRENT_SCHEMA_VERSION + 1
		)

		save_path.write_text(
			json.dumps(
				raw_data,
				ensure_ascii=False,
				indent=4,
			),
			encoding="utf-8",
		)

		assert_raises(
			UnsupportedSaveVersionError,
			lambda: manager.load_campaign(
				save_path
			),
		)

		save_path.write_text(
			"{ damaged json",
			encoding="utf-8",
		)

		assert_raises(
			InvalidSaveError,
			lambda: manager.load_campaign(
				save_path
			),
		)

		assert_raises(
			SaveNotFoundError,
			lambda: manager.load_campaign(
				Path(directory) / "missing.json"
			),
		)


if __name__ == "__main__":
	run_tests()
	print("Save manager checks passed")