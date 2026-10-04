# Structures et appels natifs Windows pour lire et modifier l'affichage.
# L'ordre et les types des champs ctypes doivent respecter les formats Windows.

import ctypes

# Charger la bibliothèque Windows utilisée pour gérer l'affichage.
user32 = ctypes.WinDLL("user32.dll")

# Options Windows de lecture, d'identification, de validation et d'application.
QDC_ONLY_ACTIVE_PATHS = 2
DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME = 2
QDC_ALL_PATHS = 1
DISPLAYCONFIG_PATH_ACTIVE = 1
SDC_USE_SUPPLIED_DISPLAY_CONFIG = 0x20
SDC_VALIDATE = 0x40
SDC_APPLY = 0x80
SDC_TOPOLOGY_EXTEND = 0x04

# Identifiant local d'une carte graphique.
class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.c_uint32),
        ("HighPart", ctypes.c_int32),
    ]

# Décrire la source d'un chemin d'affichage, côté carte graphique.
class DISPLAYCONFIG_PATH_SOURCE_INFO(ctypes.Structure):
    _fields_ = [
        ("adapterId", LUID),
        ("id", ctypes.c_uint32),
        ("modeInfoIdx", ctypes.c_uint32),
        ("statusFlags", ctypes.c_uint32),
    ]

# Représenter une fréquence sous forme de fraction.
class DISPLAYCONFIG_RATIONAL(ctypes.Structure):
    _fields_ = [
        ("Numerator", ctypes.c_uint32),
        ("Denominator", ctypes.c_uint32),
    ]


# Décrire la cible d'un chemin, côté sortie vers le moniteur.
class DISPLAYCONFIG_PATH_TARGET_INFO(ctypes.Structure):
    _fields_ = [
        ("adapterId", LUID),
        ("id", ctypes.c_uint32),
        ("modeInfoIdx", ctypes.c_uint32),
        ("outputTechnology", ctypes.c_uint32),
        ("rotation", ctypes.c_uint32),
        ("scaling", ctypes.c_uint32),
        ("refreshRate", DISPLAYCONFIG_RATIONAL),
        ("scanLineOrdering", ctypes.c_uint32),
        ("targetAvailable", ctypes.c_int32),
        ("statusFlags", ctypes.c_uint32),
    ]

# Réunir la source, la cible et l'état d'un chemin d'affichage.
class DISPLAYCONFIG_PATH_INFO(ctypes.Structure):
    _fields_ = [
        ("sourceInfo", DISPLAYCONFIG_PATH_SOURCE_INFO),
        ("targetInfo", DISPLAYCONFIG_PATH_TARGET_INFO),
        ("flags", ctypes.c_uint32),
    ]

# Représenter une position dans le bureau Windows.
class POINTL(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int32),
        ("y", ctypes.c_int32),
    ]


# Décrire la résolution et la position d'une surface du bureau.
class DISPLAYCONFIG_SOURCE_MODE(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_uint32),
        ("height", ctypes.c_uint32),
        ("pixelFormat", ctypes.c_uint32),
        ("position", POINTL),
    ]

# Représenter une largeur et une hauteur.
class DISPLAYCONFIG_2DREGION(ctypes.Structure):
    _fields_ = [
        ("cx", ctypes.c_uint32),
        ("cy", ctypes.c_uint32),
    ]


# Décrire les dimensions, fréquences et caractéristiques du signal vidéo.
class DISPLAYCONFIG_VIDEO_SIGNAL_INFO(ctypes.Structure):
    _fields_ = [
        ("pixelRate", ctypes.c_uint64),
        ("hSyncFreq", DISPLAYCONFIG_RATIONAL),
        ("vSyncFreq", DISPLAYCONFIG_RATIONAL),
        ("activeSize", DISPLAYCONFIG_2DREGION),
        ("totalSize", DISPLAYCONFIG_2DREGION),
        ("videoStandard", ctypes.c_uint32),
        ("scanLineOrdering", ctypes.c_uint32),
    ]

# Contenir les informations du signal envoyé au moniteur.
class DISPLAYCONFIG_TARGET_MODE(ctypes.Structure):
    _fields_ = [
        ("targetVideoSignalInfo", DISPLAYCONFIG_VIDEO_SIGNAL_INFO),
    ]


# Partager une zone mémoire entre les variantes source et cible d'un mode.
class DISPLAYCONFIG_MODE_UNION(ctypes.Union):
    _fields_ = [
        ("targetMode", DISPLAYCONFIG_TARGET_MODE),
        ("sourceMode", DISPLAYCONFIG_SOURCE_MODE),
    ]


# Associer un mode à son type et à son périphérique.
class DISPLAYCONFIG_MODE_INFO(ctypes.Structure):
    _fields_ = [
        ("infoType", ctypes.c_uint32),
        ("id", ctypes.c_uint32),
        ("adapterId", LUID),
        ("mode", DISPLAYCONFIG_MODE_UNION),
    ]

