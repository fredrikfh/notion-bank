import csv
from datetime import datetime
from notion.add_relation import add_relation
from notion.create_notion_db_record import create_notion_db_record_background

from notion.create_notion_page import create_notion_page


def send_to_notion(notion, file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            data.append(row)

    # remove all whitespace from the data
    for row in data:
        for index, item in enumerate(row):
            row[index] = item.strip()

    keys = data[0]
    rows = data[1:]

    dict_list = []

    for row in rows:
        row_dict = {key: value for key, value in zip(keys, row)}
        dict_list.append(row_dict)

    for element in dict_list:
        # dato = datetime.strptime(element['Dato'], "%d/%m/%Y").date()
        dato = element['Dato']
        dato = datetime.strptime(dato, "%m/%d/%Y").date()
        belop = -float(element['Beløp'].replace(',', '.'))
        tekst = ' '.join(element['Beskrivelse'].split())
        ref = element['Referanse']

        # create a notion page
        page = create_notion_page(
            dato=dato, Beskrivelse=tekst, Beløp=belop, ref=ref)

        add_relation(notion, page, "Bank", "American Express")
        create_notion_db_record_background(notion, page)
