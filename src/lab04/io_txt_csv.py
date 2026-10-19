"""Чтение TXT и запись CSV для лабораторной работы 4."""

import csv
from pathlib import Path


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Прочитать текст целиком. Для Windows-1251: encoding="cp1251".

    Если файла нет, возникнет FileNotFoundError; если кодировка
    не подходит, возможен UnicodeDecodeError.
    """
    return Path(path).read_text(encoding=encoding)


def ensure_parent_dir(path: str | Path) -> None:
    """Создать родительские папки, если они ещё не существуют."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(
    rows: list[tuple | list],
    path: str | Path,
    header: tuple[str, ...] | None = None,
) -> None:
    """Записать CSV (UTF-8, разделитель запятая); строки одинаковой длины.

    Если задан header, он записывается первой строкой. При разной
    длине строк (в том числе относительно заголовка) — ValueError.
    """
    expected = len(header) if header is not None else (len(rows[0]) if rows else None)
    for number, row in enumerate(rows, 1):
        if len(row) != expected:
            raise ValueError(f"Строка {number}: ожидалось {expected} столбцов, получено {len(row)}")

    ensure_parent_dir(path)
    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        if header is not None:
            writer.writerow(header)
        writer.writerows(rows)
