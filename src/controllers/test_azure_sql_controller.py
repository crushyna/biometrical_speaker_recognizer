import unittest

from src.controllers.azure_sql_controller import SQLController


class SQLControllerTest(unittest.TestCase):

    def test_something(self):
        self.assertIsInstance(SQLController.test_connection_query(), int)
        self.assertEqual(SQLController.test_connection_query(), 1)


if __name__ == '__main__':
    unittest.main()
