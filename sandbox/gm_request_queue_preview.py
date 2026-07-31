import sys

from PySide6.QtWidgets import (
	QApplication,
	QMainWindow,
)

from app.models.action_request import (
	ActionRequest,
	ActionType,
)
from app.models.campaign import Campaign
from app.models.character import Character
from app.models.health import Health
from app.models.item import (
	Item,
	ItemUseEffect,
)
from app.systems.actions.action_processor import (
	ActionProcessor,
)
from app.systems.actions.action_request_queue import (
	ActionRequestQueue,
)
from app.theme.stylesheet import load_stylesheet
from app.ui.panels.action_requests.action_request_panel import (
	ActionRequestPanel,
)


def create_preview_window() -> QMainWindow:
	potion = Item(
		name="Лечебное зелье",
		description="Восстанавливает 5 здоровья",
		quantity=2,
		use_effect=ItemUseEffect.HEAL,
		effect_value=5,
	)

	alrik = Character(
		name="Альрик",
		inventory=[potion],
	)

	mira = Character(
		name="Мира",
		health=Health(
			current=4,
			maximum=12,
		),
	)

	campaign = Campaign(
		characters=[
			alrik,
			mira,
		],
	)

	request_queue = ActionRequestQueue()
	processor = ActionProcessor(campaign)

	for _ in range(2):
		request_queue.submit(
			ActionRequest(
				action_type=ActionType.USE_ITEM,
				character_id=alrik.id,
				target_id=mira.id,
				item_id=potion.id,
			)
		)

	panel = ActionRequestPanel(
		campaign=campaign,
		request_queue=request_queue,
		processor=processor,
	)

	window = QMainWindow()
	window.setWindowTitle(
		"Campfire — запросы игроков"
	)
	window.resize(520, 640)
	window.setCentralWidget(panel)

	return window


def main() -> int:
	app = QApplication(sys.argv)
	app.setStyleSheet(load_stylesheet())

	window = create_preview_window()
	window.show()

	return app.exec()


if __name__ == "__main__":
	sys.exit(main())