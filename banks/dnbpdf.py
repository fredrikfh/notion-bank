import io
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader, PdfWriter
import os
import pdfplumber
import tempfile
import tabula
import pandas as pd
from datetime import datetime
from notion.create_notion_db_record import create_notion_db_record
from notion.create_notion_page import create_notion_page

# since DNB forklarende text spans multiple lines, wee need to merge these together


def merge_rows(df):
    merged_rows = []
    current_row = None
    for index, row in df.iterrows():
        if not pd.isna(row['Dato']):
            if current_row is not None:
                merged_rows.append(current_row)
            current_row = row
        else:
            current_row['Forklarende tekst'] += ' ' + \
                str(row['Forklarende tekst'])
    merged_rows.append(current_row)
    return pd.DataFrame(merged_rows)


def preprocess_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        output = PdfWriter()
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            start_index = text.find("Bruk")
            if start_index != -1:
                # Crop the page to keep only the content after the word "Bruk"
                cropped_text = text[start_index:]
                cropped_page = PdfReader(
                    io.StringIO(cropped_text)).getPage(0)
                output.addPage(cropped_page)

        # Save the preprocessed PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            output.write(temp_file)
            temp_file.flush()

        return temp_file.name


def getData(pdf_path):
    preprocessed_pdf_path = preprocess_pdf(pdf_path)
    # Define the desired column names
    columns = ['Bruk', 'Bokføring', 'Forklarende tekst',
               'Ut av konto', 'Inn på konto', 'Rentedato', 'Arkivref.']

    # Read the PDF into a list of DataFrames
    tables = tabula.read_pdf(pdf_path, pages=1, multiple_tables=True)

    # Print all tables
    for table in tables:
        print(table)
        print("Continue")

    # Concatenate all tables into a single DataFrame
    df = pd.concat(tables, axis=0, ignore_index=True)

    # Skip the first row
    df = df.iloc[1:]
    merged_rows = merge_rows(df)
    print(merged_rows)

    # TODO delete this
    os.remove(preprocessed_pdf_path)
    return merged_rows


def send_to_notion(notion, filePath):
    for index, row in getData(filePath).iterrows():
        Bruk = datetime.strptime(row['Dato'], "%d.%m.%y").date()
        Overføring = datetime.strptime(row['Unnamed: 0'], "%d.%m.%y").date()
        Beskrivelse = row['Forklarende tekst']
        ut = row['Ut av konto']
        inn = row['Inn på konto']
        rente = datetime.strptime(row['Rentedato'], "%d.%m.%y").date()
        ref = row['Arkivref.']

        page = create_notion_page(Bruk=Bruk, Overføring=Overføring,
                                  Beskrivelse=Beskrivelse, ut=ut, inn=inn, rente=rente, ref=ref)

        # for debug purposes this is commented out
        # create_notion_db_record(notion, page)
