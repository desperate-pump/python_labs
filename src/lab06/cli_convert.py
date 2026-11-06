"""ЛР6: консольные команды для конвертации файлов."""

import argparse

from src.lab05.csv_xlsx import csv_to_xlsx
from src.lab05.json_csv import csv_to_json, json_to_csv


def main(argv=None):
    parser = argparse.ArgumentParser(description="Конвертация JSON, CSV и XLSX")
    commands = parser.add_subparsers(dest="command", required=True)

    for name in ("json2csv", "csv2json", "csv2xlsx"):
        command = commands.add_parser(name, help=f"Конвертация {name}")
        command.add_argument("--in", dest="input", required=True, help="Входной файл")
        command.add_argument("--out", dest="output", required=True, help="Выходной файл")

    args = parser.parse_args(argv)

    try:
        if args.command == "json2csv":
            json_to_csv(args.input, args.output)
        elif args.command == "csv2json":
            csv_to_json(args.input, args.output)
        else:
            csv_to_xlsx(args.input, args.output)
    except (OSError, ValueError, UnicodeError) as error:
        parser.error(str(error))

    print(f"Готово: {args.output}")


if __name__ == "__main__":
    main()
