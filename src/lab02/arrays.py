"""ЛР2. Задание A: операции со списками."""


def check_numbers(nums: list[float | int]) -> None:
    """Проверить, что передан список чисел."""
    if not isinstance(nums, list):
        raise TypeError("Ожидался список чисел")

    for num in nums:
        if isinstance(num, bool) or not isinstance(num, (int, float)):
            raise TypeError("Элементы списка должны быть числами")


def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    """Вернуть минимум и максимум; для пустого списка вызвать ValueError."""
    check_numbers(nums)
    if not nums:
        raise ValueError("Список пуст")

    minimum = maximum = nums[0]
    for num in nums[1:]:
        if num < minimum:
            minimum = num
        if num > maximum:
            maximum = num

    return minimum, maximum


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    """Вернуть уникальные числа по возрастанию без sort() и sorted()."""
    check_numbers(nums)
    unique = []

    for num in nums:
        if num not in unique:
            unique.append(num)

    # Сортируем, сравнивая каждый элемент со следующими.
    for i in range(len(unique)):
        for j in range(i + 1, len(unique)):
            if unique[i] > unique[j]:
                unique[i], unique[j] = unique[j], unique[i]

    return unique


def flatten(mat: list[list | tuple]) -> list:
    """Собрать строки-списки и строки-кортежи в один список."""
    if not isinstance(mat, list):
        raise TypeError("Ожидался список строк")

    result = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError("Каждая строка должна быть списком или кортежем")
        for item in row:
            result.append(item)

    return result


if __name__ == "__main__":
    print("ЛР2 — Задание A. Списки")

    print("\nmin_max:")
    for nums in ([3, -1, 5, 5, 0], [42], [-5, -2, -9], [1.5, 2, 2.0, -3.1]):
        print(f"{nums} -> {min_max(nums)}")
    try:
        min_max([])
    except ValueError:
        print("[] -> ValueError (ожидаемая ошибка)")

    print("\nunique_sorted:")
    for nums in ([3, 1, 2, 1, 3], [], [-1, -1, 0, 2, 2], [1.0, 1, 2.5, 2.5, 0]):
        print(f"{nums} -> {unique_sorted(nums)}")

    print("\nflatten:")
    for mat in ([[1, 2], [3, 4]], [[1, 2], (3, 4, 5)], [[1], [], [2, 3]]):
        print(f"{mat} -> {flatten(mat)}")
    try:
        flatten([[1, 2], "ab"])
    except TypeError:
        print("[[1, 2], 'ab'] -> TypeError (ожидаемая ошибка)")

    # Простые автоматические проверки результатов.
    assert min_max([3, -1, 5, 5, 0]) == (-1, 5)
    assert unique_sorted([3, 1, 2, 1, 3]) == [1, 2, 3]
    assert flatten([[1, 2], (3, 4, 5)]) == [1, 2, 3, 4, 5]
    print("\nСамопроверка задания A: OK")
