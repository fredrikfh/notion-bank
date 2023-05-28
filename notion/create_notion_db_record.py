from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
from notion_client import Client

from dotenv import load_dotenv
from notion.check_notion_db_record_exists import check_notion_db_record_exists
from notion.find_relation import find_operator
from functions.console import log


def create_notion_db_record(notion, page):
    # check if page already exists in Notion
    if (check_notion_db_record_exists(notion, page)):
        log("duplicate, skipping...", "warning")
        return

    # check if there exists a relation with operator
    operators = find_operator(
        notion, os.environ['NOTION_OPERATOR_DATABASE_ID'], page["Beskrivelse"]["title"][0]["text"]["content"])
    if len(operators) > 0:
        page["Operator"] = {"relation": [{"id": operators[0]}]}

    log(f"Sending page to Notion...", "success")
    notion.pages.create(
        parent={"database_id": os.environ['NOTION_DATABASE_ID']},
        properties=page
    )


executor = ThreadPoolExecutor(max_workers=4)


def create_notion_db_record_background(notion: Client, page: dict):
    """
    Submit the function to be executed asynchronously in the background.

    Args:
    notion: Notion client instance.
    page: Page data to be added to the Notion database.

    Returns:
    concurrent.futures.Future: Future object that represents a computation 
    that hasn't necessarily completed yet.
    """
    future = executor.submit(create_notion_db_record, notion, page)
    return future
