import unittest
from data_for_tests import PROBLEM_FINES_FILENAME, FINES_FILENAME, START_PLAN_FINES, RESULT_PLAN_FINES
from loader import Loader
from data_structure import TransportTask
from potential_method import potential_method
from algorithms import north_west_method


# Я не уверен, что решения правильные, у меня нет решенной задачи со штрафами.
class TestLoader(unittest.TestCase):
    def setUp(self):
        with Loader(PROBLEM_FINES_FILENAME) as data:
            m_cost, v_exporter, v_importer = data
        self.task = TransportTask(m_cost, v_exporter, v_importer, FINES_FILENAME)

    def test_start_plan(self):
        self.assertEqual(north_west_method(self.task), START_PLAN_FINES)

    def test_potential_method(self):
        self.assertEqual(potential_method(self.task, START_PLAN_FINES), RESULT_PLAN_FINES)
