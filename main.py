import argparse
from monitors import print_displays


def main():
    parser = argparse.ArgumentParser(description="Display Switch")
    parser.add_argument("command", choices=["list"])
    args = parser.parse_args()

    if args.command == "list":
        print_displays()

if __name__ == "__main__":
    main()