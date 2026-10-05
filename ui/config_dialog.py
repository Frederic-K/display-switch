from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout

from ui.theme import SPACE_1, SPACE_2, SPACE_3, SPACE_4
from ui.widgets import make_button_row, make_label

DIALOG_WIDTH = 340


# Montrer les rôles détectés et renvoyer True si l'utilisateur choisit « Enregistrer ».
# Annuler, Échap ou la fermeture de la boîte renvoient False.
def confirm_telework_config(parent, settings):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Configurer Télétravail")
    dialog.setFixedWidth(DIALOG_WIDTH)

    buttons, (save_button, cancel_button) = make_button_row(["Enregistrer", "Annuler"])
    save_button.clicked.connect(dialog.accept)
    cancel_button.clicked.connect(dialog.reject)
    # Entrée vaut Annuler, pour ne rien enregistrer par mégarde.
    cancel_button.setDefault(True)
    # Garder le focus sur la boîte à l'ouverture : aucun bouton ne paraît sélectionné.
    dialog.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
    dialog.setFocus()

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(SPACE_4, SPACE_4, SPACE_4, SPACE_4)
    layout.setSpacing(SPACE_1)
    layout.addWidget(make_label("Configurer Télétravail", "title"))
    layout.addSpacing(SPACE_2)
    layout.addWidget(make_label(f"Écran à conserver : {settings['primary_monitor']}"))
    layout.addWidget(make_label(f"Écran à désactiver : {settings['secondary_monitor']}"))
    layout.addSpacing(SPACE_2)
    layout.addWidget(make_label("Ces réglages seront utilisés par le bouton Télétravail."))
    layout.addWidget(make_label("Aucun changement d’affichage ne sera appliqué."))
    layout.addSpacing(SPACE_3)
    layout.addLayout(buttons)

    # Centrer la boîte sur la fenêtre. move() place le cadre Windows (barre de titre comprise),
    # supposé identique à celui de la fenêtre : on retire donc son épaisseur à la position du contenu.
    dialog.adjustSize()
    content = dialog.rect()
    content.moveCenter(parent.geometry().center())
    frame_offset = parent.geometry().topLeft() - parent.frameGeometry().topLeft()
    dialog.move(content.topLeft() - frame_offset)

    return dialog.exec() == QDialog.DialogCode.Accepted
