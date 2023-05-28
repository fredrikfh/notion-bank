# make sure the program is run with a cli argument
import os

from functions.console import log


def main():
    if len(os.sys.argv) < 3:
        log("Run program like this: python3 main.py <file> <bank>", "danger")
        exit()

    # make sure the program is run with a cli argument for filePath and bankType (string)
    filePath = os.sys.argv[1]
    bankType = os.sys.argv[2]

    # make sure the file path is valid
    if not os.path.isfile(filePath):
        log("The file path provided is not valid.", "danger")
        exit()

    # make sure the bankType is valid
    if bankType not in ["dnb", "nordea", "danske", "amex"]:
        log("The bank type provided is not valid.", "danger")
        exit()
