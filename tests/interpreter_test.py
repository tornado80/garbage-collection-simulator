import unittest
from garbage_collection_simulator.interpreter import Interpreter


class InterpreterTest(unittest.TestCase):
    def test_print_command(self):
        i = Interpreter(100)
        i.execute_command("L1 = ((a)(b((c)d))ef(g(h)))")
        i.execute_command("Print L1")

    def test_delete_command(self):
        i = Interpreter(100)
        i.execute_command("salam = ((a)(b((c)d))ef(g(h)))")
        i.execute_command("Delete salam from (**")
        i.execute_command("Print salam")

    def test_empty_list_command(self):
        i = Interpreter(100)
        i.execute_command("salam = ()")
        i.execute_command("Print salam")

    def test_make_child_command(self):
        i = Interpreter(100)
        i.execute_command("a = ((((Z)Y)X)TM(A(B(C))))")
        i.execute_command("b = ((V)PQ(R(S)))")
        i.execute_command("Make (ABC) Child of b at (***(** Without Root")
        i.execute_command("Print b")
        i.execute_command("Make b Child of a at (*** Without Root")
        i.execute_command("Print a")

    def test_make_child_with_root_command(self):
        i = Interpreter(100)
        i.execute_command("b = ((V)PQ(R(S)))")
        i.execute_command("Make (ABC) Child of b at (***(** With Root")
        i.execute_command("Print b")

    def test_different_variable_name(self):
        i = Interpreter(100)
        i.execute_command("d222_good_var3 = (((((A(C)B)))))")  # testing variable names with numbers
        i.execute_command("Print d222_good_var3")

    def test_invalid_list_expression_raising_syntax_error(self):
        i = Interpreter(100)
        self.assertRaises(SyntaxError, i.execute_command, "salam = ((*)(*))(8))")  # Invalid list expression raises error

    def test_garbage_collect(self):
        i = Interpreter(100)
        i.execute_command("a = ((((Z)Y)X)TM(A(B(C))))")
        i.execute_command("b = ((V)PQ(R(S)))")
        i.execute_command("c = (123(8)45(6(7)))")
        i.execute_command("Print c")
        i.execute_command("Make (ABC) Child of b at (***(** Without Root")
        i.execute_command("Print b")
        i.execute_command("Make b Child of a at (*** Without Root")
        i.execute_command("Print a")
        i.execute_command("b = (D(E)(F(H))(G))")
        i.execute_command("Print b")
        i.execute_command("c = (B)")
        i.execute_command("Garbage-Collect")  # We can see that list c was garbage collected and returned to memory

if __name__ == '__main__':
    unittest.main()
