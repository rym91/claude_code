#!/usr/bin/env python3
"""Fix Amazon price-template cells that Excel/Calc turned into dates.

In locales where "." is the date separator (uk-UA, ru-RU, de-DE ...), pasting a
price like 15.04 into a General-formatted cell makes the spreadsheet parse it as
"15 April of the current year". Prices such as 19.99 survive (there is no month
99), which is why only part of the column looks broken.

Two commands:

  check / fix   scan a filled-in template, report (and optionally repair) the
                price cells that became dates
  paste         write a column of prices copied from Google Sheets into the
                template as real numbers, bypassing locale parsing entirely

Usage:
  python3 fix_price_dates.py check PriceAndQuantityBC.xlsm
  python3 fix_price_dates.py fix   PriceAndQuantityBC.xlsm -o fixed.xlsm
  python3 fix_price_dates.py paste PriceAndQuantityBC.xlsm prices.txt --column G
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

try:
    import openpyxl
    from openpyxl.utils import column_index_from_string, get_column_letter
except ImportError:  # pragma: no cover - dependency hint
    sys.exit("openpyxl is required:  pip install openpyxl")

PRICE_FORMAT = "0.00"
HEADER_SCAN_ROWS = 12


def open_book(path: Path):
    keep_vba = path.suffix.lower() in {".xlsm", ".xltm"}
    return openpyxl.load_workbook(path, keep_vba=keep_vba)


def pick_sheet(book, name: str | None):
    if name:
        if name not in book.sheetnames:
            sys.exit(f"sheet {name!r} not found; available: {', '.join(book.sheetnames)}")
        return book[name]
    for candidate in ("Template", "Шаблон"):
        if candidate in book.sheetnames:
            return book[candidate]
    return book.worksheets[0]


def find_header_row(sheet) -> int:
    """Row that holds the column captions (the one containing 'SKU')."""
    for row in range(1, min(HEADER_SCAN_ROWS, sheet.max_row) + 1):
        for cell in sheet[row]:
            if isinstance(cell.value, str) and cell.value.strip().lower() == "sku":
                return row
    return 1


def find_price_columns(sheet, header_row: int) -> list[int]:
    columns = []
    for cell in sheet[header_row]:
        if isinstance(cell.value, str) and "price" in cell.value.lower():
            columns.append(cell.column)
    return columns


def first_data_row(sheet, header_row: int) -> int:
    for row in range(header_row + 1, sheet.max_row + 1):
        if sheet.cell(row=row, column=1).value not in (None, ""):
            return row
    return header_row + 1


def date_to_price(value: dt.date, decimals: int = 2) -> float:
    """Reverse the day.month parse: 15 April -> 15.04 (assumes 2 decimals)."""
    return float(f"{value.day}.{value.month:0{decimals}d}")


def scan(sheet, columns: list[int], start_row: int) -> list[tuple[int, int, dt.date, float]]:
    hits = []
    for column in columns:
        for row in range(start_row, sheet.max_row + 1):
            value = sheet.cell(row=row, column=column).value
            if isinstance(value, dt.datetime):
                value = value.date()
            if isinstance(value, dt.date):
                hits.append((row, column, value, date_to_price(value)))
    return hits


def parse_price(raw: str) -> float | None:
    text = raw.strip().replace(" ", "").replace(" ", "")
    for junk in ("$", "USD", "usd"):
        text = text.replace(junk, "")
    if not text:
        return None
    if "," in text and "." not in text:
        text = text.replace(",", ".")
    else:
        text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return None


def cmd_check(args) -> int:
    book = open_book(args.file)
    sheet = pick_sheet(book, args.sheet)
    header_row = find_header_row(sheet)
    columns = (
        [column_index_from_string(c.strip().upper()) for c in args.columns.split(",")]
        if args.columns
        else find_price_columns(sheet, header_row)
    )
    if not columns:
        sys.exit("no price columns found; pass --columns G,J")

    start_row = first_data_row(sheet, header_row)
    hits = scan(sheet, columns, start_row)
    names = ", ".join(get_column_letter(c) for c in columns)
    print(f"sheet {sheet.title!r}, header row {header_row}, price columns: {names}")
    print(f"{len(hits)} cell(s) stored as a date instead of a price")
    for row, column, value, price in hits:
        cell = f"{get_column_letter(column)}{row}"
        print(f"  {cell}: {value.isoformat()} -> {price:.2f}")

    if hits and args.command == "fix":
        for row, column, _value, price in hits:
            cell = sheet.cell(row=row, column=column)
            cell.value = price
            cell.number_format = PRICE_FORMAT
        out = args.output or args.file
        book.save(out)
        print(f"saved {out}")
        print(
            "note: 15.4 and 15.04 collapse to the same date, so a one-decimal "
            "price is restored as .0X -- re-check those against the source sheet"
        )
    return 0


def cmd_paste(args) -> int:
    book = open_book(args.file)
    sheet = pick_sheet(book, args.sheet)
    header_row = find_header_row(sheet)
    column = column_index_from_string(args.column.strip().upper())
    start_row = args.start_row or first_data_row(sheet, header_row)

    raw_lines = args.values.read_text(encoding="utf-8-sig").splitlines()
    written = blank = bad = 0
    for offset, raw in enumerate(raw_lines):
        if not raw.strip():
            blank += 1
            continue
        price = parse_price(raw)
        if price is None:
            print(f"  line {offset + 1}: {raw!r} is not a number, row left unchanged")
            bad += 1
            continue
        cell = sheet.cell(row=start_row + offset, column=column)
        cell.value = price
        cell.number_format = PRICE_FORMAT
        written += 1

    out = args.output or args.file
    book.save(out)
    end_row = start_row + len(raw_lines) - 1
    print(
        f"wrote {written} price(s) into {get_column_letter(column)}"
        f"{start_row}:{get_column_letter(column)}{end_row} of {sheet.title!r}"
    )
    if blank or bad:
        print(f"{blank} blank and {bad} unparsable line(s) left unchanged")
    print(f"saved {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    for name, help_text in (("check", "report price cells stored as dates"), ("fix", "repair them in place")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("file", type=Path)
        p.add_argument("-o", "--output", type=Path, help="write to this file instead of overwriting")
        p.add_argument("--sheet", help="sheet name (default: Template)")
        p.add_argument("--columns", help="price columns, e.g. G,J (default: auto-detect by header)")
        p.set_defaults(func=cmd_check)

    p = sub.add_parser("paste", help="write a copied column of prices as real numbers")
    p.add_argument("file", type=Path)
    p.add_argument("values", type=Path, help="text file with one price per line")
    p.add_argument("--column", required=True, help="target column letter, e.g. G")
    p.add_argument("--start-row", type=int, help="first data row (default: auto-detect)")
    p.add_argument("-o", "--output", type=Path, help="write to this file instead of overwriting")
    p.add_argument("--sheet", help="sheet name (default: Template)")
    p.set_defaults(func=cmd_paste)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
