"""ЛР2. Задание C: форматирование записи студента."""


def format_record(rec: tuple[str, str, float]) -> str:
    """Вернуть строку вида 'Иванов И.И., гр. BIVT-25, GPA 4.60'.

    ValueError — неверное содержимое записи; TypeError — неверный тип.
    """
    if not isinstance(rec, tuple):
        raise TypeError("Запись должна быть кортежем")
    if len(rec) != 3:
        raise ValueError("Нужны ФИО, группа и GPA")

    fio, group, gpa = rec
    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("ФИО и группа должны быть строками")
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом")
    if not 0 <= gpa <= 5:
        raise ValueError("GPA должен быть от 0 до 5")

    names = fio.split()  # Убираем лишние пробелы.
    group = " ".join(group.split())
    if len(names) not in (2, 3) or not group:
        raise ValueError("Некорректное ФИО или пустая группа")

    surname = names[0].capitalize()
    initials = ""
    for name in names[1:]:
        initials += name[0].upper() + "."

    return f"{surname} {initials}, гр. {group}, GPA {gpa:.2f}"


if __name__ == "__main__":
    print("ЛР2 — Задание C. Записи студентов\n")

    students = [
        ("Иванов Иван Иванович", "BIVT-25", 4.6),
        ("Петров Пётр", "IKBO-12", 5.0),
        ("Петров Пётр Петрович", "IKBO-12", 5.0),
        ("  сидорова  анна  сергеевна  ", "АВВ-01", 3.999),
    ]
    for student in students:
        print(format_record(student))

    print("\nПримеры некорректных записей:")
    for student in (("", "BIVT-25", 4.6), ("Иванов Иван", "", 4.6),
                    ("Иванов Иван", "BIVT-25", "4.6"),
                    ("Иванов Иван", "BIVT-25", 6.0)):
        try:
            format_record(student)
        except (ValueError, TypeError) as error:
            print(f"{student!r} -> {type(error).__name__}: {error}")

    assert format_record(students[0]) == "Иванов И.И., гр. BIVT-25, GPA 4.60"
    assert format_record(students[3]) == "Сидорова А.С., гр. АВВ-01, GPA 4.00"
    print("\nСамопроверка задания C: OK")
