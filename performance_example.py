"""
Example file with performance-critical functions for testing.
"""

import time
import random
from typing import List


def bubble_sort(data: List[int]) -> List[int]:
    """
    Bubble sort algorithm - O(n²) complexity.
    Performance critical: should complete within reasonable time.
    """
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def fibonacci(n: int) -> int:
    """
    Recursive Fibonacci - exponential complexity.
    Performance critical: should handle reasonable input sizes.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def binary_search(arr: List[int], target: int) -> int:
    """
    Binary search algorithm - O(log n) complexity.
    Performance critical: should be very fast.
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def process_large_dataset(data: List[str]) -> dict:
    """
    Process large dataset - O(n) complexity.
    Performance critical: memory usage and execution time.
    """
    result = {}
    for item in data:
        if item not in result:
            result[item] = 0
        result[item] += 1
    return result


def simple_function(x: int) -> int:
    """Simple function - no performance concerns."""
    return x * 2
