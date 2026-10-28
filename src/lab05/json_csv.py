"""Задание A: преобразование JSON и CSV."""

import csv
import json
from pathlib import Path


def _check_paths(input_path: str, output_path: str, input_ext: str, output_ext: str):
    """Проверить существование входного файла и расширения путей."""
    source = Path(input_path)
    target = Path(output_path)
    if not source.exists():
        raise FileNotFoundError(f"Файл не найден: {source}")
    if not source.is_file() or source.suffix.lower() != input_ext or target.suffix.lower() != output_ext:
        raise ValueError("Неверный тип входного или выходного файла")
    return source, target


def _read_csv(path: Path):
    """Прочитать CSV с заголовком и проверить количество полей."""
    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, strict=True)
            headers = reader.fieldnames
            if not headers or any(not name.strip() for name in headers):
                raise ValueError("CSV пуст или не содержит корректного заголовка")
            if len(headers) != len(set(headers)):
                raise ValueError("Повторяющиеся заголовки CSV")
            rows = list(reader)
    except csv.Error as error:
        raise ValueError("Некорректный CSV") from error
    if any(None in row or None in row.values() for row in rows):
        raise ValueError("Количество полей не совпадает с заголовком CSV")
    return headers, rows


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Сохранить список JSON-словарей в CSV."""
    source, target = _check_paths(json_path, csv_path, ".json", ".csv")
    with source.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list) or not data or not all(isinstance(row, dict) for row in data):
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    keys = set()
    for row in data:
        for key, value in row.items():
            if not key.strip() or not isinstance(value, (str, int, float, bool)):
                raise ValueError("Неверный ключ или значение JSON")
        keys.update(row)
    if not keys:
        raise ValueError("JSON не содержит полей")

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=sorted(keys), restval="", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Сохранить CSV как список словарей со строковыми значениями."""
    source, target = _check_paths(csv_path, json_path, ".csv", ".json")
    _, rows = _read_csv(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
        file.write("\n")
