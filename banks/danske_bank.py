import csv
# import os
from datetime import datetime

from notion_client import Client
from functions.console import log

from notion.add_relation import add_relation
from notion.create_notion_db_record import upload_concurrently
from notion.create_page import create_transaction_page
# from notion.find_relation import find_operator

# TODO if "Fra Sparekonto AKA" set internal transfer to true


def main(notion, file_path):
    transactions = get_transactions(file_path)
    pages = create_pages(transactions, notion)
    send_to_notion(notion, pages)


def create_operator(notion, database_id, name):
    """ 
    Creates a new operator in the database 
    """
    new_page = {
        "Name": {"title": [{"text": {"content": name}}]}
    }
    created_page = notion.pages.create(
        parent={"database_id": database_id}, properties=new_page)
    return created_page['id']


def get_transactions(file_path):
    """
    Formats a csv file generated from American Express to Notion
    """
    transactions = []

    file_data = []
    for encoding in ['utf-8', 'latin-1', 'iso-8859-15']:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                reader = csv.reader(file, delimiter=';', quotechar='"')
                for row in reader:
                    file_data.append(row)
                # No error was raised, so break the loop
                break
        except UnicodeDecodeError:
            log(
                f"Could not decode file at {file_path} with encoding {encoding}. Trying another encoding.", "warning")
            continue

    # At this point, file_data has been filled in with the data from the file

    # If none of the encodings worked, raise an exception
    if not file_data:
        raise ValueError(
            f"Could not decode file at {file_path} with any of the tried encodings.")

    # remove all whitespace from the data
    for row in file_data:
        for index, item in enumerate(row):
            # TODO this is not perfect
            row[index] = item.replace('�', 'ø').strip()

    keys = file_data[0]
    rows = file_data[1:]

    for row in rows:
        row_dict = dict(zip(keys, row))
        transactions.append(row_dict)
    return transactions[1:]


def create_pages(transactions, notion: Client | None = None):
    pages = []
    # loop through the data except the first row
    for row in transactions:
        dato = datetime.strptime(row['Dato'], "%d.%m.%Y").date()
        kategori = row['Kategori']
        underkategori = row['Underkategori']
        tekst = row['Tekst']
        beløp = row['Beløp']

        beløp = float(beløp.replace('.', '').replace(',', '.')) if (
            beløp and isinstance(beløp, str)) else 0

        # create a notion page
        page = create_transaction_page(dato=dato, description=tekst,
                                       amount=beløp)
        # if kategori and notion:
        #     add_relation(notion, page, "Kategori", kategori)

        # if underkategori and notion:
        #     add_relation(notion, page, "Subkategori", underkategori)

        pages.append(page)

    # print()
    # print(transactions)
    # print(pages)
    return pages


def send_to_notion(notion, pages):
    """
    open the csv in filePath
    """

    for page in pages:
        add_relation(notion, page, "Bank", "Danske Bank")
        upload_concurrently(notion, page)
