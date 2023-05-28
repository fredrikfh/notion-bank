import csv
from datetime import datetime
from notion.add_relation import add_relation
from notion.create_notion_db_record import create_notion_db_record_background

from notion.create_notion_page import create_notion_page


def send_to_notion(notion, file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';', quotechar='"')
        for row in reader:
            data.append(row)

    keys = data[0]
    rows = data[1:]
    dict_list = []

    for row in rows:
        row_dict = {key: value for key, value in zip(keys, row)}
        dict_list.append(row_dict)

    for element in dict_list:
        dato = element['Dato']
        dato = datetime.strptime(dato, "%d.%m.%Y").date()
        inn = element['Inn på konto']
        ut = element['Ut fra konto']
        tekst = element['Forklaring']

        belop = 0
        if inn:
            belop = float(inn)
        elif ut:
            belop = - float(ut)

        page = create_notion_page(dato=dato, Beskrivelse=tekst, Beløp=belop)
        add_relation(notion, page, "Bank", "DnB")

        create_notion_db_record_background(notion, page)
