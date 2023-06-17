import os
from functions.cache import get_database_data


def check_notion_db_record_exists(notion, page) -> bool:
    """
    Checks if a record exists in the Notion database
    """

    existing_record = False
    notion_database_id = os.environ['NOTION_DATABASE_ID']

    data = get_database_data(notion, notion_database_id)

    for page_record in data["results"]:

        page_record_dato = page_record["properties"]["Dato"]["date"]["start"]
        page_record_beskrivelse = page_record["properties"]["Beskrivelse"]["title"][0]["text"]["content"]
        page_record_belop = page_record["properties"]["Beløp"]["number"]

        page_dato = page["Dato"]["date"]["start"]
        page_beskrivelse = page["Beskrivelse"]["title"][0]["text"]["content"]
        page_belop = page["Beløp"]["number"]

        identical_dato = page_record_dato == page_dato
        identical_beskrivelse = page_record_beskrivelse == page_beskrivelse
        identical_belop = (page_record_belop == page_belop) or (
            abs(page_record_belop) == abs(page_belop))

        if identical_dato and identical_beskrivelse and identical_belop:
            existing_record = True
            break

    return existing_record