# Préciser quelle information demander à Windows et pour quel périphérique.
class DISPLAYCONFIG_DEVICE_INFO_HEADER(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint32),
        ("size", ctypes.c_uint32),
        ("adapterId", LUID),
        ("id", ctypes.c_uint32),
    ]


# Recevoir le nom du moniteur, son chemin Windows et ses informations EDID.
class DISPLAYCONFIG_TARGET_DEVICE_NAME(ctypes.Structure):
    _fields_ = [
        ("header", DISPLAYCONFIG_DEVICE_INFO_HEADER),
        ("flags", ctypes.c_uint32),
        ("outputTechnology", ctypes.c_uint32),
        ("edidManufactureId", ctypes.c_uint16),
        ("edidProductCodeId", ctypes.c_uint16),
        ("connectorInstance", ctypes.c_uint32),
        ("monitorFriendlyDeviceName", ctypes.c_wchar * 64),
        ("monitorDevicePath", ctypes.c_wchar * 128),
    ]

# Déclarer les types de l'appel qui calcule la capacité nécessaire aux tableaux.
user32.GetDisplayConfigBufferSizes.argtypes = [
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32),
]
user32.GetDisplayConfigBufferSizes.restype = ctypes.c_long

# Déclarer les types de l'appel qui remplit les chemins et les modes.
user32.QueryDisplayConfig.argtypes = [
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(DISPLAYCONFIG_PATH_INFO),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(DISPLAYCONFIG_MODE_INFO),
    ctypes.POINTER(ctypes.c_uint32),
]
user32.QueryDisplayConfig.restype = ctypes.c_long

# Déclarer les types de l'appel qui identifie un périphérique.
user32.DisplayConfigGetDeviceInfo.argtypes = [
    ctypes.POINTER(DISPLAYCONFIG_DEVICE_INFO_HEADER),
]
user32.DisplayConfigGetDeviceInfo.restype = ctypes.c_long

# Déclarer les types de l'appel qui valide ou applique une configuration.
user32.SetDisplayConfig.argtypes = [
    ctypes.c_uint32,
    ctypes.POINTER(DISPLAYCONFIG_PATH_INFO),
    ctypes.c_uint32,
    ctypes.POINTER(DISPLAYCONFIG_MODE_INFO),
    ctypes.c_uint32,
]
user32.SetDisplayConfig.restype = ctypes.c_long

# Demander les capacités nécessaires pour lire les chemins et les modes.
def get_buffer_sizes(flags=QDC_ONLY_ACTIVE_PATHS):
    path_count = ctypes.c_uint32()
    mode_count = ctypes.c_uint32()

    result = user32.GetDisplayConfigBufferSizes(
        flags,
        ctypes.byref(path_count),
        ctypes.byref(mode_count),
    )

    if result != 0:
        raise ctypes.WinError(result)

    return path_count.value, mode_count.value

# Lire ensemble les chemins et leurs modes, avec trois tentatives si la capacité change.
def query_displays(flags=QDC_ONLY_ACTIVE_PATHS):
    for _ in range(3):
        path_capacity, mode_capacity = get_buffer_sizes(flags)

        paths = (DISPLAYCONFIG_PATH_INFO * path_capacity)()
        modes = (DISPLAYCONFIG_MODE_INFO * mode_capacity)()

        path_count = ctypes.c_uint32(path_capacity)
        mode_count = ctypes.c_uint32(mode_capacity)

        result = user32.QueryDisplayConfig(
            flags,
            ctypes.byref(path_count),
            paths,
            ctypes.byref(mode_count),
            modes,
            None,
        )

        if result == 122:
            continue

        if result != 0:
            raise ctypes.WinError(result)

        return paths[:path_count.value], modes[:mode_count.value]

    raise RuntimeError("La configuration des écrans change. Réessayez.")

# Garder une entrée par cible disponible, en privilégiant son chemin actif.
def get_connected_displays():
    paths, modes = query_displays(QDC_ALL_PATHS)
    selected_paths = {}

    for path in paths:
        target = path.targetInfo

        if not target.targetAvailable:
            continue

        key = (
            target.adapterId.HighPart,
            target.adapterId.LowPart,
            target.id,
        )

        if key not in selected_paths or path.flags & DISPLAYCONFIG_PATH_ACTIVE:
            selected_paths[key] = path

    return list(selected_paths.values()), modes

