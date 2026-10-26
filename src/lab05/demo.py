"""Три сценария для демонстрации ЛР5 из корня репозитория."""

import argparse
import csv
import json
import sys
from pathlib import Path

from openpyxl import load_workbook

from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import csv_to_json, json_to_csv


def main() -> int:
    """Запустить выбранную конвертацию и показать фактический результат."""
    parser = argparse.ArgumentParser(description="Демонстрация лабораторной работы 5")
    parser.add_argument("scenario", choices=("json-to-csv", "csv-to-json", "csv-to-xlsx"))
    args = parser.parse_args()
    try:
        if args.scenario == "json-to-csv":
            source = Path("data/samples/people.json")
            target = Path("data/out/people_from_json.csv")
            json_to_csv(str(source), str(target))
            data = json.loads(source.read_text(encoding="utf-8"))
            with target.open(encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                rows = list(reader)
            if len(rows) != len(data) or headers != sorted({key for row in data for key in row}):
                raise ValueError("Проверка заголовка или числа записей не пройдена")
            print("JSON → CSV")
            print("Вход:", source)
            print("Выход:", target)
            print("Столбцы:", ", ".join(headers))
            print(f"Записей: {len(data)} → {len(rows)}")
            print(target.read_text(encoding="utf-8"), end="")
        elif args.scenario == "csv-to-json":
            source = Path("data/samples/people.csv")
            target = Path("data/out/people_from_csv.json")
            csv_to_json(str(source), str(target))
            with source.open(encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames
                rows = list(reader)
            data = json.loads(target.read_text(encoding="utf-8"))
            if data != rows or any(list(row) != headers for row in data):
                raise ValueError("Проверка ключей или значений JSON не пройдена")
            print("CSV → JSON")
            print("Вход:", source)
            print("Выход:", target)
            print("Ключи:", ", ".join(headers))
            print(f"Записей: {len(rows)} → {len(data)}; значения — строки")
            print(target.read_text(encoding="utf-8"), end="")
        else:
            source = Path("data/samples/people.csv")
            target = Path("data/out/people.xlsx")
            csv_to_xlsx(str(source), str(target))
            with source.open(encoding="utf-8", newline="") as file:
                expected = list(csv.reader(file))
            wb = load_workbook(target)
            try:
                ws = wb["Sheet1"]
                actual = [[value if value is not None else "" for value in row]
                          for row in ws.iter_rows(values_only=True)]
                if wb.sheetnames != ["Sheet1"] or actual != expected:
                    raise ValueError("Проверка содержимого XLSX не пройдена")
                print("CSV → XLSX")
                print("Вход:", source)
                print("Выход:", target)
                print("Листы:", wb.sheetnames)
                print(f"Строк: {ws.max_row} (с заголовком); столбцов: {ws.max_column}")
                for column in ws.columns:
                    letter = column[0].column_letter
                    print(f"Ширина {letter}: {ws.column_dimensions[letter].width:g}")
                for row in ws.iter_rows(values_only=True):
                    print(" | ".join("" if value is None else value for value in row))
            finally:
                wb.close()
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    print("Проверка результата: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
