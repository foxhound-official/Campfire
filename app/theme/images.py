from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap


ASSETS_PATH = (
	Path(__file__).resolve().parents[1]
	/ "assets"
)

CHARACTER_PORTRAITS = "portraits/characters"
PARTY_PORTRAITS = "portraits/party"
CREATURE_PORTRAITS = "portraits/creatures"
ITEM_IMAGES = "items"


IMAGE_EXTENSIONS = (
	".png",
	".webp",
	".jpg",
	".jpeg",
)


def find_image(
		folder: str,
		image_name: str,
) -> Path | None:
	if not image_name:
		return None

	folder_path = ASSETS_PATH / folder

	for extension in IMAGE_EXTENSIONS:
		image_path = (
			folder_path
			/ f"{image_name}{extension}"
		)

		if image_path.is_file():
			return image_path

	return None


def load_cover_pixmap(
		folder: str,
		image_name: str,
		target_size: QSize,
) -> QPixmap:
	image_path = find_image(
		folder,
		image_name,
	)

	if image_path is None:
		return QPixmap()

	pixmap = QPixmap(str(image_path))

	if pixmap.isNull():
		return QPixmap()

	scaled_pixmap = pixmap.scaled(
		target_size,
		Qt.AspectRatioMode.KeepAspectRatioByExpanding,
		Qt.TransformationMode.SmoothTransformation,
	)

	crop_x = max(
		0,
		(
			scaled_pixmap.width()
			- target_size.width()
		) // 2,
	)
	crop_y = max(
		0,
		(
			scaled_pixmap.height()
			- target_size.height()
		) // 2,
	)

	return scaled_pixmap.copy(
		crop_x,
		crop_y,
		target_size.width(),
		target_size.height(),
	)