# Préparer les noms, états et résolutions à afficher dans la fenêtre ou le terminal.
def get_display_text(*, include_identifiers=False):
    paths, modes = get_connected_displays()
    descriptions = []

    for path in paths:
        name, device_path = get_monitor_identity(path.targetInfo)
        name = name or "Moniteur sans nom"
        is_active = bool(path.flags & DISPLAYCONFIG_PATH_ACTIVE)

        if is_active:
            mode_index = path.sourceInfo.modeInfoIdx

            if mode_index >= len(modes):
                raise RuntimeError("Mode d’affichage introuvable.")

            mode_info = modes[mode_index]

            if mode_info.infoType != 1:
                raise RuntimeError("Le mode reçu n’est pas un mode source.")

            source = mode_info.mode.sourceMode
            is_primary = source.position.x == 0 and source.position.y == 0
            role = "Principal" if is_primary else "Secondaire"

            description = (
                f"{name}\n"
                f"{source.width} × {source.height} — {role} — Actif"
            )
        else:
            description = f"{name}\nInactif — Résolution courante indisponible"

        if include_identifiers:
            description += f"\nIdentifiant : {device_path}"

        descriptions.append(description)

    return "\n\n".join(descriptions) or "Aucun écran disponible."


# Afficher les écrans et leurs identifiants dans le terminal.
def print_displays():
    print(get_display_text(include_identifiers=True))

# Récupérer le nom lisible et le chemin Windows d'un moniteur.
def get_monitor_identity(target):
    request = DISPLAYCONFIG_TARGET_DEVICE_NAME()
    request.header.type = DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME
    request.header.size = ctypes.sizeof(request)
    request.header.adapterId = target.adapterId
    request.header.id = target.id

    result = user32.DisplayConfigGetDeviceInfo(
        ctypes.byref(request.header)
    )

    if result != 0:
        raise ctypes.WinError(result)

    return request.monitorFriendlyDeviceName, request.monitorDevicePath

# Retrouver un moniteur par nom exact et refuser les correspondances absentes ou ambiguës.
def find_monitor(paths, expected_name):
    matches = []

    for path in paths:
        name, _ = get_monitor_identity(path.targetInfo)

        if name == expected_name:
            matches.append(path)

    if not matches:
        raise RuntimeError(f"Moniteur introuvable : {expected_name}")

    if len(matches) > 1:
        raise RuntimeError(f"Plusieurs moniteurs portent le nom : {expected_name}")

    return matches[0]

# Vérifier que le moniteur configuré est actif et principal, sans changer son rôle.
def validate_primary_monitor(primary, modes):
    if not primary.flags & DISPLAYCONFIG_PATH_ACTIVE:
        raise RuntimeError("Le moniteur principal configuré est inactif.")

    mode_index = primary.sourceInfo.modeInfoIdx

    if mode_index >= len(modes):
        raise RuntimeError("Le mode du moniteur principal est introuvable.")

    mode_info = modes[mode_index]

    if mode_info.infoType != 1:
        raise RuntimeError("Le mode du moniteur principal est invalide.")

    position = mode_info.mode.sourceMode.position

    if position.x != 0 or position.y != 0:
        raise RuntimeError(
            "Le moniteur principal configuré n’est pas principal dans Windows."
        )

# Valider puis désactiver le secondaire en conservant le principal ; dry_run valide seulement.
# Relire le résultat après application et signaler les erreurs, sans retour arrière automatique.
def disable_secondary(settings, *, dry_run=False):
    paths, modes = get_connected_displays()

    primary = find_monitor(paths, settings["primary_monitor"])
    secondary = find_monitor(paths, settings["secondary_monitor"])

    if primary is secondary:
        raise RuntimeError("Les deux rôles désignent le même écran.")

    validate_primary_monitor(primary, modes)

    if not secondary.flags & DISPLAYCONFIG_PATH_ACTIVE:
        return "L’écran secondaire est déjà désactivé."

    if primary.sourceInfo.modeInfoIdx == secondary.sourceInfo.modeInfoIdx:
        raise RuntimeError("Passez en bureau étendu avant cette action.")

    remaining_paths = [
        path for path in paths
        if path.flags & DISPLAYCONFIG_PATH_ACTIVE and path is not secondary
    ]

    if not remaining_paths or not any(
        path is primary for path in remaining_paths
    ):
        raise RuntimeError("Le principal doit rester actif.")

    path_array = (DISPLAYCONFIG_PATH_INFO * len(remaining_paths))(
        *remaining_paths
    )
    mode_array = (DISPLAYCONFIG_MODE_INFO * len(modes))(*modes)

    result = user32.SetDisplayConfig(
        len(remaining_paths),
        path_array,
        len(modes),
        mode_array,
        SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_VALIDATE,
    )

    if result != 0:
        raise ctypes.WinError(result)

    if dry_run:
        return "Désactivation validée par Windows — aucun changement appliqué."

    result = user32.SetDisplayConfig(
        len(remaining_paths),
        path_array,
        len(modes),
        mode_array,
        SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_APPLY,
    )

    if result != 0:
        raise ctypes.WinError(result)

    updated_paths, updated_modes = get_connected_displays()
    updated_primary = find_monitor(
        updated_paths, settings["primary_monitor"]
    )
    validate_primary_monitor(updated_primary, updated_modes)

    updated_secondary = find_monitor(
        updated_paths, settings["secondary_monitor"]
    )

    if updated_secondary.flags & DISPLAYCONFIG_PATH_ACTIVE:
        raise RuntimeError(
            "Après application, l’écran secondaire est encore actif."
        )

    return "Écran secondaire désactivé — principal actif et conservé."

