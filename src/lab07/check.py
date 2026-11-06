"""ЛР7: проверка поиска и сортировок против эталона на случайных данных.

Запуск из корня репозитория: python3 -m src.lab07.check
"""

import random

from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort


def random_list():
    """Случайный список длиной 0..50, значения от -100 до 100, с повторами."""
    n = random.randint(0, 50)
    return [random.randint(-100, 100) for _ in range(n)]


def check_sorting(fn, trials=100):
    """Сравнить fn(nums) со sorted(nums); исходный список не должен меняться."""
    for _ in range(trials):
        nums = random_list()
        original = list(nums)
        result = fn(nums)
        assert result == sorted(nums), f"{fn.__name__} ошиблась на {nums}: {result}"
        assert nums == original, f"{fn.__name__} изменила исходный список: {original} -> {nums}"


def check_search(trials=100):
    """linear_search против list.index; binary_search на отсортированных списках."""
    for _ in range(trials):
        nums = random_list()
        x = random.randint(-110, 110)  # иногда x нет в списке

        try:
            expected = nums.index(x)
        except ValueError:
            expected = -1
        result = linear_search(nums, x)
        assert result == expected, f"linear_search({nums}, {x}) = {result}, ожидалось {expected}"

        b = sorted(nums)
        queries = [x]
        if b:
            queries += [b[0], b[-1]]  # крайние элементы
        for q in queries:
            i = binary_search(b, q)
            if q in b:
                assert 0 <= i < len(b) and b[i] == q, f"binary_search({b}, {q}) = {i}"
            else:
                assert i == -1, f"binary_search({b}, {q}) = {i}, ожидалось -1"


def check_two_sum(trials=100):
    """Оба способа дают пару с нужной суммой или оба None."""
    for _ in range(trials):
        nums = random_list()
        target = random.randint(-200, 200)
        brute = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)
        if brute is None:
            assert fast is None, f"two_sum({nums}, {target}): brute=None, fast={fast}"
        else:
            for pair in (brute, fast):
                assert pair is not None, f"two_sum({nums}, {target}): brute={brute}, fast=None"
                i, j = pair
                assert i < j and nums[i] + nums[j] == target, f"two_sum({nums}, {target}): {pair}"


if __name__ == "__main__":
    random.seed(42)
    trials = 100
    total = 0
    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn, trials)
        total += trials
    check_search(trials)
    total += trials
    check_two_sum(trials)
    total += trials
    print(f"OK: {total} проверок")
