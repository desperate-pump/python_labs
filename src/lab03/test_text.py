"""Самопроверка задания A лабораторной работы 3."""

from src.lib.text import normalize, tokenize, count_freq, top_n


def main():
    # Нормализация
    assert normalize("ПрИвЕт\nМИр\t") == "привет мир"
    assert normalize("ёжик, Ёлка") == "ежик, елка"
    assert normalize("Hello\r\nWorld") == "hello world"
    assert normalize("  двойные   пробелы  ") == "двойные пробелы"
    assert normalize("ЁЖИК", yo2e=False) == "ёжик"
    assert normalize("Straße", casefold=True) == "strasse"
    assert normalize("Straße", casefold=False) == "straße"
    assert normalize("  \t\n  ") == ""

    # Выделение слов
    assert tokenize("привет мир") == ["привет", "мир"]
    assert tokenize("hello,world!!!") == ["hello", "world"]
    assert tokenize("по-настоящему круто") == ["по-настоящему", "круто"]
    assert tokenize("2025 год") == ["2025", "год"]
    assert tokenize("emoji 😀 не слово") == ["emoji", "не", "слово"]
    assert tokenize("кот—пёс") == ["кот", "пёс"]
    assert tokenize("one_two") == ["one_two"]

    # Подсчёт и сортировка частот
    assert count_freq(["a", "b", "a", "c", "b", "a"]) == {"a": 3, "b": 2, "c": 1}
    assert count_freq([]) == {}
    assert top_n({"a": 3, "b": 2, "c": 1}, 2) == [("a", 3), ("b", 2)]
    assert top_n({"bb": 2, "aa": 2, "cc": 1}, 2) == [("aa", 2), ("bb", 2)]
    assert top_n({}, 5) == []
    assert top_n({"a": 1}, 5) == [("a", 1)]

    print("Самопроверка задания A: 21 тест пройден (OK)")


if __name__ == "__main__":
    main()