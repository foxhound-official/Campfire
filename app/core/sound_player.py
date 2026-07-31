from pathlib import Path

from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import QAbstractButton


class SoundPlayer(QObject):

	def __init__(
			self,
			parent: QObject | None = None,
	):
		super().__init__(parent)

		self._effects: dict[
			str,
			QSoundEffect,
		] = {}

	def register(
			self,
			name: str,
			path: str,
			volume: float = 0.5,
	) -> None:
		resolved_path = self._resolve_path(path)

		if not resolved_path.is_file():
			print(
				"Звуковой файл не найден: "
				f"{resolved_path}"
			)
			return

		effect = QSoundEffect(self)
		effect.setSource(
			QUrl.fromLocalFile(
				str(resolved_path)
			)
		)
		effect.setVolume(volume)

		self._effects[name] = effect

	def play(self, name: str) -> None:
		effect = self._effects.get(name)

		if effect is None:
			return

		if effect.isPlaying():
			effect.stop()

		effect.play()

	def bind_button(
			self,
			button: QAbstractButton,
			sound_name: str = "button_click",
	) -> None:
		button.clicked.connect(
			lambda _checked=False: self.play(
				sound_name
			)
		)

	def _resolve_path(self, path: str) -> Path:
		sound_path = Path(path)

		if sound_path.is_absolute():
			return sound_path.resolve()

		project_root = (
			Path(__file__).resolve().parents[2]
		)

		return (
			project_root / sound_path
		).resolve()