# Restaurer le bureau étendu de Windows et vérifier les deux écrans.
# En cas d'échec après la tentative d'application, tenter de rétablir l'état précédent.
def enable_secondary(settings):
    paths, modes = get_connected_displays()

    if len(paths) != 2:
        raise RuntimeError("La réactivation V1 nécessite deux écrans disponibles.")

    primary = find_monitor(paths, settings["primary_monitor"])
    secondary = find_monitor(paths, settings["secondary_monitor"])

    if primary is secondary:
        raise RuntimeError("Les deux rôles désignent le même écran.")

    validate_primary_monitor(primary, modes)

    if secondary.flags & DISPLAYCONFIG_PATH_ACTIVE:
        if primary.sourceInfo.modeInfoIdx == secondary.sourceInfo.modeInfoIdx:
            raise RuntimeError("Les écrans sont en duplication, pas en extension.")
        return "L’écran secondaire est déjà actif en bureau étendu."

    previous_paths = [
        path for path in paths
        if path.flags & DISPLAYCONFIG_PATH_ACTIVE
    ]
    path_array = (DISPLAYCONFIG_PATH_INFO * len(previous_paths))(
        *previous_paths
    )
    mode_array = (DISPLAYCONFIG_MODE_INFO * len(modes))(*modes)

    result = user32.SetDisplayConfig(
        0, None, 0, None,
        SDC_TOPOLOGY_EXTEND | SDC_VALIDATE,
    )

    if result != 0:
        raise ctypes.WinError(result)

    try:
        result = user32.SetDisplayConfig(
            0, None, 0, None,
            SDC_TOPOLOGY_EXTEND | SDC_APPLY,
        )

        if result != 0:
            raise ctypes.WinError(result)

        updated_paths, updated_modes = get_connected_displays()
        updated_primary = find_monitor(
            updated_paths, settings["primary_monitor"]
        )
        updated_secondary = find_monitor(
            updated_paths, settings["secondary_monitor"]
        )

        validate_primary_monitor(updated_primary, updated_modes)

        if not updated_secondary.flags & DISPLAYCONFIG_PATH_ACTIVE:
            raise RuntimeError("L’écran secondaire est resté inactif.")

        if (
            updated_primary.sourceInfo.modeInfoIdx
            == updated_secondary.sourceInfo.modeInfoIdx
        ):
            raise RuntimeError("Windows a activé une duplication.")

    except (OSError, RuntimeError) as error:
        restore_result = user32.SetDisplayConfig(
            len(previous_paths),
            path_array,
            len(modes),
            mode_array,
            SDC_USE_SUPPLIED_DISPLAY_CONFIG | SDC_APPLY,
        )

        if restore_result != 0:
            raise RuntimeError(
                f"Réactivation échouée : {error}. "
                f"Retour arrière échoué : {ctypes.WinError(restore_result)}"
            ) from error

        raise RuntimeError(
            f"Réactivation non confirmée : {error}. "
            "Windows a accepté le retour à la configuration précédente."
        ) from error

    return "Écran secondaire activé — bureau étendu et principal conservé."

# Proposer les réglages Télétravail à partir de deux écrans actifs en extension.
def detect_telework_config():
    paths, modes = get_connected_displays()

    if len(paths) != 2:
        raise RuntimeError("Deux écrans doivent être disponibles.")

    settings = {}

    for path in paths:
        if not path.flags & DISPLAYCONFIG_PATH_ACTIVE:
            raise RuntimeError("Activez les deux écrans avant de configurer.")

        mode_index = path.sourceInfo.modeInfoIdx

        if mode_index >= len(modes) or modes[mode_index].infoType != 1:
            raise RuntimeError("Le mode d’un écran est invalide.")

        name, _ = get_monitor_identity(path.targetInfo)

        if not name.strip():
            raise RuntimeError("Un écran ne possède pas de nom utilisable.")

        if name in settings.values():
            raise RuntimeError("Les deux écrans portent le même nom.")

        position = modes[mode_index].mode.sourceMode.position
        is_primary = position.x == 0 and position.y == 0
        role = "primary_monitor" if is_primary else "secondary_monitor"

        if role in settings:
            raise RuntimeError(
                "Un bureau étendu avec un seul écran principal est nécessaire."
            )

        settings[role] = name

    return settings