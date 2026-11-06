"""ЛР7: сортировки пузырьком, вставками и выбором.

Каждая функция возвращает новый список и не меняет исходный.
Готовые sorted, .sort(), min, max внутри не используются.
"""


def bubble_sort(nums):
    """Новый список, отсортированный по возрастанию. Исходный не меняется.
    Сложность O(n²); на отсортированных данных — O(n) за счёт флага swapped.

    bubble_sort([3, 1, 2]) -> [1, 2, 3]
    bubble_sort([2, 2, 1]) -> [1, 2, 2]
    bubble_sort([]) -> []
    """
    nums = list(nums)
    n = len(nums)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:  # обменов не было — список уже отсортирован
            break
    return nums


def insertion_sort(nums):
    """Тот же контракт, что у bubble_sort. Сложность O(n²).

    insertion_sort([3, 1, 2]) -> [1, 2, 3]
    """
    nums = list(nums)
    for i in range(1, len(nums)):
        current = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > current:
            nums[j + 1] = nums[j]  # сдвигаем больший элемент вправо
            j -= 1
        nums[j + 1] = current
    return nums


def selection_sort(nums):
    """Тот же контракт, что у bubble_sort. Сложность O(n²).

    selection_sort([3, 1, 2]) -> [1, 2, 3]
    """
    nums = list(nums)
    n = len(nums)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if nums[j] < nums[min_index]:
                min_index = j
        nums[i], nums[min_index] = nums[min_index], nums[i]
    return nums
