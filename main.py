import argparse


def main():
    parser = argparse.ArgumentParser(description="Display Switch")
    parser.add_argument("command", choices=["list"])
    args = parser.parse_args()
    
    if args.command == "list":
        print("Liste des écrans à implémenter")

if __name__ == "__main__":
    main()