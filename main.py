import argparse
import sys

from config import load_config
from monitors import disable_secondary, enable_secondary, print_displays


def main():
    parser = argparse.ArgumentParser(description="Display Switch")
    parser.add_argument(
    "command",
    nargs="?",
    choices=["list", "check", "disable", "enable"],
    )
    args = parser.parse_args()

    if args.command is None:
        from PySide6.QtWidgets import QApplication
        from ui.main_window import MainWindow

        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        return app.exec()

    try:
        if args.command == "list":
            print_displays()
        elif args.command == "check":
            print(disable_secondary(load_config(), dry_run=True))
        elif args.command == "disable":
            print(disable_secondary(load_config(), dry_run=False))
        elif args.command == "enable":
            print(enable_secondary(load_config()))
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())