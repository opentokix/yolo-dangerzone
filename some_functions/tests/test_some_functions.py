#!/usr/bin/env python
import unittest
import sys
import os
sys.path.append(os.path.abspath("../main"))
from some_functions import *


class Tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_add_two(self):
        self.assertEqual(add_two(2), 4)

    def test_mul_two(self):
        self.assertEqual(mul_two(2), 4)

    def test_square(self):
        self.assertEqual(square(10), 100)
        self.assertIsNot(square(-1), '< 0')

if __name__ == '__main__':
    unittest.main()
