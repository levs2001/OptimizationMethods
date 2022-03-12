import unittest
from data_for_tests import EXPORTER, IMPORTER, M_COST, START_PLAN, RESULT_PLAN
from data_structure import TransportTask
from potential_method import potential_method


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.task = TransportTask(M_COST, EXPORTER, IMPORTER)

    def test_potential_method(self):
        self.assertEqual(potential_method(self.task, START_PLAN), RESULT_PLAN)
