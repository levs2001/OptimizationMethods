import unittest
from data_for_tests import EXPORTER, IMPORTER, M_COST, START_PLAN, START_COST
from data_structure import TransportTask
from algorithms import north_west_method, calculate_function


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.task = TransportTask(M_COST, EXPORTER, IMPORTER)

    def test_start_plan(self):
        ans = north_west_method(self.task)
        self.assertEqual(ans, START_PLAN)

    def test_calculate_function(self):
        self.assertEqual(calculate_function(START_PLAN, self.task.m_cost), START_COST)
