import unittest
from data_for_tests import EXPORTER, IMPORTER, M_COST, M_COST_FINES, EXPORTER_INCOMP, FINES_FILENAME
from data_structure import TransportTask


class TestLoader(unittest.TestCase):
    def setUp(self):
        self.closed_task = TransportTask(M_COST, EXPORTER, IMPORTER)
        self.task_fines = TransportTask(M_COST, EXPORTER_INCOMP, IMPORTER, FINES_FILENAME)

    def test_exporter(self):
        self.assertEqual(self.closed_task.v_exporter, EXPORTER)
        fine_exporter = EXPORTER_INCOMP.copy()
        fine_exporter.append(sum(IMPORTER) - sum(EXPORTER_INCOMP))
        self.assertEqual(self.task_fines.v_exporter, fine_exporter)

    def test_importer(self):
        self.assertEqual(self.closed_task.v_importer, IMPORTER)

    def test_cost_matrix(self):
        self.assertEqual(self.closed_task.m_cost, M_COST)
        self.assertEqual(self.task_fines.m_cost, M_COST_FINES)
