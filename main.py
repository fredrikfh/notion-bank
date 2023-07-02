import os
import sys

from dotenv import load_dotenv
from notion_client import Client
from banks.amex import main as amex

from banks.danske_bank import main as danske_bank
from banks.dnb import main as dnb
from functions.check_valid_cli_args import main as check_valid_cli_args
from functions.process_statement import process_statement

BANKS = ["dnb", "nordea", "danske", "amex"]

check_valid_cli_args()
load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))


if len(sys.argv) == 3:
    FILE_PATH = sys.argv[1]
    BANK_TYPE = sys.argv[2]

    bank_functions = {
        'dnb': dnb,
        'danske': danske_bank,
        'amex': amex,
    }

    if BANK_TYPE in bank_functions:
        bank_functions[BANK_TYPE](notion, FILE_PATH)
    else:
        print(f"Unsupported bank type: {BANK_TYPE}")

else:
    FOLDER_PATH = "./bank_statements"
    ALLOWED_EXTENSIONS = [".csv", ".txt"]

    for filename in os.listdir(FOLDER_PATH):
        if any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
            file_path = os.path.join(FOLDER_PATH, filename)
            process_statement(notion, file_path)
