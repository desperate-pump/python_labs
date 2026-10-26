"""Конвертации JSON ↔ CSV без вывода в терминал."""

import csv
import json
from pathlib import Path


def _check_paths(
    input_path: str, output_path: str, input_suffix: str, output_suffix: str,
) -> tuple[Path, Path]:
    """Проверить входной файл и расширения обоих путей."""
    source, target = Path(input_path), Path(output_path)
    if not source.exists():
        raise FileNotFoundError(f"Файл не найден: {source}")
    if not source.is_file():
        raise ValueError("Входной путь должен указывать на файл")
    if source.suffix.lower() != input_suffix or target.suffix.lower() != output_suffix:
        raise ValueError(f"Ожидаются расширения {input_suffix} → {output_suffix}")
    return source, target


def _unique_object(pairs: list[tuple]) -> dict:
    """Не допустить потери значения при повторяющемся ключе JSON."""
    result = dict(pairs)
    if len(result) != len(pairs):
        raise ValueError("Ключи JSON-объекта не должны повторяться")
    return result


def _read_csv(csv_path: str) -> tuple[list[str], list[dict[str, str]]]:
    """Прочитать CSV с уникальным заголовком и одинаковой длиной строк."""
    try:
        with Path(csv_path).open(encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, delimiter=",", strict=True)
            headers = reader.fieldnames
            if not headers or any(not key.strip() for key in headers):
                raise ValueError("CSV пуст или содержит пустые заголовки")
            if len(set(headers)) != len(headers):
                raise ValueError("Заголовки CSV не должны повторяться")
            rows = []
            for row in reader:
                if None in row or None in row.values():
                    raise ValueError(f"Строка CSV {reader.line_num}: число полей не совпадает с заголовком")
                rows.append(row)
    except csv.Error as error:
        raise ValueError(f"Некорректный CSV: {error}") from error
    return headers, rows


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Записать список словарей в CSV; столбцы отсортированы по алфавиту."""
    source, target = _check_paths(json_path, csv_path, ".json", ".csv")
    with source.open(encoding="utf-8") as file:
        data = json.load(file, object_pairs_hook=_unique_object)
    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    keys = set()
    for row in data:
        if not isinstance(row, dict):
            raise ValueError("Каждый элемент списка JSON должен быть словарём")
        for key, value in row.items():
            if not key.strip():
                raise ValueError("Ключи JSON не должны быть пустыми")
            if not isinstance(value, (str, int, float, bool)):
                raise ValueError("Допустимы строки, числа и bool; null и вложенные структуры не поддерживаются")
            # allow_nan=False запрещает NaN и бесконечности, не входящие в JSON.
            if isinstance(value, float):
                json.dumps(value, allow_nan=False)
        keys.update(row)
    if not keys:
        raise ValueError("JSON должен содержать хотя бы один столбец")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=sorted(keys), restval="", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Записать строки CSV в JSON; все значения остаются строками."""
    source, target = _check_paths(csv_path, json_path, ".csv", ".json")
    headers, rows = _read_csv(str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as file:
        json.dump(rows, file, ensure_ascii=False, indent=2)
        file.write("\n")
