# Лабораторная работа 3. Тексты и частоты слов

**Цель:** научиться нормализовать текст, выделять слова, считать их частоты и выводить самые частые слова. Используется только стандартная библиотека Python (Python 3.10+).

### Задание A. Обработка текста и подсчёт частот

* **Скрипт:** `src/lib/text.py`.
* **Суть задания:** реализовать четыре функции: `normalize` приводит текст к единому виду, `tokenize` выделяет слова с сохранением дефисов, `count_freq` подсчитывает повторения, `top_n` выбирает самые частые слова. При одинаковых частотах используется алфавитный порядок.

**Текст программы `src/lib/text.py`:**

```python
import re


def normalize(text: str, *, casefold: bool = True,
              yo2e: bool = True) -> str:
    """Привести текст к единому виду."""
    if casefold:
        text = text.casefold()
    else:
        text = text.lower()

    if yo2e:
        text = text.replace("ё", "е")
        text = text.replace("Ё", "Е")

    text = " ".join(text.split())
    return text


def tokenize(text: str) -> list[str]:
    """Разбить текст на слова с сохранением дефисов внутри слов."""
    return re.findall(r"\w+(?:-\w+)*", text)


def count_freq(tokens: list[str]) -> dict[str, int]:
    """Подсчитать количество вхождений каждого слова."""
    freq = {}
    for word in tokens:
        freq[word] = freq.get(word, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    """Получить n самых частых слов с алфавитным разрешением равенств."""
    pairs = sorted(freq.items(), key=lambda item: (-item[1], item[0]))
    return pairs[:n]
```

**Пример работы функций:**

```python
from src.lib.text import normalize, tokenize, count_freq, top_n

text = normalize("Привет, мир! Привет!!!")
words = tokenize(text)
freq = count_freq(words)

print(words)          # ['привет', 'мир', 'привет']
print(freq)           # {'привет': 2, 'мир': 1}
print(top_n(freq, 2)) # [('привет', 2), ('мир', 1)]
```

**Самопроверка:** в `src/lab03/test_text.py` собраны 21 проверка, включая случаи с `ё`, разным регистром, лишними пробелами, дефисами, числами, эмодзи, пустым вводом и равными частотами.

Запуск из корня репозитория:

```bash
python3 -m src.lab03.test_text
```

Ожидаемый результат:

```text
Самопроверка задания A: 21 тест пройден (OK)
```

#### Результат работы задания A

![Самопроверка задания A](../../images/lab03/img01.png)

---

### Задание B. Статистика слов из стандартного ввода

* **Скрипт:** `src/lab03/text_stats.py`.
* **Суть задания:** прочитать одну строку с клавиатуры (`stdin`), обработать её функциями из задания A, вывести общее количество слов, количество уникальных слов и топ-5 по частоте.

**Текст программы `src/lab03/text_stats.py`:**

```python
from src.lib.text import normalize, tokenize, count_freq, top_n


def main():
    """Прочитать строку и вывести статистику слов."""
    text = input()

    clean_text = normalize(text)
    words = tokenize(clean_text)
    freq = count_freq(words)
    top = top_n(freq, 5)

    print("Всего слов:", len(words))
    print("Уникальных слов:", len(freq))
    print("Топ-5:")

    for word, count in top:
        print(f"{word}:{count}")


if __name__ == "__main__":
    main()
```

**Запуск в терминале MacBook из корня репозитория:**

```bash
python3 -m src.lab03.text_stats
```

После запуска ввести строку и нажать Enter.

**Пример ввода:**

```text
Привет, мир! Привет!!!
```

**Результат вывода:**

```text
Всего слов: 3
Уникальных слов: 2
Топ-5:
привет:2
мир:1
```

Пример запуска с передачей строки через терминал:

```bash
echo "Привет, мир! Привет!!!" | python3 -m src.lab03.text_stats
```

#### Результат работы задания B

![Запуск программы и вывод статистики](../../images/lab03/img02.png)

---

### Проверка и структура работы

* `src/lib/text.py` — четыре функции для обработки текста (без ввода и вывода).
* `src/lab03/text_stats.py` — основная программа.
* `src/lab03/test_text.py` — 21 проверка функций.
* `images/lab03/img01.png` — скриншот проверки задания A.
* `images/lab03/img02.png` — скриншот запуска задания B.

Запускать программы нужно **из корневой папки `python_labs`**. Для работы не требуются сторонние библиотеки.