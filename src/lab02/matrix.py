"""ЛР2. Задание B: операции с матрицами."""


def check_matrix(mat: list[list[float | int]]) -> None:
    """Проверить, что матрица состоит из строк одинаковой длины."""
    if not isinstance(mat, list):
        raise TypeError("Матрица должна быть списком")
    if not mat:
        return

    if not isinstance(mat[0], list):
        raise TypeError("Строки матрицы должны быть списками")

    columns = len(mat[0])
    for row in mat:
        if not isinstance(row, list):
            raise TypeError("Строки матрицы должны быть списками")
        if len(row) != columns:
            raise ValueError("У строк матрицы разная длина")
        for num in row:
            if isinstance(num, bool) or not isinstance(num, (int, float)):
                raise TypeError("Элементы матрицы должны быть числами")


def transpose(mat: list[list[float | int]]) -> list[list]:
    """Поменять строки и столбцы местами; [] преобразовать в []."""
    check_matrix(mat)
    if not mat:
        return []

    result = []
    for j in range(len(mat[0])):
        row = []
        for i in range(len(mat)):
            row.append(mat[i][j])
        result.append(row)

    return result


def row_sums(mat: list[list[float | int]]) -> list[float]:
    """Вернуть суммы по каждой строке матрицы."""
    check_matrix(mat)
    result = []
    for row in mat:
        result.append(sum(row))
    return result


def col_sums(mat: list[list[float | int]]) -> list[float]:
    """Вернуть суммы по каждому столбцу матрицы."""
    check_matrix(mat)
    if not mat:
        return []

    result = []
    for j in range(len(mat[0])):
        total = 0
        for i in range(len(mat)):
            total += mat[i][j]
        result.append(total)

    return result


if __name__ == "__main__":
    print("ЛР2 — Задание B. Матрицы")

    mat = [[1, 2, 3], [4, 5, 6]]
    print("\nИсходная матрица:", mat)
    print("transpose:", transpose(mat))
    print("row_sums:", row_sums(mat))
    print("col_sums:", col_sums(mat))

    print("\nДополнительные примеры:")
    print("Строка -> столбец:", transpose([[1, 2, 3]]))
    print("Столбец -> строка:", transpose([[1], [2], [3]]))
    print("Пустая матрица:", transpose([]))
    print("Суммы с отрицательными числами:", row_sums([[-1, 1], [10, -10]]))

    try:
        transpose([[1, 2], [3]])
    except ValueError:
        print("Рваная матрица -> ValueError (ожидаемая ошибка)")

    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert row_sums(mat) == [6, 15]
    assert col_sums(mat) == [5, 7, 9]
    print("\nСамопроверка задания B: OK")
