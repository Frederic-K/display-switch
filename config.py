import sys
import json
from pathlib import Path


def load_config():
    if getattr(sys, "frozen", False):
        config_path = Path(sys.executable).resolve().with_name("config.json")
    else:
        config_path = Path(__file__).resolve().with_name("config.json")

    with config_path.open(encoding="utf-8") as file:
        settings = json.load(file)

    if not isinstance(settings, dict):
        raise ValueError("La configuration doit être un objet JSON.")

    for key in ("primary_monitor", "secondary_monitor"):
        name = settings.get(key)

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Nom de moniteur manquant ou invalide : {key}")

    if settings["primary_monitor"] == settings["secondary_monitor"]:
        raise ValueError("Les deux moniteurs doivent avoir des noms différents.")

    return settings