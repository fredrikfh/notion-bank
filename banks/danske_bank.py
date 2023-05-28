import csv
from datetime import datetime
import os

from functions.console import log
from notion.add_relation import add_relation
from notion.create_notion_db_record import create_notion_db_record, create_notion_db_record_background
from notion.create_notion_page import create_notion_page
from notion.find_relation import find_operator

from concurrent.futures import wait

# TODO if "Fra Sparekonto AKA" set internal transfer to true
# TODO relations lookups should be cached


def create_operator(notion, database_id, name):
    new_page = {
        "Name": {"title": [{"text": {"content": name}}]}
    }
    created_page = notion.pages.create(
        parent={"database_id": database_id}, properties=new_page)
    return created_page['id']


def send_to_notion(notion, filePath):
    # open the csv in filePath

    data = []

    with open(filePath, 'r', encoding='iso-8859-1') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        for row in reader:
            data.append(row)

    # remove all whitespace from the data
    for row in data:
        for index, item in enumerate(row):
            row[index] = item.strip()

    # loop through the data except the first row
    for row in data[1:]:
        dato = datetime.strptime(row[0], "%d.%m.%Y").date()
        kategori = row[1]
        underkategori = row[2]
        tekst = row[3]
        beløp = row[4]
        saldo = row[5]
        status = row[6]
        avstemt = row[7]

        beløp = float(beløp.replace('.', '').replace(',', '.')) if (
            beløp and isinstance(beløp, str)) else 0

        # create a notion page
        page = create_notion_page(dato=dato, Beskrivelse=tekst,
                                  Beløp=beløp)

        add_relation(notion, page, "Bank", "Danske Bank")

        # add category relation
        if kategori:
            categories = find_operator(notion, kategori)
            if len(categories) > 0:
                page["Kategori"] = {"relation": [{"id": categories[0]}]}
            else:
                category_id = create_operator(notion, os.getenv(
                    'NOTION_OPERATOR_DATABASE_ID'), kategori)
                page["Kategori"] = {"relation": [{"id": category_id}]}

        # add subcategory relation
        if underkategori:
            subcategories = find_operator(notion, underkategori)
            if len(subcategories) > 0:
                page["Subkategori"] = {"relation": [{"id": subcategories[0]}]}
            else:
                category_id = create_operator(notion, os.getenv(
                    'NOTION_OPERATOR_DATABASE_ID'), underkategori)
                page["Subkategori"] = {"relation": [{"id": category_id}]}

        create_notion_db_record(notion, page)
        # create_notion_db_record_background(notion, page)
