from PySide6.QtWidgets import QStackedWidget, QWidget


class SceneContainer(QStackedWidget):

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

    def add_scene(self, scene: QWidget) -> None:
        self.addWidget(scene)

    def show_scene(self, scene: QWidget) -> None:
        index = self.indexOf(scene)

        if index == -1:
            self.add_scene(scene)
            index = self.indexOf(scene)

        self.setCurrentIndex(index)