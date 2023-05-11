# test_statement.py
import json
import os
import unittest

from docs.ch1codes.ch1python.statement import statement


class TestStatementMethods(unittest.TestCase):

    def test_statement(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '', 'plays.json'))
        with open(file_path, 'r') as f:
            plays = json.load(f)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '', 'invoices.json'))
        with open(file_path, 'r') as f:
            invoices = json.load(f)

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '', 'expect.txt'))
        with open(file_path, 'r') as f:
            content = f.read()
        res = statement(invoices[0], plays)

        self.assertEqual(res, content)


if __name__ == '__main__':
    unittest.main()
