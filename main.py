from garbage_collection_simulator.interpreter import Interpreter
import sys
command_line_arguments = sys.argv[1:]


def show_help():
    print("""
        Following options are supported:
            -x /path/to/file or --execute /path/to/file
            -i or --interactive-shell
        Note that execution and interactive shell options should be followed by the memory size option like below:
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
            proceed_or_not = input(f"""You are going to allocate more than {memory_size} nodes or {4 * memory_size} cells. Are you sure? ("n" to exit) """)
            if proceed_or_not == "n":
                print("Execution terminated.")
                return
        interpreter = Interpreter(memory_size)
        while True:
            cmd = input(">>> ")
            try:
                interpreter.execute_command(cmd)
            except Exception as err:
                print(type(err), err)
    except IndexError:
        print("ERROR: Memory options not specified correctly. Use -m [memory size] or --memory-size=[memory size].")


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
        line_number = 1
        for line in lines:
            try:
                interpreter.execute_command(line[:-1])  # removing \n
                line_number += 1
            except Exception as err:
                print(f"Line number #{line_number}", type(err), err)
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
