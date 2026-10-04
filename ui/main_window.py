from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

from config import load_config, save_config
from monitors import (
    detect_telework_config,
    disable_secondary,
    enable_secondary,
    get_display_text,
)


# Fenêtre qui affiche l'état des écrans et donne accès aux deux modes.
class MainWindow(QWidget):
    # Construire les textes, les boutons et leur disposition, puis lire l'état initial.
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
        self.config_button = QPushButton("Configurer Télétravail…")
        self.config_button.clicked.connect(self.configure_telework)

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
        layout.addWidget(self.config_button)

        self.refresh_displays()

    # Actualiser l'état affiché ou montrer une erreur de lecture.
    def refresh_displays(self):
        try:
            self.displays.setText(get_display_text())
        except (OSError, ValueError, RuntimeError) as error:
            self.displays.setText(f"Lecture des écrans impossible : {error}")

    # Proposer la configuration Windows actuelle et l’enregistrer après confirmation.
    def configure_telework(self):
        try:
            settings = detect_telework_config()

            dialog = QMessageBox(self)
            dialog.setWindowTitle("Configurer Télétravail")
            dialog.setTextFormat(Qt.TextFormat.PlainText)
            dialog.setText(
                f"Écran à conserver : {settings['primary_monitor']}\n"
                f"Écran à désactiver : {settings['secondary_monitor']}"
            )
            dialog.setInformativeText(
                "Ces réglages seront utilisés par le bouton Télétravail.\n"
                "Aucun changement d’affichage ne sera appliqué."
            )

            save_button = dialog.addButton(
                "Enregistrer", QMessageBox.ButtonRole.AcceptRole
            )
            cancel_button = dialog.addButton(
                "Annuler", QMessageBox.ButtonRole.RejectRole
            )
            dialog.setDefaultButton(cancel_button)
            dialog.exec()

            if dialog.clickedButton() is not save_button:
                return

            if detect_telework_config() != settings:
                raise RuntimeError(
                    "La configuration Windows a changé. "
                    "Rouvrez la configuration Télétravail."
                )

            save_config(settings)
            self.message.setText("Configuration Télétravail enregistrée.")

        except (OSError, ValueError, RuntimeError) as error:
            self.message.setText(f"Erreur : {error}")
        finally:
            self.refresh_displays()

    # Exécuter l'action avec la configuration, afficher son résultat et actualiser la fenêtre.
    # Bloquer les boutons pendant l'appel, puis les réactiver même en cas d'erreur.
    def run_action(self, action):
        self.work_button.setEnabled(False)
        self.personal_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.config_button.setEnabled(False)

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
            self.config_button.setEnabled(True)
