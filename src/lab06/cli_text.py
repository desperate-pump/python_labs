"""ЛР6: команды stats и cat для текстовых файлов."""

import argparse
from pathlib import Path

from src.lib.text import count_freq, normalize, tokenize, top_n


def main(argv=None):
    parser = argparse.ArgumentParser(description="Работа с текстовыми файлами")
    commands = parser.add_subparsers(dest="command", required=True)

    cat = commands.add_parser("cat", help="Показать содержимое файла")
    cat.add_argument("--input", required=True, help="Путь к файлу")
    cat.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats = commands.add_parser("stats", help="Посчитать частоты слов")
    stats.add_argument("--input", required=True, help="Путь к TXT-файлу")
    stats.add_argument("--top", type=int, default=5, help="Сколько слов показать (по умолчанию 5)")

    args = parser.parse_args(argv)
    if args.command == "stats" and args.top < 1:
        parser.error("--top должен быть положительным числом")

    try:
        text = Path(args.input).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        parser.error(f"Не удалось прочитать файл: {error}")

    if args.command == "cat":
        for number, line in enumerate(text.splitlines(), 1):
            print(f"{number}: {line}" if args.n else line)
    else:
        words = tokenize(normalize(text))
        frequencies = count_freq(words)
        print(f"Всего слов: {len(words)}")
        print(f"Уникальных слов: {len(frequencies)}")
        print(f"Топ-{args.top}:")
        for word, count in top_n(frequencies, args.top):
            print(f"{word}: {count}")


if __name__ == "__main__":
    main()
