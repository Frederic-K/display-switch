from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from config import load_config, save_config
from monitors import (
    detect_telework_config,
    disable_secondary,
    enable_secondary,
    get_displays,
)
from ui.config_dialog import confirm_telework_config
from ui.theme import SPACE_2, SPACE_3, SPACE_4, STYLESHEET
from ui.widgets import make_button_row, make_label, make_monitor_row, make_separator

WINDOW_TITLE = "Display Switch"
# Taille intérieure : 420 pixels de large, hauteur prévue pour deux écrans et un message.
WINDOW_WIDTH = 420
WINDOW_HEIGHT = 300


# Fenêtre qui affiche l'état des écrans et donne accès aux deux modes.
# Les blocs s'empilent de haut en bas, séparés de SPACE_3 ; l'apparence vient de theme.py.
class MainWindow(QWidget):
    # Construire les textes, les boutons et leur disposition, puis lire l'état initial.
    def __init__(self):
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)
        # Un QWidget simple ne peint son fond que si on le lui demande.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setObjectName("mainWindow")
        self.setStyleSheet(STYLESHEET)
        self.setMinimumSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Bloc des écrans : son contenu est reconstruit à chaque actualisation.
        self.displays = QFrame()
        self.displays.setObjectName("displays")
        self.displays_layout = QVBoxLayout(self.displays)
        self.displays_layout.setContentsMargins(SPACE_3, SPACE_2, SPACE_3, SPACE_2)
        self.displays_layout.setSpacing(SPACE_2)

        # Ligne d'état centrée ; vide, elle garde sa hauteur pour que rien ne bouge.
        self.message = make_label(" ")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setWordWrap(True)

        mode_buttons, (self.work_button, self.personal_button) = make_button_row(
            ["Télétravail", "Personnel"], large=True
        )
        other_buttons, (self.refresh_button, self.config_button) = make_button_row(
            ["Actualiser", "Configurer Télétravail…"]
        )
        self.buttons = [
            self.work_button,
            self.personal_button,
            self.refresh_button,
            self.config_button,
        ]

        self.work_button.clicked.connect(
            lambda: self.run_action(disable_secondary)
        )
        self.personal_button.clicked.connect(
            lambda: self.run_action(enable_secondary)
        )
        self.refresh_button.clicked.connect(self.refresh_displays)
        self.config_button.clicked.connect(self.configure_telework)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACE_4, SPACE_4, SPACE_4, SPACE_4)
        layout.setSpacing(SPACE_3)
        layout.addWidget(make_label(WINDOW_TITLE, "title"))
        layout.addWidget(self.displays)
        layout.addLayout(mode_buttons)
        layout.addWidget(self.message)
        layout.addLayout(other_buttons)
        layout.addStretch()

        # Garder le focus sur la fenêtre à l'ouverture : aucun bouton ne paraît sélectionné.
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setFocus()

        self.refresh_displays()

    # Vider le bloc des écrans puis y remettre une ligne par écran, ou un message de lecture.
    def refresh_displays(self):
        while self.displays_layout.count():
            clear_item(self.displays_layout.takeAt(0))

        try:
            displays = get_displays()
        except (OSError, ValueError, RuntimeError) as error:
            self.displays_layout.addWidget(
                make_label(f"Lecture des écrans impossible : {error}")
            )
            return

        if not displays:
            self.displays_layout.addWidget(make_label("Aucun écran disponible."))

        for index, display in enumerate(displays):
            if index > 0:
                self.displays_layout.addWidget(make_separator())
            self.displays_layout.addLayout(make_monitor_row(display))

    # Proposer la configuration Windows actuelle et l’enregistrer après confirmation.
    def configure_telework(self):
        try:
            settings = detect_telework_config()

            if not confirm_telework_config(self, settings):
                return

            # Revérifier Windows au moment d'enregistrer : les rôles ont pu changer entre-temps.
            if detect_telework_config() != settings:
                raise RuntimeError(
                    "La configuration Windows a changé. "
                    "Rouvrez « Configurer Télétravail… »."
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
        for button in self.buttons:
            button.setEnabled(False)

        try:
            self.message.setText(action(load_config()))
        except (OSError, ValueError, RuntimeError) as error:
            self.message.setText(f"Erreur : {error}")
        finally:
            self.refresh_displays()
            for button in self.buttons:
                button.setEnabled(True)


# Supprimer un élément retiré d'une disposition : un widget, ou une disposition et son contenu.
def clear_item(item):
    if item.widget():
        item.widget().deleteLater()
    elif item.layout():
        while item.layout().count():
            clear_item(item.layout().takeAt(0))
        item.layout().deleteLater()
