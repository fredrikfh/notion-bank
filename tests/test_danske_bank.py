import os

from dotenv import load_dotenv
from notion_client import Client

from banks.danske_bank import create_pages, get_transactions

load_dotenv()

if os.getenv('CI'):
    notion = None
else:
    notion = Client(auth=os.getenv('NOTION_API_KEY'))

notion = Client(auth=os.getenv('NOTION_API_KEY'))
transactions = get_transactions('tests/fixtures/danske.csv')
transactions_expected = [{'Dato': '11.04.2023', 'Kategori': 'Fritid og fornøyelser', 'Underkategori': 'Kafø/restaurant', 'Tekst': 'Reffen', 'Beløp': '-138,46', 'Saldo': '4.192,83', 'Status': 'Utført',
                          'Avstemt': 'Nei'}, {'Dato': '11.04.2023', 'Kategori': 'Bil og transport', 'Underkategori': 'Buss/tog', 'Tekst': 'Metro Barcelona', 'Beløp': '-43,00', 'Saldo': '4.149,83', 'Status': 'Utført', 'Avstemt': 'Nei'}]
pages = create_pages(transactions, notion)
pages_exprected = [{'Dato': {'date': {'start': '2023-04-11'}}, 'Beskrivelse': {'title': [{'text': {'content': 'Reffen'}}]}, 'Beløp': {'number': -138.46}}, {'Dato': {'date': {'start': '2023-04-11'}}, 'Beskrivelse': {'title': [
    {'text': {'content': 'Metro Barcelona'}}]}, 'Beløp': {'number': -43.0}, 'Kategori': {'relation': [{'id': 'cc852b4f-a0c3-4f3c-975b-4dd400577eee'}]}, 'Subkategori': {'relation': [{'id': 'a094fe8b-f6b3-494e-ad3e-6cbef3a42fee'}]}}]
pages_exprected_no_relations = [{'Dato': {'date': {'start': '2023-04-11'}}, 'Beskrivelse': {'title': [{'text': {'content': 'Reffen'}}]}, 'Beløp': {
    'number': -138.46}}, {'Dato': {'date': {'start': '2023-04-11'}}, 'Beskrivelse': {'title': [{'text': {'content': 'Metro Barcelona'}}]}, 'Beløp': {'number': -43.0}}]


def test_get_transactions():
    assert transactions == transactions_expected


def test_create_pages():
    assert pages in (pages_exprected, pages_exprected_no_relations)
