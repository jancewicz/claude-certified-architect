"""
Unit tests for the fibonacci module.

This module contains comprehensive unit tests for the fibonacci function.
"""

import unittest
from fibonacci import fibonacci


class TestFibonacci(unittest.TestCase):
    """Test cases for the fibonacci function."""

    def test_fibonacci_base_cases(self):
        """Test base cases of the Fibonacci sequence."""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_small_numbers(self):
        """Test Fibonacci sequence for small numbers."""
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(3), 2)
        self.assertEqual(fibonacci(4), 3)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)

    def test_fibonacci_larger_numbers(self):
        """Test Fibonacci sequence for larger numbers."""
        self.assertEqual(fibonacci(7), 13)
        self.assertEqual(fibonacci(8), 21)
        self.assertEqual(fibonacci(9), 34)
        self.assertEqual(fibonacci(10), 55)
        self.assertEqual(fibonacci(15), 610)
        self.assertEqual(fibonacci(20), 6765)

    def test_fibonacci_negative_input(self):
        """Test that negative input raises ValueError."""
        with self.assertRaises(ValueError):
            fibonacci(-1)

        with self.assertRaises(ValueError):
            fibonacci(-10)

    def test_fibonacci_non_integer_input(self):
        """Test that non-integer input raises TypeError."""
        with self.assertRaises(TypeError):
            fibonacci(5.5)

        with self.assertRaises(TypeError):
            fibonacci("5")

        with self.assertRaises(TypeError):
            fibonacci(None)

    def test_fibonacci_sequence_property(self):
        """Test that the Fibonacci property holds: F(n) = F(n-1) + F(n-2)."""
        for n in range(2, 15):
            self.assertEqual(
                fibonacci(n),
                fibonacci(n - 1) + fibonacci(n - 2),
                f"Fibonacci property failed at n={n}",
            )

    def test_fibonacci_is_increasing(self):
        """Test that the Fibonacci sequence is monotonically increasing."""
        for n in range(1, 20):
            self.assertGreater(
                fibonacci(n),
                fibonacci(n - 1),
                f"Fibonacci sequence is not increasing at n={n}",
            )

    def test_fibonacci_returns_integer(self):
        """Test that fibonacci function always returns an integer."""
        for n in range(0, 20):
            result = fibonacci(n)
            self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main()
