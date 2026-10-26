"""Конвертация CSV → XLSX с автошириной колонок."""

from openpyxl import Workbook
from openpyxl.utils.exceptions import IllegalCharacterError

from src.lab05.json_csv import _check_paths, _read_csv


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """Перенести CSV в текстовые ячейки листа Sheet1 и сохранить XLSX."""
    source, target = _check_paths(csv_path, xlsx_path, ".csv", ".xlsx")
    headers, rows = _read_csv(str(source))
    if len(headers) > 16384 or len(rows) + 1 > 1048576:
        raise ValueError("Таблица превышает ограничения листа Excel")
    table = [headers] + [list(row.values()) for row in rows]
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    try:
        for row in table:
            if any(len(value) > 32767 for value in row):
                raise ValueError("Ячейка Excel не может содержать более 32767 символов")
            ws.append(row)
            for cell in ws[ws.max_row]:
                # Сохраняем текст, включая ведущие нули, =формулы и #N/A.
                cell.data_type = "s"
    except IllegalCharacterError as error:
        raise ValueError("CSV содержит недопустимый для XLSX управляющий символ") from error
    for column in ws.columns:
        length = max(len(cell.value or "") for cell in column)
        ws.column_dimensions[column[0].column_letter].width = min(255, max(8, length + 2))
    target.parent.mkdir(parents=True, exist_ok=True)
    wb.save(target)
