import argparse
import sys


def main() -> None:
    text = " ".join(sys.argv[1:])


if __name__ == "__main__":
    ################################
    ## ADD COMMAND LINE ARGUMENTS ##
    ################################
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    args = parser.parse_args()
    EXPERIMENT_NAME = f"{args.name}"
    print("test")
    input()

    # ScriptName = os.path.basename(sys.argv[0])
    # Options = {}
    # OptionsInfo = {}
    main()
