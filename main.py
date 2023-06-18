import os
import sys

from dotenv import load_dotenv
from notion_client import Client
from banks.amex import main as amex

from banks.danske_bank import main as danske_bank
from banks.dnb import main as dnb
from functions.check_valid_cli_args import main as check_valid_cli_args

check_valid_cli_args()
load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))
FILE_PATH = sys.argv[1]
BANK_TYPE = sys.argv[2]

if BANK_TYPE == "dnb":
    dnb(notion, FILE_PATH)

elif BANK_TYPE == "danske":
    danske_bank(notion, FILE_PATH)

elif BANK_TYPE == "amex":
    amex(notion, FILE_PATH)
