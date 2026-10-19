"""Чтение TXT, подсчёт частот слов и сохранение отчёта CSV."""

import argparse
import sys
from pathlib import Path

# Поддерживаем запуск из корня репозитория как файлом, так и через -m.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.lab04.io_txt_csv import read_text, write_csv
from src.lib.text import normalize, tokenize, count_freq, top_n


def create_report(
    input_path: str | Path,
    output_path: str | Path,
    encoding: str = "utf-8",
) -> tuple[int, int, list[tuple[str, int]]]:
    """Создать CSV и вернуть (всего слов, уникальных слов, топ-5)."""
    text = read_text(input_path, encoding=encoding)
    words = tokenize(normalize(text))
    freq = count_freq(words)
    rows = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    write_csv(rows, output_path, header=("word", "count"))
    return len(words), len(freq), top_n(freq, 5)


def main(argv: list[str] | None = None) -> int:
    """Разобрать аргументы, создать отчёт и вывести краткую статистику."""
    parser = argparse.ArgumentParser(description="Отчёт по частотам слов из TXT в CSV")
    parser.add_argument("--in", dest="input_path", default="data/input.txt",
                        help="путь к входному TXT (по умолчанию data/input.txt)")
    parser.add_argument("--out", dest="output_path", default="data/report.csv",
                        help="путь к выходному CSV (по умолчанию data/report.csv)")
    parser.add_argument("--encoding", default="utf-8",
                        help="кодировка входного файла, например cp1251")
    args = parser.parse_args(argv)

    try:
        total, unique, popular = create_report(args.input_path, args.output_path,
                                                encoding=args.encoding)
    except (OSError, UnicodeError, LookupError) as error:
        print(f"Ошибка чтения или записи файла: {error}", file=sys.stderr)
        return 1

    print("Всего слов:", total)
    print("Уникальных слов:", unique)
    print("Топ-5:")
    for word, count in popular:
        print(f"{word}:{count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
