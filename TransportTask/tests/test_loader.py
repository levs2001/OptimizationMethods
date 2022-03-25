from data_for_tests import EXPORTER, IMPORTER, M_COST, PROBLEM_FILENAME
import unittest
import loader


class TestLoader(unittest.TestCase):
    def setUp(self):
        with loader.Loader(PROBLEM_FILENAME) as data:
            self.m_cost, self.v_exporter, self.v_importer = data

    def test_exporter(self):
        self.assertEqual(self.v_exporter, EXPORTER)

    def test_importer(self):
        self.assertEqual(self.v_importer, IMPORTER)

    def test_cost_matrix(self):
        self.assertEqual(self.m_cost, M_COST)
