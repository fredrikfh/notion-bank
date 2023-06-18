# notion-bank

## Description

Send bank statements (transactions) to a Notion database.

Get started with the corresponding [Notion template](https://www.notion.so/).

## Supported banks

- DNB (txt)
- AMEX (csv)
- Danske Bank (csv)

## How to use it

Download statements from your bank and save them in the `bank_statements` folder.

Then

run `python3 main.py file_path bank_name

example: `python3 main.py bank_statements/2021-01-01.csv AMEX`

## Installation

You need a .env file in the root with the following variables:

```
NOTION_API_KEY=
NOTION_DATABASE_ID=
NOTION_OPERATOR_DATABASE_ID=
```
