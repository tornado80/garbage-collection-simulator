import unittest
from garbage_collection_simulator.data_structures import Memory, NotEnoughMemoryNodesError, \
    GeneralList, Stack, StackEmptyError


class MemoryTest(unittest.TestCase):
    def test_status(self):
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

    def test_allocate_node(self):
        memory = Memory(4)
        node1 = memory.allocate_node()
        memory.set_node_label(node1, "A")
        node2 = memory.allocate_node()
        memory.set_node_label(node2, "B")
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
        node_a = memory.allocate_node()
        memory.set_node_label(node_a, "A")
        node_b = memory.allocate_node()
        memory.set_node_label(node_b, "B")
        memory.free_node(node_a)
        memory.set_node_label(memory.allocate_node(), "C")
        memory.set_node_label(memory.allocate_node(), "D")
        memory.free_node(node_b)
        memory.set_node_label(memory.allocate_node(), "E")
        self.assertEqual(
            memory.status(),
            [
                (None, "C", None, None),
                (None, "E", None, None),
                (None, "D", None, None),
                (None, None, None, None),
            ]
        )

    def test_allocate_node_raising_error(self):
        memory = Memory(5)
        for _ in range(5):
            memory.allocate_node()
        self.assertRaises(NotEnoughMemoryNodesError, memory.allocate_node)


class StackTest(unittest.TestCase):
    def test_push(self):
        mem = Memory(5)
        stack = Stack(mem)
        stack.push("A")
        stack.push("B")
        stack.push("C")
        self.assertEqual("C", stack.top())

    def test_pop(self):
        mem = Memory(5)
        stack = Stack(mem)
        stack.push("A")
        stack.push("B")
        stack.push("C")
        stack.pop()
        self.assertEqual("B", stack.top())

    def test_top_raising_error(self):
        mem = Memory(5)
        stack = Stack(mem)
        stack.push("A")
        stack.push("B")
        stack.pop()
        stack.pop()
        self.assertRaises(StackEmptyError, stack.top)


class GeneralListTest(unittest.TestCase):
    def test_convert_expression_to_general_list(self):
        memory = Memory(100)
        result_list = GeneralList.convert_expression_to_general_list(memory, "(a(b(c)d)ef(g)((i)h))")
        self.assertEqual(str(result_list), "(a(b(c)d)ef(g)((i)h))")

    def test_find_node_by_expression(self):
        memory = Memory(100)
        result_list = GeneralList.convert_expression_to_general_list(memory, "(a(b(c)d)ef(g)((i)h))")
        _, actual = result_list.find_node_by_expression("(*(*(*")
        self.assertEqual(actual, "c")


if __name__ == '__main__':
    unittest.main()
