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
