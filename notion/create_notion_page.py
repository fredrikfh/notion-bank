from datetime import date
from typing import Optional


def create_notion_page(dato: date, Beskrivelse: str, Beløp: float, Overføring: Optional[date] = None, rente: Optional[date] = None, ref: Optional[str] = None):

    # Beløp = float(Beløp.replace('.', '').replace(',', '.')) if (
    #     Beløp and isinstance(Beløp, str)) else 0

    new_page = {
        "Dato": {"date": {"start": dato.isoformat()}},
        "Beskrivelse": {"title": [{"text": {"content": Beskrivelse}}]},
        "Beløp": {"number": Beløp}
    }

    if Overføring:
        new_page["Overføring"] = {"date": {"start": Overføring.isoformat()}}

    if rente:
        new_page["Rentedato"] = {"date": {"start": rente.isoformat()}}

    if ref:
        new_page["Ref"] = {"rich_text": [{"text": {"content": ref}}]}

    return new_page
