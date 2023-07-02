import csv
from banks.amex import main as amex

from banks.danske_bank import main as danske_bank
from banks.dnb import main as dnb
from functions.substring_exists import substring_exist
# from main import BANKS


def process_statement(notion, file_path):
    bank = determine_bank_type(file_path)

    if bank == "dnb":
        dnb(notion, file_path)

    elif bank == "danske":
        danske_bank(notion, file_path)

    elif bank == "amex":
        amex(notion, file_path)

    # Todo delete the file.


def read_first_line(file, encoding):
    """
    A helper function to read the first line of a file.
    """
    first_line = ""
    for line in file:
        line = line.strip()
        if line:
            first_line = line
            break
    return first_line


def get_first_line(file_path):
    """
    This function reads the first line of a file.
    It tries to open the file with 'utf-8' encoding first.
    If that fails due to a UnicodeDecodeError, it then tries 'latin-1'.
    """

    for encoding in ['utf-8', 'latin-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                if file_path.endswith((".csv", ".txt")):
                    return read_first_line(file, encoding)
        except UnicodeDecodeError:
            continue

    # If none of the encodings worked, raise an exception
    raise ValueError(
        f"Could not decode file at {file_path} with any of the tried encodings.")


def determine_bank_type(file_path):
    """
    Determines which bank the statement is from.
    """

    first_line = get_first_line(file_path)

    statements = {
        "dnb": '"Dato";"Forklaring";"Rentedato"',
        "danske": '"Dato";"Kategori";"',
        "amex": "Dato,Beskrivelse,Beløp,"
    }

    for bank, statement in statements.items():
        if bank in file_path or statement in first_line:
            return bank

    return "unknown"
