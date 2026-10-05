# Apparence de la fenêtre, d'après le design system « Display Switch » :
# un thème clair et neutre, une seule police en graisse légère, pas d'icône.

# Couleurs.
BG = "#f8f8f8"
SURFACE = "#ffffff"
BORDER = "#dedede"
BORDER_CONTROL = "#8c8c8c"
INK = "#1f1f1f"
INK_MUTED = "#5c5c5c"
CONTROL = "#ffffff"
CONTROL_HOVER = "#f0f0f0"
CONTROL_ACTIVE = "#e4e4e4"
ACCENT = "#1a5fb4"
SUCCESS = "#1e7b34"
# Bouton désactivé : l'état de repos à 50 % d'opacité, précalculé sur BG.
DISABLED_INK = "#8c8c8c"
DISABLED_BORDER = "#c2c2c2"

# Espacements, rayons et hauteurs, en pixels (Qt les adapte à la mise à l'échelle de Windows).
SPACE_1 = 4
SPACE_2 = 8
SPACE_3 = 12
SPACE_4 = 16
RADIUS_SM = 4
RADIUS_MD = 6
RADIUS_LG = 8
CONTROL_LG = 36
CONTROL_SM = 28
DOT_SIZE = 8

# Polices : Ubuntu n'étant pas installée sous Windows, Segoe UI la remplace, en graisse légère.
FONT_FAMILY = "Segoe UI"
FONT_WEIGHT = 300
TITLE_SIZE = 18
MONITOR_NAME_SIZE = 14
BODY_SIZE = 13
BUTTON_LG_SIZE = 14
BUTTON_SIZE = 13
CAPTION_SIZE = 12

# Feuille de style Qt appliquée à la fenêtre : les boîtes de dialogue ouvertes depuis elle en héritent.
# Les rôles des textes et des boutons passent par leur nom d'objet (#...) ou la propriété « size ».
STYLESHEET = f"""
* {{
    font-family: "{FONT_FAMILY}";
    font-weight: {FONT_WEIGHT};
    font-size: {BODY_SIZE}px;
}}
QWidget#mainWindow {{
    background: {BG};
}}
QDialog {{
    background: {SURFACE};
}}
QLabel {{
    color: {INK_MUTED};
}}
QLabel#title {{
    color: {INK};
    font-size: {TITLE_SIZE}px;
}}
QLabel#monitorName {{
    color: {INK};
    font-size: {MONITOR_NAME_SIZE}px;
}}
QLabel#caption {{
    font-size: {CAPTION_SIZE}px;
}}
QFrame#displays {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: {RADIUS_LG}px;
}}
QFrame#separator {{
    background: {BORDER};
}}
QLabel#dotActive {{
    background: {SUCCESS};
    border-radius: {DOT_SIZE // 2}px;
}}
QLabel#dotInactive {{
    border: 1px solid {BORDER_CONTROL};
    border-radius: {DOT_SIZE // 2}px;
}}
QPushButton {{
    background: {CONTROL};
    color: {INK};
    border: 1px solid {BORDER_CONTROL};
    border-radius: {RADIUS_SM}px;
    padding: 0 {SPACE_3}px;
    font-size: {BUTTON_SIZE}px;
}}
QPushButton[size="lg"] {{
    border-radius: {RADIUS_MD}px;
    font-size: {BUTTON_LG_SIZE}px;
}}
QPushButton:hover {{
    background: {CONTROL_HOVER};
}}
QPushButton:pressed, QPushButton:focus {{
    background: {CONTROL_ACTIVE};
    border: 2px solid {ACCENT};
}}
QPushButton:disabled {{
    color: {DISABLED_INK};
    border-color: {DISABLED_BORDER};
}}
"""
