import csv
from datetime import datetime

from notion_client import Client

from notion.add_relation import add_relation
from notion.create_notion_db_record import upload_concurrently
from notion.create_page import create_transaction_page


def main(notion: Client, file_path):
    transactions = get_transactions(file_path)
    pages = create_pages(transactions)
    send_to_notion(notion, pages)


def get_transactions(file_path):
    """
    Formats a csv file generated from American Express to Notion
    """
    transactions = []

    file_data = []
    with open(file_path, 'r', encoding='utf8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            file_data.append(row)

    # remove all whitespace from the data
    for row in file_data:
        for index, item in enumerate(row):
            row[index] = item.strip()

    keys = file_data[0]
    rows = file_data[1:]

    for row in rows:
        row_dict = dict(zip(keys, row))
        transactions.append(row_dict)
    return transactions


def create_pages(transactions):
    pages = []
    for element in transactions:
        dato = datetime.strptime(element['Dato'], "%m/%d/%Y").date()
        belop = -float(element['Beløp'].replace(',', '.'))
        tekst = ' '.join(element['Beskrivelse'].split())
        ref = element['Referanse']

        pages.append(create_transaction_page(
            dato=dato, description=tekst, amount=belop, reference=ref))
    return pages


def send_to_notion(notion, pages):
    for page in pages:
        add_relation(notion, page, "Bank", "American Express")
        upload_concurrently(notion, page)
