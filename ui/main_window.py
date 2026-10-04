from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config import load_config
from monitors import disable_secondary, enable_secondary, get_display_text


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Display Switch")
        self.resize(540, 300)

        self.displays = QLabel()
        self.displays.setTextFormat(Qt.TextFormat.PlainText)
        self.displays.setWordWrap(True)

        self.message = QLabel()
        self.message.setTextFormat(Qt.TextFormat.PlainText)
        self.message.setWordWrap(True)

        self.work_button = QPushButton("Télétravail")
        self.personal_button = QPushButton("Personnel")
        self.refresh_button = QPushButton("Actualiser")

        self.work_button.clicked.connect(
            lambda: self.run_action(disable_secondary)
        )
        self.personal_button.clicked.connect(
            lambda: self.run_action(enable_secondary)
        )
        self.refresh_button.clicked.connect(self.refresh_displays)

        buttons = QHBoxLayout()
        buttons.addWidget(self.work_button)
        buttons.addWidget(self.personal_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(self.displays)
        layout.addStretch()
        layout.addLayout(buttons)
        layout.addWidget(self.message)
        layout.addWidget(self.refresh_button)

        self.refresh_displays()

    def refresh_displays(self):
        try:
            self.displays.setText(get_display_text())
        except (OSError, ValueError, RuntimeError) as error:
            self.displays.setText(f"Lecture des écrans impossible : {error}")

    def run_action(self, action):
        self.work_button.setEnabled(False)
        self.personal_button.setEnabled(False)
        self.refresh_button.setEnabled(False)

        try:
            result = action(load_config())
            self.message.setText(result)
        except (OSError, ValueError, RuntimeError) as error:
            self.message.setText(f"Erreur : {error}")
        finally:
            self.refresh_displays()
            self.work_button.setEnabled(True)
            self.personal_button.setEnabled(True)
            self.refresh_button.setEnabled(True)