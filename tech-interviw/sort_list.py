"""
Задача - из случайных элементов выбрать n максимальных
"""

import random
import time
from timeit import timeit
from typing import List


class Stack:
    # Методы за O(1)
    def __init__(self):
        self.stack = []
        self.men_nums = []

    def push(self, num):
        self.stack.append(num)
        if not self.min_nums or num <= self.min_nums[-1]:
            self.min_nums.append(num)

    def pop(self):
        num = self.stack.pop()
        if num == self.min_nums[-1]:
            self.min_nums.pop()
        return num

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_nums[-1]

    def is_empty(self):
        return len(self.stack) == 0

    def __len__(self):
        return len(self.stack)


# Вывести первый объект из списка O(1)/O(n)
def get_first_matching_object(predicate, objects=None):
    if objects is None:
        objects = []
    for obj in objects:
        if predicate(obj):
            return obj  # if true (match)
    return None


# get_first_matching_object(lambda x: x == 1, [1, 2, 3, 4])

# Написать декоратор к исключениям
import functools


def decorator(exceptions):
    def wrapper(func):
        @functools.wraps(func)
        def wrapper1(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                for ex in exceptions:
                    if isinstance(e, ex):
                        raise e
            return res

        return wrapper1

    return wrapper


# Вернуть n отсортирвоанных чисел
random.seed(0)
l = random.sample(range(0, 10000), 1)


def get_n_max_sorted(l, n):
    return sorted(l, reverse=True)[:n]


import heapq


def get_n_max_sorted_h(l, n):
    return heapq.nlargest(n, l)


class Solution:
    # декоратор в классе
    @staticmethod
    def time_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(f"Elapsed time: {(end - start) * 1000:.3f}ms")

        return wrapper

    def _swap(self, nums, a, b):
        nums[a], nums[b] = nums[b], nums[a]

    # последовательно сравнивает O(n^2)
    @time_func
    def bubble_sort(self, nums):
        n = len(nums)
        for i in range(n):
            for j in range(0, n - i - 1):
                if nums[j] > nums[j + 1]:
                    self._swap(nums, j, j + 1)

    # рекурсивно, деля на левую(меньшую) и правую(большую) части O(n*log(n))/O(n)
    def quicksort(self, nums, low=None, high=None):
        if low is None:
            low = 0
        if high is None:
            high = len(nums) - 1
        if low < high:
            pivot = nums[high]
            i = low - 1
            for j in range(low, high):
                if nums[j] < pivot:
                    i += 1
                    self._swap(nums, i, j)
            self._swap(nums, i + 1, high)
            pi = i + 1
            self.quicksort(nums, low, pi - 1)
            self.quicksort(nums, pi + 1, high)

    def _heapify(self, nums, len_arr, node):
        large = node
        left_leaf = 2 * node + 1
        right_leaf = 2 * node + 2

        if left_leaf < len_arr and nums[left_leaf] > nums[large]:
            large = left_leaf

        if right_leaf < len_arr and nums[right_leaf] > nums[large]:
            large = right_leaf

        if large != node:
            self._swap(nums, large, node)
            self._heapify(nums, len_arr, large)

    # б-дерево O(n*log(n))
    @time_func
    def heap_sort(self, nums):
        len_arr = len(nums)
        if len_arr == 1:
            return nums
        for i in range(len_arr // 2 - 1, -1, -1):
            self._heapify(nums, len_arr, i)
        for i in range(len_arr - 1, 0, -1):
            self._swap(nums, 0, i)
            self._heapify(nums, i, 0)

    # есть ли дубликаты
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

    # вычисляет массив, каждый элемент которого равен произведению всех элементов, кроме текущего в исходном массиве
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        length = len(nums)
        left_products = [1] * length
        right_products = [1] * length
        result = [0] * length
        for i in range(1, length):
            left_products[i] = left_products[i - 1] * nums[i - 1]
        for i in range(length - 2, -1, -1):
            right_products[i] = right_products[i + 1] * nums[i + 1]
        for i in range(length):
            result[i] = left_products[i] * right_products[i]

        return result


if __name__ == "__main__":
    print(get_n_max_sorted(l, 5))
    print(timeit(lambda: get_n_max_sorted(l, 5), number=10000))
    print(get_n_max_sorted_h(l, 5))
    print(timeit(lambda: get_n_max_sorted_h(l, 5), number=10000))
    elements = [39, 12, 18, 85, 72, 10, 2, 18]
    print("Unsorted list is:")
    print(elements)
    my_sort = Solution()
    my_sort.bubble_sort(elements)
    print("Sorted list by bubble is:")
    print(elements)
    elements = [39, 12, 18, 85, 72, 10, 2, 18]
    start = time.time()
    my_sort.quicksort(elements)
    end = time.time()
    print(f"Elapsed time: {(end - start) * 1000:.3f}ms")
    print("Sorted list by quick is:")
    print(elements)
    elements = [39, 12, 18, 85, 72, 10, 2, 18]
    my_sort.heap_sort(elements)
    print("Sorted list by heap_sort is:")
    print(elements)
