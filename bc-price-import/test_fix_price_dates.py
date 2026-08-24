#!/usr/bin/env python3
"""Self-contained checks for fix_price_dates.py:  python3 test_fix_price_dates.py"""

import datetime as dt
import tempfile
from pathlib import Path

import openpyxl

import fix_price_dates as m

HEADERS = [
    "SKU",
    "Fulfillment Channel Code (US)",
    "Quantity (US)",
    "Handling Time",
    "Restock Date",
    "Inventory Always Available (US)",
    "Your Price USD (Sell on Amazon, US)",
    "Pricing Rule",
    "Minimum Seller Allowed Price USD",
]

# What the seller meant vs. what the spreadsheet stored after a locale-mangled paste.
ROWS = [
    ("SMVF1371", 25.99, 25.99),
    ("SMVF1867", dt.datetime(2026, 4, 15), 15.04),
    ("SMVF1471", 20.14, 20.14),
    ("SMVF1941", dt.datetime(2026, 1, 25), 25.01),
    ("SMVF1413", dt.datetime(2026, 11, 22), 22.11),
    ("SMVF1403", 22.95, 22.95),
]


def make_template(path: Path) -> None:
    book = openpyxl.Workbook()
    sheet = book.active
    sheet.title = "Template"
    sheet["A2"] = "Use ENGLISH to fill this template."
    for index, header in enumerate(HEADERS, start=1):
        sheet.cell(row=4, column=index, value=header)
    for offset, (sku, stored, _expected) in enumerate(ROWS):
        row = 6 + offset
        sheet.cell(row=row, column=1, value=sku)
        sheet.cell(row=row, column=7, value=stored)
    book.save(path)


def prices(path: Path) -> list:
    sheet = openpyxl.load_workbook(path)["Template"]
    return [sheet.cell(row=6 + i, column=7).value for i in range(len(ROWS))]


def test_parse_price():
    assert m.parse_price("25.99") == 25.99
    assert m.parse_price(" $20.14 ") == 20.14
    assert m.parse_price("25,01") == 25.01
    assert m.parse_price("1,234.50") == 1234.50
    assert m.parse_price("") is None
    assert m.parse_price("n/a") is None


def test_date_to_price():
    assert m.date_to_price(dt.date(2026, 4, 15)) == 15.04
    assert m.date_to_price(dt.date(2026, 11, 22)) == 22.11
    assert m.date_to_price(dt.date(2026, 1, 25)) == 25.01


def test_detects_and_repairs_dates(tmp: Path):
    broken, fixed = tmp / "broken.xlsx", tmp / "fixed.xlsx"
    make_template(broken)

    book = m.open_book(broken)
    sheet = m.pick_sheet(book, None)
    header_row = m.find_header_row(sheet)
    assert header_row == 4
    assert m.find_price_columns(sheet, header_row) == [7, 9]
    assert m.first_data_row(sheet, header_row) == 6
    assert len(m.scan(sheet, [7], 6)) == 3

    assert m.main(["fix", str(broken), "-o", str(fixed)]) == 0
    assert prices(fixed) == [expected for _sku, _stored, expected in ROWS]


def test_paste_writes_numbers(tmp: Path):
    target, pasted = tmp / "target.xlsx", tmp / "pasted.xlsx"
    make_template(target)
    values = tmp / "prices.txt"
    values.write_text("25.99\n15.04\n$20.14\n25,01\n22.11\n22.95\n")

    assert m.main(["paste", str(target), str(values), "--column", "G", "-o", str(pasted)]) == 0
    assert prices(pasted) == [expected for _sku, _stored, expected in ROWS]
    sheet = openpyxl.load_workbook(pasted)["Template"]
    assert sheet.cell(row=7, column=7).number_format == "0.00"


def test_paste_keeps_row_alignment_on_blanks(tmp: Path):
    target, pasted = tmp / "align.xlsx", tmp / "align-out.xlsx"
    make_template(target)
    values = tmp / "with-blank.txt"
    values.write_text("25.99\n\n20.14\n")

    assert m.main(["paste", str(target), str(values), "--column", "G", "-o", str(pasted)]) == 0
    sheet = openpyxl.load_workbook(pasted)["Template"]
    assert sheet.cell(row=6, column=7).value == 25.99
    assert sheet.cell(row=8, column=7).value == 20.14  # third line lands on the third row


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as directory:
        tmp = Path(directory)
        test_parse_price()
        test_date_to_price()
        test_detects_and_repairs_dates(tmp)
        test_paste_writes_numbers(tmp)
        test_paste_keeps_row_alignment_on_blanks(tmp)
    print("all checks passed")
