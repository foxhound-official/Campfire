from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QProgressBar,
    QSpinBox,
    QVBoxLayout,
)


class CharacterPanel(QFrame):

    WIDTH = 320

    def __init__(self):
        super().__init__()

        self.setFixedWidth(self.WIDTH)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        title = QLabel("Персонаж")
        layout.addWidget(title)

        self.portrait = QLabel("Портрет")
        self.portrait.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portrait.setFixedHeight(220)
        self.portrait.setFrameShape(QFrame.Shape.Box)

        layout.addWidget(self.portrait)

        form = QFormLayout()
        form.setSpacing(8)

        self.name = QLineEdit()
        self.race = QLineEdit()
        self.character_class = QLineEdit()

        self.level = QSpinBox()
        self.level.setMinimum(1)
        self.level.setMaximum(20)

        form.addRow("Имя", self.name)
        form.addRow("Раса", self.race)
        form.addRow("Класс", self.character_class)
        form.addRow("Уровень", self.level)

        layout.addLayout(form)

        layout.addWidget(QLabel("Здоровье"))

        self.health = QProgressBar()
        self.health.setRange(0, 100)
        self.health.setValue(100)

        layout.addWidget(self.health)

        layout.addWidget(QLabel("Эффекты"))

        self.effects = QListWidget()

        layout.addWidget(self.effects)

        layout.addStretch()