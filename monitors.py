import ctypes

user32 = ctypes.WinDLL("user32.dll")

QDC_ONLY_ACTIVE_PATHS = 2
DISPLAYCONFIG_DEVICE_INFO_GET_TARGET_NAME = 2
QDC_ALL_PATHS = 1

class LUID(ctypes.Structure):
    _fields_ = [
        ("LowPart", ctypes.c_uint32),
        ("HighPart", ctypes.c_int32),
    ]

class DISPLAYCONFIG_PATH_SOURCE_INFO(ctypes.Structure):
    _fields_ = [
        ("adapterId", LUID),
        ("id", ctypes.c_uint32),
        ("modeInfoIdx", ctypes.c_uint32),
        ("statusFlags", ctypes.c_uint32),
    ]

class DISPLAYCONFIG_RATIONAL(ctypes.Structure):
    _fields_ = [
        ("Numerator", ctypes.c_uint32),
        ("Denominator", ctypes.c_uint32),
    ]


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

class DISPLAYCONFIG_PATH_INFO(ctypes.Structure):
    _fields_ = [
        ("sourceInfo", DISPLAYCONFIG_PATH_SOURCE_INFO),
        ("targetInfo", DISPLAYCONFIG_PATH_TARGET_INFO),
        ("flags", ctypes.c_uint32),
    ]

class POINTL(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int32),
        ("y", ctypes.c_int32),
    ]


class DISPLAYCONFIG_SOURCE_MODE(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_uint32),
        ("height", ctypes.c_uint32),
        ("pixelFormat", ctypes.c_uint32),
        ("position", POINTL),
    ]

class DISPLAYCONFIG_2DREGION(ctypes.Structure):
    _fields_ = [
        ("cx", ctypes.c_uint32),
        ("cy", ctypes.c_uint32),
    ]


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

class DISPLAYCONFIG_TARGET_MODE(ctypes.Structure):
    _fields_ = [
        ("targetVideoSignalInfo", DISPLAYCONFIG_VIDEO_SIGNAL_INFO),
    ]


class DISPLAYCONFIG_MODE_UNION(ctypes.Union):
    _fields_ = [
        ("targetMode", DISPLAYCONFIG_TARGET_MODE),
        ("sourceMode", DISPLAYCONFIG_SOURCE_MODE),
    ]


class DISPLAYCONFIG_MODE_INFO(ctypes.Structure):
    _fields_ = [
        ("infoType", ctypes.c_uint32),
        ("id", ctypes.c_uint32),
        ("adapterId", LUID),
        ("mode", DISPLAYCONFIG_MODE_UNION),
    ]

class DISPLAYCONFIG_DEVICE_INFO_HEADER(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_uint32),
        ("size", ctypes.c_uint32),
        ("adapterId", LUID),
        ("id", ctypes.c_uint32),
    ]


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

user32.GetDisplayConfigBufferSizes.argtypes = [
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint32),
]
user32.GetDisplayConfigBufferSizes.restype = ctypes.c_long

user32.QueryDisplayConfig.argtypes = [
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(DISPLAYCONFIG_PATH_INFO),
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(DISPLAYCONFIG_MODE_INFO),
    ctypes.POINTER(ctypes.c_uint32),
]
user32.QueryDisplayConfig.restype = ctypes.c_long

user32.DisplayConfigGetDeviceInfo.argtypes = [
    ctypes.POINTER(DISPLAYCONFIG_DEVICE_INFO_HEADER),
]
user32.DisplayConfigGetDeviceInfo.restype = ctypes.c_long

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

def print_active_displays():
    paths, modes = query_displays()

    for path in paths:
        mode_index = path.sourceInfo.modeInfoIdx

        if mode_index >= len(modes):
            raise RuntimeError("Mode d’affichage introuvable.")

        mode_info = modes[mode_index]

        if mode_info.infoType != 1:
            raise RuntimeError("Le mode reçu n’est pas un mode source.")

        source = mode_info.mode.sourceMode
        is_primary = source.position.x == 0 and source.position.y == 0
        role = "Principal" if is_primary else "Secondaire"

        name, device_path = get_monitor_identity(path.targetInfo)
        name = name or "Moniteur sans nom"

        print(
            f"{name} : "
            f"{source.width} × {source.height} — {role} — Actif"
        )
        print(f"  Identifiant : {device_path}")

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