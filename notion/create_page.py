from datetime import date
from typing import Optional


def create_transaction_page(
        dato: date,
        description: str,
        amount: float,
        transfer_date: Optional[date] = None,
        interest_date: Optional[date] = None,
        reference: Optional[str] = None):
    """
    Creates a notion page with the following properties:
    - Dato
    - Beskrivelse
    - Beløp
    - Overføring
    - Rentedato
    - Ref
    """

    new_page = {
        "Dato": {"date": {"start": dato.isoformat()}},
        "Beskrivelse": {"title": [{"text": {"content": description}}]},
        "Beløp": {"number": amount}
    }

    if transfer_date:
        new_page["Overføring"] = {"date": {"start": transfer_date.isoformat()}}

    if interest_date:
        new_page["Rentedato"] = {"date": {"start": interest_date.isoformat()}}

    if reference:
        new_page["Ref"] = {"rich_text": [{"text": {"content": reference}}]}

    return new_page
