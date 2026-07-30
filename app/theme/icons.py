from pathlib import Path

from PySide6.QtGui import QIcon


FEATURE_ICONS_PATH = (
	Path(__file__).resolve().parents[1]
	/ "assets"
	/ "icons"
	/ "features"
)

FEATURE_ICON_EXTENSIONS = (
	".svg",
	".png",
)


def load_feature_icon(icon_name: str) -> QIcon:
	if not icon_name:
		return QIcon()

	for extension in FEATURE_ICON_EXTENSIONS:
		icon_path = (
			FEATURE_ICONS_PATH
			/ f"{icon_name}{extension}"
		)

		if icon_path.is_file():
			return QIcon(str(icon_path))

	return QIcon()