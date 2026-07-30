from PySide6.QtWidgets import QLabel

from app.models.item import Item
from app.ui.widgets.cards.card import Card


class ItemCard(Card):

    def __init__(self, item: Item):
        super().__init__()

        self.item = item

        self.title_label = QLabel(item.name)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setWordWrap(True)

        self.description_label = QLabel(
            item.description or "Нет описания"
        )
        self.description_label.setObjectName(
            "cardDescription"
        )
        self.description_label.setWordWrap(True)

        self.quantity_label = QLabel(
            f"Количество: {item.quantity}"
        )
        self.quantity_label.setObjectName(
            "itemQuantity"
        )
        self.quantity_label.setVisible(
            item.quantity > 1
        )

        self.content_layout.addWidget(
            self.title_label
        )
        self.content_layout.addWidget(
            self.description_label
        )
        self.content_layout.addWidget(
            self.quantity_label
        )