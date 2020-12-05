from garbage_collection_simulator.interpreter import Interpreter
import sys
command_line_arguments = sys.argv[1:]


def show_help():
    print("""
        Following options are supported:
            -x /path/to/file or --execute /path/to/file
            -i or --interactive-shell
        Note that after execution and interactive shell options should be followed by the memory size option like below:
            -m NUM or --memory-size=NUM
        Thus a complete command would be look like:
            "$ python3 main.py -x -m 200 hello.txt"
        Or:
            "$ python3 main.py -i -m 200"
        Obviously "-x /path/to/file" could be replaced by "--execute /path/to/file". 
        Also "-i" could be replace by "--interactive-shell".
        Instead of "-m X" you can use "--memory-size=X". 
    """)


def start_interactive_shell():
    try:
        if command_line_arguments[1] == "-m" and command_line_arguments[2].isdecimal():
            memory_size = int(command_line_arguments[2])
        elif command_line_arguments[1].split("=")[0] == "--memory-size" and command_line_arguments[1].split("=")[1].isdecimal():
            memory_size = int(command_line_arguments[1].split("=")[1])
        else:
            raise IndexError()
        if memory_size > 100:
            proceed_or_not = input(f"""
            You are going to allocate more than {memory_size} nodes or {4 * memory_size} cells. Are you sure? (y/n) """)
            if proceed_or_not == "n":
                print("Execution terminated.")
        interpreter = Interpreter(memory_size)
        print("""
        Following command are implemented:
            1. Print $VAR_NAME
            2. $VAR_NAME = $LIST_EXPRESSION
            3. $VAR_NAME = $VAR_NAME 
            4. Delete $VAR_NAME from $NODE_EXPRESSION
            5. Garbage-Collect
            6. Make $VAR_NAME Child of $VAR_NAME at $NODE_EXPRESSION With Root
            7. Make $VAR_NAME Child of $VAR_NAME at $NODE_EXPRESSION Without Root
            8. Make $LIST_EXPRESSION Child of $VAR_NAME at $NODE_EXPRESSION With Root
            9. Make $LIST_EXPRESSION Child of $VAR_NAME at $NODE_EXPRESSION Without Root
            10. Set $VAR_NAME at $NODE_EXPRESSION Label to $NODE_LABEL
        Examples:
            1. Print Salam
            2. salam_beto2 = (ABC(D(F))G(H))
            3. Salam = salam_beto2
            4. Delete salam_beto2 from (***(**
            5. Garbage-Collect
            6. Make Salam Child of salam_beto2 at (***(* With Root
            7. Make Salam Child of salam_beto2 at (***(* Without Root
            8. Make (PQ(R(T))S) Child of salam_beto2 at (***(* With Root
            9. Make (PQ(R(T))S) Child of salam_beto2 at (***(* Without Root
            10. Set salam_beto2 at (** Label to K
        Notes:
            0. Check the examples on the "tests" directory at "interpreter_test.py".
            1. Garbage-Collect command prints the traversed lists (those marked as not garbage).
            2. You can assign variables to each other, so the left hand side variable points to the right hand side variable list.
            3. You can change the label of a node to a single character.
            4. Make Child commands have options "With/Without Root". Use "Without Root" for ordinary "Make Child".
        Syntax:
            $NODE_EXPRESSION: A valid node expression containing "(" and "*" which the latter stands for node.
            $NODE_LABEL: A single character with ascii code between 33 and 126.
            $VAR_NAME: A string containing underscores, digits (except at beginning), capital and small alphabets.
            $LIST_EXPRESSION: Obvious.
        """)
        while True:
            cmd = input(">>> ")
            try:
                interpreter.execute_command(cmd)
            except Exception as err:
                print(type(err), err)
    except IndexError:
        print("ERROR: Memory options not specified correctly. Use -m [memory size] or --memory-size=[memory size].")
    except FileNotFoundError:
        print("ERROR: Module not found!")


def execute_file():
    try:
        if command_line_arguments[1] == "-m" and command_line_arguments[2].isdecimal():
            try:
                file_path = command_line_arguments[3]
            except IndexError:
                raise FileNotFoundError()
            memory_size = int(command_line_arguments[2])
        elif command_line_arguments[1].split("=")[0] == "--memory-size" and command_line_arguments[1].split("=")[1].isdecimal():
            try:
                file_path = command_line_arguments[2]
            except IndexError:
                raise FileNotFoundError()
            memory_size = int(command_line_arguments[1].split("=")[1])
        else:
            raise IndexError()
        if memory_size > 100:
            proceed_or_not = input(f"""
            You are going to allocate more than {memory_size} nodes or {4 * memory_size} cells. Are you sure? (y/n) """)
            if proceed_or_not == "n":
                print("Execution terminated.")
                return
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()
        interpreter = Interpreter(memory_size)
        for line in lines:
            interpreter.execute_command(line[:-1])  # removing \n
    except IndexError:
        print("ERROR: Memory options not specified correctly. Use -m [memory size] or --memory-size=[memory size].")
    except FileNotFoundError:
        print("ERROR: Module not found!")


print("Garbage Collection Simulator - 2020")
if len(command_line_arguments) == 0:
    print("ERROR: No options passed. Use -h or --help to get more information.")
else:
    if command_line_arguments[0] == "-i" or command_line_arguments[0] == "--interactive-shell":
        start_interactive_shell()
    elif command_line_arguments[0] == "-h" or command_line_arguments[0] == "--help":
        show_help()
    elif command_line_arguments[0] == "-x" or command_line_arguments[0] == "--execute":
        execute_file()
    else:
        print("ERROR: No options passed. Use -h or --help to get more information.")
