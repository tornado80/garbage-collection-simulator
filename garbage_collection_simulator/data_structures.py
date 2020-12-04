class NotEnoughMemoryNodesError(MemoryError):
    pass


class StackEmptyError(ValueError):
    pass


class Memory:
    def __init__(self, size):
        """
        A memory simulator instance is created with given number of nodes.
        Each node occupies 4 consequent indices with names: tag, label, next, down.
        Thus nodes array have 4 * size indices.
        """
        self.__nodes = [None] * (size * 4)
        self.__size = size
        self.__avail_list_head = 0
        self.__init_avail_list()

    def __init_avail_list(self):
        for i in range(0, 4 * (self.__size - 1), 4):
            self.set_node_next(i, i + 4)

    def allocate_node(self, new_label = None, new_down = None, new_next = None):
        if self.__avail_list_head is None:
            raise NotEnoughMemoryNodesError("Can not allocate nodes due to insufficient memory space.")
        next_avail_node = self.get_node_next(self.__avail_list_head)
        allocated_node = self.__avail_list_head
        self.__avail_list_head = next_avail_node
        self.set_node_next(allocated_node, new_next)
        self.set_node_down(allocated_node, new_down)
        self.set_node_label(allocated_node, new_label)
        return allocated_node

    def free_node(self, node):
        self.set_node_next(node, self.__avail_list_head)
        self.__avail_list_head = node

    def set_node_next(self, node, new_next):
        self.__nodes[node + 2] = new_next

    def set_node_down(self, node, new_down):
        self.__nodes[node + 3] = new_down

    def set_node_label(self, node, new_label):
        self.__nodes[node + 1] = new_label

    def get_node_label(self, node):
        return self.__nodes[node + 1]

    def get_node_down(self, node):
        return self.__nodes[node + 3]

    def get_node_next(self, node):
        return self.__nodes[node + 2]

    def __get_node_tag(self, node):
        return self.__nodes[node]

    def __set_node_tag(self, node, new_tag):
        self.__nodes[node] = new_tag

    def status(self):
        return [
            (
                self.__nodes[4 * i],  # tag
                self.__nodes[4 * i + 1],  # label
                self.__nodes[4 * i + 2],  # next
                self.__nodes[4 * i + 3]  # down
            ) for i in range(self.__size)
        ]

    def __str__(self):
        return "\n".join(
            [
                f"node #{i + 1} : "
                f"(tag = {self.__nodes[4 * i]}, "
                f"label = {self.__nodes[4 * i + 1]}, "
                f"next = {self.__nodes[4 * i + 2]}, "
                f"down = {self.__nodes[4 * i + 3]})" for i in range(self.__size)
            ]
        )

    def garbage_collect(self, *roots_list):
        pass


class Stack:
    def __init__(self, memory: Memory):
        self.__top = None
        self.__memory = memory

    def top(self):
        if self.is_empty():
            raise StackEmptyError("Stack is empty.")
        return self.__memory.get_node_label(self.__top)

    def is_empty(self):
        return self.__top is None

    def push(self, element):
        new_node = self.__memory.allocate_node(new_label = element, new_down = self.__top)
        self.__top = new_node

    def pop(self):
        top_element = self.__memory.get_node_label(self.__top)
        top_node = self.__top
        self.__top = self.__memory.get_node_down(self.__top)
        self.__memory.free_node(top_node)
        return top_element


class GeneralList:
    def __init__(self, memory, root):
        self.__memory = memory
        self.__root = root

    @classmethod
    def convert_expression_to_general_list(cls, memory: Memory, expression: str):
        ptr_to_ptr, _ = cls.__convert_expression_to_general_list(memory, list(expression), 0)
        return cls(memory, ptr_to_ptr)

    @staticmethod
    def __convert_expression_to_general_list(memory: Memory, expression: list, idx):
        first_node = None
        previous_node = first_node
        while idx < len(expression):
            if expression[idx] == "(":
                new_node = memory.allocate_node()
                if previous_node is not None:
                    memory.set_node_next(previous_node, new_node)
                else:
                    first_node = new_node
                previous_node = new_node
                down_node, idx = GeneralList.__convert_expression_to_general_list(memory, expression, idx + 1)
                memory.set_node_down(new_node, down_node)
            elif expression[idx] == ")":
                return first_node, idx + 1
            else:
                new_node = memory.allocate_node(new_label = expression[idx])
                if previous_node is not None:
                    memory.set_node_next(previous_node, new_node)
                else:
                    first_node = new_node
                previous_node = new_node
                idx += 1
        return first_node, idx

    def find_node_by_expression(self, node_expression):
        ptr = self.__root
        for ch in node_expression[:-1]:
            if ch == "(":
                ptr = self.__memory.get_node_down(ptr)
            else:
                ptr = self.__memory.get_node_next(ptr)
        return ptr, self.__memory.get_node_label(ptr)

    def __str__(self):
        result = []
        stack = Stack(self.__memory)
        stack.push(self.__root)
        reached_end = False
        while not stack.is_empty():
            top = stack.top()
            if reached_end:
                stack.pop()
                result.append(")")
                if self.__memory.get_node_next(top) is not None:
                    reached_end = False
                    stack.push(self.__memory.get_node_next(top))
                continue
            if self.__memory.get_node_down(top) is None:
                result.append(self.__memory.get_node_label(top))
                stack.pop()
                if self.__memory.get_node_next(top) is None:
                    reached_end = True
                else:
                    stack.push(self.__memory.get_node_next(top))
            else:
                result.append("(")
                stack.push(self.__memory.get_node_down(top))
        return "".join(result)
