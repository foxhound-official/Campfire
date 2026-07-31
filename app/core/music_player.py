from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtCore import (
	QEasingCurve,
	QObject,
	QUrl,
	QVariantAnimation,
)
from PySide6.QtMultimedia import (
	QAudioOutput,
	QMediaPlayer,
)


class MusicPlayer(QObject):

	def __init__(
			self,
			parent: QObject | None = None,
			fade_duration: int = 1800,
			volume: float = 0.25,
	):
		super().__init__(parent)

		self.fade_duration = fade_duration
		self.volume = volume

		self._players: list[QMediaPlayer] = []
		self._outputs: list[QAudioOutput] = []

		self._animations: dict[
			int,
			QVariantAnimation,
		] = {}

		self._active_index: int | None = None
		self._current_path: Path | None = None

		for _ in range(2):
			player = QMediaPlayer(self)
			output = QAudioOutput(self)

			output.setVolume(0.0)

			player.setAudioOutput(output)
			player.setLoops(
				QMediaPlayer.Loops.Infinite
			)

			self._players.append(player)
			self._outputs.append(output)

	def play(self, path: str) -> None:
		if not path:
			self.stop()
			return

		resolved_path = self._resolve_path(path)

		if not resolved_path.is_file():
			print(
				"Музыкальный файл не найден: "
				f"{resolved_path}"
			)
			self.stop()
			return

		if (
			resolved_path == self._current_path
			and self._active_index is not None
		):
			active_player = self._players[
				self._active_index
			]

			if not active_player.isPlaying():
				active_player.play()
				self._fade_volume(
					self._active_index,
					self.volume,
				)

			return

		previous_index = self._active_index

		next_index = (
			0
			if previous_index is None
			else 1 - previous_index
		)

		next_player = self._players[next_index]
		next_output = self._outputs[next_index]

		self._cancel_fade(next_index)

		next_player.stop()
		next_output.setVolume(0.0)

		next_player.setSource(
			QUrl.fromLocalFile(
				str(resolved_path)
			)
		)
		next_player.play()

		self._active_index = next_index
		self._current_path = resolved_path

		self._fade_volume(
			next_index,
			self.volume,
		)

		if previous_index is not None:
			previous_player = self._players[
				previous_index
			]

			self._fade_volume(
				previous_index,
				0.0,
				on_finished=previous_player.stop,
			)

	def stop(self) -> None:
		self._active_index = None
		self._current_path = None

		for index, player in enumerate(
				self._players
		):
			if (
				player.playbackState()
				== QMediaPlayer.PlaybackState.StoppedState
			):
				self._cancel_fade(index)
				self._outputs[index].setVolume(0.0)
				continue

			self._fade_volume(
				index,
				0.0,
				on_finished=player.stop,
			)

	def _resolve_path(self, path: str) -> Path:
		music_path = Path(path)

		if music_path.is_absolute():
			return music_path.resolve()

		project_root = Path(__file__).resolve().parents[2]

		return (project_root / music_path).resolve()

	def _fade_volume(
			self,
			index: int,
			target_volume: float,
			on_finished: Callable[[], None] | None = None,
	) -> None:
		self._cancel_fade(index)

		output = self._outputs[index]

		animation = QVariantAnimation(self)
		animation.setDuration(self.fade_duration)
		animation.setStartValue(output.volume())
		animation.setEndValue(target_volume)
		animation.setEasingCurve(
			QEasingCurve.Type.InOutCubic
		)

		def update_volume(value: object) -> None:
			output.setVolume(float(value))

		def finish_animation() -> None:
			if (
				self._animations.get(index)
				is not animation
			):
				animation.deleteLater()
				return

			output.setVolume(target_volume)
			self._animations.pop(index, None)

			if on_finished is not None:
				on_finished()

			animation.deleteLater()

		animation.valueChanged.connect(update_volume)
		animation.finished.connect(finish_animation)

		self._animations[index] = animation
		animation.start()

	def _cancel_fade(self, index: int) -> None:
		animation = self._animations.pop(
			index,
			None,
		)

		if animation is None:
			return

		animation.stop()
		animation.deleteLater()