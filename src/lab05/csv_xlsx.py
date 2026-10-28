"""Задание B: преобразование CSV в XLSX."""

from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from src.lab05.json_csv import _check_paths, _read_csv


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Создать лист Sheet1 и установить ширину колонок."""
    source, target = _check_paths(csv_path, xlsx_path, ".csv", ".xlsx")
    headers, rows = _read_csv(source)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"

    try:
        for values in [headers] + [[row[name] for name in headers] for row in rows]:
            if any(len(value) > 32767 for value in values):
                raise ValueError("Слишком длинное значение для ячейки Excel")
            sheet.append(values)
            for cell in sheet[sheet.max_row]:
                cell.data_type = "s"  # Сохраняем CSV-значения как текст.
    except IllegalCharacterError as error:
        raise ValueError("Недопустимый символ в CSV") from error

    for column in sheet.columns:
        length = max(len(cell.value or "") for cell in column)
        letter = column[0].column_letter
        sheet.column_dimensions[letter].width = min(255, max(8, length + 2))

    target.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(target)
