import os
from functions.console import log

from notion.cache import get_database_data


def find_operator(notion, text):
    """Find operator in Notion database."""
    operator_db = os.getenv("NOTION_OPERATOR_DATABASE_ID")
    if not operator_db:
        log("NOTION_OPERATOR_DATABASE_ID is not set", "danger")
        return None
    operators = get_database_data(notion, operator_db)

    if not operators:
        log("Unable to fetch operators from Notion database", "danger")
        return None

    results = operators.get("results")

    if not results:
        log("No operators found in Notion database", "danger")
        return None

    matching_operator_ids = []
    for operator in results:
        operator_name = operator["properties"]["Name"]["title"][0]["text"]["content"]
        if operator_name.lower() in text.lower():
            matching_operator_ids.append(operator["id"])

    return matching_operator_ids
