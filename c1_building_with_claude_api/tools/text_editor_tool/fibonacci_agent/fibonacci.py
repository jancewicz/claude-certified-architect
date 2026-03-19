"""
Fibonacci sequence module.

This module provides a function to calculate the n-th element of the Fibonacci sequence.
"""


def fibonacci(n):
    """
    Find the n-th element of the Fibonacci sequence.

    The Fibonacci sequence is defined as:
    - F(0) = 0
    - F(1) = 1
    - F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n (int): The position in the Fibonacci sequence (0-indexed).

    Returns:
        int: The n-th Fibonacci number.

    Raises:
        ValueError: If n is negative.
        TypeError: If n is not an integer.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(6)
        8
        >>> fibonacci(10)
        55
    """
    if not isinstance(n, int):
        raise TypeError(f"n must be an integer, got {type(n).__name__}")

    if n < 0:
        raise ValueError(f"n must be non-negative, got {n}")

    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Use iterative approach for efficiency
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr
