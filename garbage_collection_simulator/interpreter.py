from garbage_collection_simulator.data_structures import Memory, GeneralList, Stack


def make_child_by_variable_command(list1_name: str, list2_name: str, node_expression: str, memory: Memory, variables: dict):
    list1 = variables[list1_name]
    list2 = variables[list2_name]
    node, _ = list2.find_node_by_expression(node_expression)
    memory.set_node_down(node, memory.get_node_down(list1.root))


def make_child_by_variable_with_root_command(list1_name: str, list2_name: str, node_expression: str, memory: Memory, variables: dict):
    list1 = variables[list1_name]
    list2 = variables[list2_name]
    node, _ = list2.find_node_by_expression(node_expression)
    memory.set_node_down(node, list1.root)


def make_child_by_list_expression_command(list_expression: str, list2_name: str, node_expression: str, memory: Memory, variables: dict):
    list2 = variables[list2_name]
    list1 = GeneralList.convert_expression_to_general_list(memory, list_expression)
    node, _ = list2.find_node_by_expression(node_expression)
    memory.set_node_down(node, memory.get_node_down(list1.root))


def make_child_by_list_expression_with_root_command(list_expression: str, list2_name: str, node_expression: str, memory: Memory, variables: dict):
    list2 = variables[list2_name]
    list1 = GeneralList.convert_expression_to_general_list(memory, list_expression)
    node, _ = list2.find_node_by_expression(node_expression)
    memory.set_node_down(node, list1.root)


def delete_command(var_name: str, node_expression: str, memory: Memory, variables: dict):
    general_list = variables[var_name]
    node, _ = general_list.find_node_by_expression(node_expression)
    memory.set_node_down(node, None)


def print_command(var_name, variables: dict):
    general_list = variables[var_name]
    print(general_list)


def garbage_collect_command(memory: Memory, variables: dict):
    memory.garbage_collect(*variables.values())


def set_node_label_command(var_name1: str, node_expression: str, label: str, memory: Memory, variables: dict):
    list1 = variables[var_name1]
    node, _ = list1.find_node_by_expression(node_expression)
    memory.set_node_label(node, label)


def assignment_command(var_name: str, list_expression: str, memory: Memory, variables: dict):
    variables[var_name] = GeneralList.convert_expression_to_general_list(memory, list_expression)


def assignment_between_variables_command(var_name1: str, var_name2: str, variables: dict):
    variables[var_name1] = variables[var_name2]


class UndefinedSequenceError(SyntaxError):
    pass


def is_node_label_valid(node_label: str):
    if len(node_label) == 1 and 33 <= ord(node_label[0]) <= 126:
        return True
    return False


def is_variable_name_valid(name: str) -> bool:
    if name[0].isdigit():
        return False
    if name.replace("_", "").isalnum():
        return True
    return False


def is_node_expression_valid(node_expression: str) -> bool:
    for ch in node_expression:
        if ch != "*" and ch != "(":
            return False
    return True


def is_list_expression_valid(list_expression: str) -> bool:
    stack = Stack(Memory(len(list_expression)))
    for ch in list_expression:
        if ch == "(":
            stack.push(ch)
        elif ch == ")":
            if stack.is_empty():
                return False
            else:
                stack.pop()
    if stack.is_empty():
        return True
    else:
        return False


class Interpreter:
    # This Syntax dictionary identifies the language syntax.
    # Tuples' first elements is the executor function.
    # The second and third elements are booleans showing whether respectively Memory, or Variables list are needed.
    Syntax = {
        "Make": {
            "$VAR_NAME": {
                "Child": {
                    "of": {
                        "$VAR_NAME": {
                            "at": {
                                "$NODE_EXPRESSION": {
                                    "Without": {
                                        "Root": (make_child_by_variable_command, True, True)
                                    },
                                    "With": {
                                        "Root": (make_child_by_variable_with_root_command, True, True)
                                    }
                                }
                            }
                        }
                    }
                },
            },
            "$LIST_EXPRESSION": {
                "Child": {
                    "of": {
                        "$VAR_NAME": {
                            "at": {
                                "$NODE_EXPRESSION": {
                                    "Without": {
                                        "Root": (make_child_by_list_expression_command, True, True)
                                    },
                                    "With": {
                                        "Root": (make_child_by_list_expression_with_root_command, True, True)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "Set": {
            "Label": {
                "of": {
                    "$VAR_NAME": {
                        "at": {
                            "$NODE_EXPRESSION": {
                                "to": {
                                    "$NODE_LABEL": (set_node_label_command, True, True)
                                }
                            }
                        }
                    }
                }
            },
            "$VAR_NAME": {
                "at": {
                    "$NODE_EXPRESSION": {
                        "Label": {
                            "to": {
                                "$NODE_LABEL": (set_node_label_command, True, True)
                            }
                        }
                    }
                }
            }
        },
        "Delete": {
            "$VAR_NAME": {
                "from": {
                    "$NODE_EXPRESSION": (delete_command, True, True)
                }
            }
        },
        "Print": {
            "$VAR_NAME": (print_command, False, True)
        },
        "Garbage-Collect": (garbage_collect_command, True, True),
        "$VAR_NAME": {
            "=": {
                "$LIST_EXPRESSION": (assignment_command, True, True),
                "$VAR_NAME": (assignment_between_variables_command, False, True)
            }
        }
    }
    Controls = {
        "$VAR_NAME": is_variable_name_valid,
        "$NODE_EXPRESSION": is_node_expression_valid,
        "$LIST_EXPRESSION": is_list_expression_valid,
        "$NODE_LABEL": is_node_label_valid
    }

    def __init__(self, memory_size):
        self.__memory = Memory(memory_size)
        self.__variables = {}

    def execute_command(self, command):
        words = command.split()
        kwargs = {}
        args = []
        d = Interpreter.Syntax
        for word in words:
            if not isinstance(d, dict):
                raise SyntaxError(f"Expected line finished.")
            if word not in d:
                raise_error = True
                for key, valid in Interpreter.Controls.items():
                    if key in d:
                        if valid(word):
                            raise_error = False
                            args.append(word)
                            d = d[key]  # going deeper in the syntax tree
                            break
                if raise_error:
                    raise SyntaxError(f"Expected one of following valid terms: {d.keys()}, got {word}.")
            else:
                d = d[word]  # going deeper in the syntax tree
        if isinstance(d, tuple):  # d is the function
            if d[1]:
                kwargs["memory"] = self.__memory
            if d[2]:
                kwargs["variables"] = self.__variables
            d[0](*args, **kwargs)  # execute command
        else:
            raise SyntaxError(f"Expected one of following valid terms: {d.keys()}, got nothing.")
