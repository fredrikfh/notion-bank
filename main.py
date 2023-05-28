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
filePath = os.sys.argv[1]
bankType = os.sys.argv[2]

if bankType == "dnb":
    dnb_send_to_notion(notion, filePath)

elif bankType == "danske":
    danske_bank_send_to_notion(notion, filePath)

elif bankType == "amex":
    amex_send_to_notion(notion, filePath)
