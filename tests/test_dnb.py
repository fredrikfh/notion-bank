from banks.dnb import get_transactions, create_pages

transactions = get_transactions('tests/fixtures/dnb.txt')
transactions_expected = [{'Dato': '19.05.2023', 'Forklaring': 'Supermercado Expres ', 'Rentedato': '19.05.2023', 'Ut fra konto': '2500', 'Inn på konto': '', 'belop': -2500.0}, {'Dato': '17.05.2023', 'Forklaring': 'Sopping A ',
                                                                                                                                                                                 'Rentedato': '19.05.2023', 'Ut fra konto': '', 'Inn på konto': '6000', 'belop': 6000.0}, {'Dato': '15.05.2023', 'Forklaring': 'Payment B', 'Rentedato': '15.05.2023', 'Ut fra konto': '126', 'Inn på konto': '', 'belop': -126.0}]
pages = create_pages(transactions)
pages_exprected = [{'Dato': {'date': {'start': '2023-05-19'}}, 'Beskrivelse': {'title': [{'text': {'content': 'Supermercado Expres '}}]}, 'Beløp': {'number': -2500.0}}, {'Dato': {'date': {'start': '2023-05-17'}}, 'Beskrivelse': {
    'title': [{'text': {'content': 'Sopping A '}}]}, 'Beløp': {'number': 6000.0}}, {'Dato': {'date': {'start': '2023-05-15'}}, 'Beskrivelse': {'title': [{'text': {'content': 'Payment B'}}]}, 'Beløp': {'number': -126.0}}]


def test_get_transactions():
    assert transactions == transactions_expected


def test_create_pages():
    assert pages == pages_exprected
