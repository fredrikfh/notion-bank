import os

from notion.cache import get_database_data


def find_operator(notion, text):
    operators = get_database_data(notion, os.getenv(
        "NOTION_OPERATOR_DATABASE_ID")).get("results")
    matching_operator_ids = []

    for operator in operators:
        operator_name = operator["properties"]["Name"]["title"][0]["text"]["content"]
        if operator_name.lower() in text.lower():
            matching_operator_ids.append(operator["id"])

    return matching_operator_ids
