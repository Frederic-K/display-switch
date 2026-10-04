import argparse
import sys

from config import load_config
from monitors import check_disable, print_displays


def main():
    parser = argparse.ArgumentParser(description="Display Switch")
    parser.add_argument("command", choices=["list", "check"])
    args = parser.parse_args()

    try:
        if args.command == "list":
            print_displays()
        elif args.command == "check":
            print(check_disable(load_config()))
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())