import os

from dotenv import load_dotenv
from notion_client import Client
from banks.amex import send_to_notion as amex_send_to_notion

from banks.danske_bank import send_to_notion as danske_bank_send_to_notion
from banks.dnb import send_to_notion as dnb_send_to_notion
from functions.check_valid_cli_args import main as check_valid_cli_args

check_valid_cli_args()
load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))
FILE_PATH = os.sys.argv[1]
BANK_TYPE = os.sys.argv[2]

if BANK_TYPE == "dnb":
    dnb_send_to_notion(notion, FILE_PATH)

elif BANK_TYPE == "danske":
    danske_bank_send_to_notion(notion, FILE_PATH)

elif BANK_TYPE == "amex":
    amex_send_to_notion(notion, FILE_PATH)
