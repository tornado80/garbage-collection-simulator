import unittest
from garbage_collection_simulator.data_structures import Memory, NotEnoughMemoryCellsError


class MemoryTest(unittest.TestCase):
    def test__init_avail_list(self):
        memory = Memory(4)
        self.assertEqual(
            memory.status(),
            [
                (None, None, 4, None),
                (None, None, 8, None),
                (None, None, 12, None),
                (None, None, None, None),
            ]
        )

    def test_allocate_cell(self):
        memory = Memory(4)
        cell1 = memory.allocate_cell()
        memory.set_cell_label(cell1, "A")
        cell2 = memory.allocate_cell()
        memory.set_cell_label(cell2, "B")
        self.assertEqual(
            memory.status(),
            [
                (None, "A", None, None),
                (None, "B", None, None),
                (None, None, 12, None),
                (None, None, None, None),
            ]
        )

    def test_free_node(self):
        memory = Memory(4)
        cell_a = memory.allocate_cell()
        memory.set_cell_label(cell_a, "A")
        cell_b = memory.allocate_cell()
        memory.set_cell_label(cell_b, "B")
        memory.free_cell(cell_a)
        memory.set_cell_label(memory.allocate_cell(), "C")
        memory.set_cell_label(memory.allocate_cell(), "D")
        memory.free_cell(cell_b)
        memory.set_cell_label(memory.allocate_cell(), "E")
        self.assertEqual(
            memory.status(),
            [
                (None, "C", None, None),
                (None, "E", None, None),
                (None, "D", None, None),
                (None, None, None, None),
            ]
        )

    def test_allocate_cell_raising_error(self):
        memory = Memory(5)
        for _ in range(5):
            memory.allocate_cell()
        self.assertRaises(NotEnoughMemoryCellsError, memory.allocate_cell)


if __name__ == '__main__':
    unittest.main()
