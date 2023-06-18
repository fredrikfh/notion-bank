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
    Formats a csv file generated from DNB to Notion
    """
    transactions = []

    file_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        for row in reader:
            file_data.append(row)

    keys = file_data[0]
    rows = file_data[1:]

    for row in rows:
        row_dict = dict(zip(keys, row))
        transactions.append(row_dict)
    return transactions


def create_pages(transactions):
    pages = []
    for element in transactions:
        date = datetime.strptime(element['Dato'], "%d.%m.%Y").date()
        belop_inn = element['Inn på konto']
        belop_ut = element['Ut fra konto']
        element['belop'] = float(belop_inn) if belop_inn else -float(belop_ut)

        pages.append(create_transaction_page(
            dato=date, description=element['Forklaring'], amount=element['belop']))
    return pages


def send_to_notion(notion, pages):
    for page in pages:
        add_relation(notion, page, "Bank", "DnB")
        upload_concurrently(notion, page)
