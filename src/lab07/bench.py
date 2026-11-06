"""ЛР7: замеры поиска и сортировок через timeit.

Запуск из корня репозитория: python3 -m src.lab07.bench
Результат: таблица в консоли и data/lab07/bench.csv.
"""

import random
import timeit

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

REPEAT = 3  # повторов замера, берём минимум
SLOW_LIMIT = 10_000  # квадратичные сортировки на большем n не запускаем: > 60 с
CSV_PATH = "data/lab07/bench.csv"


def measure(func):
    """Минимальное время одного запуска func из REPEAT повторов, в секундах."""
    return min(timeit.repeat(func, number=1, repeat=REPEAT))


def bench_sorts():
    """Три свои сортировки против sorted на одних и тех же данных."""
    rows = []
    for n in (1_000, 10_000, 100_000):
        data = [random.randint(0, 10**6) for _ in range(n)]
        rows.append(("sort", n, "sorted", measure(lambda: sorted(data))))
        for fn in (bubble_sort, insertion_sort, selection_sort):
            if n > SLOW_LIMIT:
                rows.append(("sort", n, fn.__name__, "> 60"))
            else:
                rows.append(("sort", n, fn.__name__, measure(lambda: fn(data))))
    return rows


def bench_search():
    """10 000 запросов к списку из 100 000: линейный против бинарного."""
    n = 100_000
    nums = [random.randint(0, 10**6) for _ in range(n)]
    queries = [random.choice(nums) for _ in range(10_000)]
    sorted_nums = sorted(nums)
    return [
        ("search", n, "linear_search", measure(lambda: [linear_search(nums, q) for q in queries])),
        ("search", n, "sorted_for_binary", measure(lambda: sorted(nums))),
        ("search", n, "binary_search", measure(lambda: [binary_search(sorted_nums, q) for q in queries])),
    ]


def bench_two_sum():
    """Перебор пар против словаря. Ответ — только два последних числа."""
    rows = []
    for n in (1_000, 10_000):
        nums = random.sample(range(10**6), n - 2) + [10**6, 10**6 + 1]
        target = 2 * 10**6 + 1  # остальные числа меньше 10**6, другой пары нет
        for fn in (two_sum_brute, two_sum_fast):
            rows.append(("two_sum", n, fn.__name__, measure(lambda: fn(nums, target))))
    return rows


def print_table(rows):
    print(f"{'task':<8} | {'n':>7} | {'impl':<18} | {'seconds':>10}")
    print("-" * 53)
    for task, n, impl, seconds in rows:
        print(f"{task:<8} | {n:>7} | {impl:<18} | {seconds:>10}")


if __name__ == "__main__":
    random.seed(42)
    print("Идут замеры, это займёт около минуты...")
    rows = bench_sorts() + bench_search() + bench_two_sum()
    rows = [(task, n, impl, s if isinstance(s, str) else f"{s:.6f}") for task, n, impl, s in rows]
    print_table(rows)
    write_csv(rows, CSV_PATH, header=("task", "n", "impl", "seconds"))
    print(f"Готово: {CSV_PATH}")
