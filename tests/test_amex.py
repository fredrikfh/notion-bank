import os

from dotenv import load_dotenv
from notion_client import Client

from banks.amex import create_pages, get_transactions

load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))
transactions = get_transactions('tests/fixtures/amex.csv')
transactions_expected = [{'Dato': '05/19/2023', 'Beskrivelse': 'MEDLEMSAVGIFT', 'Beløp': '100,00', 'Utvidede detaljer': '', 'Opptrer på din kontoutskrift som': 'MEDLEMSAVGIFT', 'Adresse': '', 'Sted': '', 'Postnummer': '', 'Land': '', 'Referanse': "'AT847282'", 'Kategori': ''}, {'Dato': '05/16/2023', 'Beskrivelse': 'CHATGPT SUBSCRIPTION    SAN FRANCISCO', 'Beløp': '219,56', 'Utvidede detaljer': 'Foreign Spend Amount: 20.00 UNITED STATES DOLLAR Commission Amount: 5,36 Currency Exchange Rate: 0.0933', 'Opptrer på din kontoutskrift som': 'CHATGPT SUBSCRIPTION    SAN FRANCISCO', 'Adresse': '185 BERRY STREET\nSUITE 550\nSAN FRANCISCO\nCA', 'Sted': '', 'Postnummer': '94107', 'Land': 'UNITED STATES OF AMERICA (THE)', 'Referanse': "'AT83831718'", 'Kategori': ''}, {'Dato': '05/16/2023', 'Beskrivelse': 'Supermercado Expres', 'Beløp': '101,50', 'Utvidede detaljer': '', 'Opptrer på din kontoutskrift som': '', 'Adresse': '', 'Sted': '', 'Postnummer': '', 'Land': '', 'Referanse': "'AT94933'", 'Kategori': 'Miscellaneous-Other'}, {
    'Dato': '05/12/2023', 'Beskrivelse': 'PAPERFORM               PALO ALTO', 'Beløp': '262,51', 'Utvidede detaljer': 'Foreign Spend Amount: 24.00 UNITED STATES DOLLAR Commission Amount: 6,40 Currency Exchange Rate: 0.0937', 'Opptrer på din kontoutskrift som': 'PAPERFORM               PALO ALTO', 'Adresse': '185 BERRY STREET\nSUITE 550\nSAN FRANCISCO\nCA', 'Sted': '', 'Postnummer': '94107', 'Land': 'UNITED STATES OF AMERICA (THE)', 'Referanse': "'AT8381919'", 'Kategori': ''}, {'Dato': '05/12/2023', 'Beskrivelse': 'WWW.WOLFRAMALPHA.COM    CHAMPAIGN', 'Beløp': '79,30', 'Utvidede detaljer': 'Foreign Spend Amount: 7.25 UNITED STATES DOLLAR Commission Amount: 1,93 Currency Exchange Rate: 0.0937', 'Opptrer på din kontoutskrift som': 'WWW.WOLFRAMALPHA.COM    CHAMPAIGN', 'Adresse': '185 BERRY STREET\nSUITE 550\nSAN FRANCISCO\nCA', 'Sted': '', 'Postnummer': '94107', 'Land': 'UNITED STATES OF AMERICA (THE)', 'Referanse': "'AT9348382'", 'Kategori': ''}]
pages = create_pages(transactions)
pages_exprected = [{'Dato': {'date': {'start': '2023-05-19'}}, 'Beskrivelse': {'title': [{'text': {'content': 'MEDLEMSAVGIFT'}}]}, 'Beløp': {'number': -100.0}, 'Ref': {'rich_text': [{'text': {'content': "'AT847282'"}}]}}, {'Dato': {'date': {'start': '2023-05-16'}}, 'Beskrivelse': {'title': [{'text': {'content': 'CHATGPT SUBSCRIPTION SAN FRANCISCO'}}]}, 'Beløp': {'number': -219.56}, 'Ref': {'rich_text': [{'text': {'content': "'AT83831718'"}}]}}, {'Dato': {'date': {'start': '2023-05-16'}}, 'Beskrivelse': {'title': [{'text': {'content': 'Supermercado Expres'}}]},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'Beløp': {'number': -101.5}, 'Ref': {'rich_text': [{'text': {'content': "'AT94933'"}}]}}, {'Dato': {'date': {'start': '2023-05-12'}}, 'Beskrivelse': {'title': [{'text': {'content': 'PAPERFORM PALO ALTO'}}]}, 'Beløp': {'number': -262.51}, 'Ref': {'rich_text': [{'text': {'content': "'AT8381919'"}}]}}, {'Dato': {'date': {'start': '2023-05-12'}}, 'Beskrivelse': {'title': [{'text': {'content': 'WWW.WOLFRAMALPHA.COM CHAMPAIGN'}}]}, 'Beløp': {'number': -79.3}, 'Ref': {'rich_text': [{'text': {'content': "'AT9348382'"}}]}}]


def test_get_transactions():
    assert transactions == transactions_expected


def test_create_pages():
    assert pages == pages_exprected
