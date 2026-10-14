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