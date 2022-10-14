import unittest


class ExampleTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_equals(self):
        self.assertEqual(5, 4)
        self.assertEqual(5, 5)
