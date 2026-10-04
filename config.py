import json
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile


# Localiser la configuration à côté du script ou de l’exécutable.
def get_config_path():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().with_name("config.json")

    return Path(__file__).resolve().with_name("config.json")


# Vérifier que les deux rôles contiennent des noms valides et différents.
def validate_config(settings):
    if not isinstance(settings, dict):
        raise ValueError("La configuration doit être un objet JSON.")

    for key in ("primary_monitor", "secondary_monitor"):
        name = settings.get(key)

        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Nom de moniteur manquant ou invalide : {key}")

    if settings["primary_monitor"] == settings["secondary_monitor"]:
        raise ValueError("Les deux moniteurs doivent avoir des noms différents.")


# Lire et valider les réglages enregistrés.
def load_config():
    with get_config_path().open(encoding="utf-8") as file:
        settings = json.load(file)

    validate_config(settings)
    return settings


# Enregistrer les réglages en remplaçant le JSON seulement après écriture complète.
def save_config(settings):
    validate_config(settings)
    config_path = get_config_path()

    with NamedTemporaryFile(dir=config_path.parent, delete=False) as file:
        temporary_path = Path(file.name)

    try:
        content = json.dumps(settings, ensure_ascii=False, indent=2)
        temporary_path.write_text(content + "\n", encoding="utf-8")
        temporary_path.replace(config_path)
    finally:
        temporary_path.unlink(missing_ok=True)