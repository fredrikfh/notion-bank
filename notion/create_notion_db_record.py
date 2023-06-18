import os
from concurrent.futures import ThreadPoolExecutor

from notion_client import Client
from requests.exceptions import RequestException

from functions.console import log
from notion.check_notion_db_record_exists import check_notion_db_record_exists
from notion.find_relation import find_operator


def upload_record(notion, page):
    """ check if page already exists in Notion"""
    try:
        if check_notion_db_record_exists(notion, page):
            log("duplicate (skip)", "warning")
            return

        # check if there exists a relation with operator
        operators = find_operator(
            notion, page["Beskrivelse"]["title"][0]["text"]["content"])
        if operators is not None and len(operators) > 0:
            page["Operator"] = {"relation": [{"id": operators[0]}]}

        notion.pages.create(
            parent={"database_id": os.environ['NOTION_DATABASE_ID']},
            properties=page
        )
        log("Transaction uploaded to Notion", "success")
    except RequestException as error:
        log(f"Unable to upload record: {error}", "danger")


executor = ThreadPoolExecutor(max_workers=4)


def upload_concurrently(notion: Client, page: dict):
    """
    Submit the function to be executed asynchronously in the background.

    Args:
    notion: Notion client instance.
    page: Page data to be added to the Notion database.

    Returns:
    concurrent.futures.Future: Future object that represents a computation
    that hasn't necessarily completed yet.
    """
    future = executor.submit(upload_record, notion, page)
    return future
