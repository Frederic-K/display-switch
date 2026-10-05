from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from ui.theme import CONTROL_LG, CONTROL_SM, DOT_SIZE, SPACE_1, SPACE_2


# Créer un texte brut ; le nom d'objet choisit son style dans la feuille de style.
def make_label(text, object_name=""):
    label = QLabel(text)
    label.setTextFormat(Qt.TextFormat.PlainText)
    label.setObjectName(object_name)
    return label


# Créer deux boutons de même largeur sur toute la ligne, grands ou petits.
# Le clic ne donne pas le focus : le contour bleu reste réservé au clavier (Tab).
def make_button_row(labels, *, large=False):
    row = QHBoxLayout()
    row.setSpacing(SPACE_2)
    buttons = []

    for label in labels:
        button = QPushButton(label)
        button.setFixedHeight(CONTROL_LG if large else CONTROL_SM)
        button.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        if large:
            button.setProperty("size", "lg")
        row.addWidget(button, 1)
        buttons.append(button)

    return row, buttons


# Point d'état toujours accompagné de son mot : disque vert « Actif », anneau gris « Inactif ».
def make_state_badge(active):
    dot = QLabel()
    dot.setFixedSize(DOT_SIZE, DOT_SIZE)
    dot.setObjectName("dotActive" if active else "dotInactive")

    badge = QHBoxLayout()
    badge.setSpacing(SPACE_1)
    badge.addWidget(dot)
    badge.addWidget(make_label("Actif" if active else "Inactif", "caption"))
    return badge


# Une ligne d'écran : nom et détail à gauche, état à droite.
def make_monitor_row(display):
    if display["active"]:
        width, height = display["resolution"]
        role = "Principal" if display["primary"] else "Secondaire"
        detail = f"{width} × {height} — {role}"
    else:
        detail = "Résolution indisponible"

    texts = QVBoxLayout()
    texts.setSpacing(SPACE_1)
    texts.addWidget(make_label(display["name"], "monitorName"))
    texts.addWidget(make_label(detail))

    row = QHBoxLayout()
    row.addLayout(texts)
    row.addStretch()
    row.addLayout(make_state_badge(display["active"]))
    return row


# Trait horizontal clair entre deux écrans.
def make_separator():
    separator = QFrame()
    separator.setObjectName("separator")
    separator.setFixedHeight(1)
    return separator
