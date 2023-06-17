import os
import sys

from functions.console import log


def main():
    """
    Runs the main function.
    """

    if len(os.sys.argv) < 3:
        log("Run program like this: python3 main.py <file> <bank>", "danger")
        sys.exit()

    # make sure the program is run with a cli argument for filePath and
    # bankType (string)
    file_path = os.sys.argv[1]
    bank_type = os.sys.argv[2]

    # make sure the file path is valid
    if not os.path.isfile(file_path):
        log("The file path provided is not valid.", "danger")
        sys.exit()

    # make sure the bankType is valid
    if bank_type not in ["dnb", "nordea", "danske", "amex"]:
        log("The bank type provided is not valid.", "danger")
        sys.exit()
