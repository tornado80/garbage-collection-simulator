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
        for i in range(self.__size - 1):
            self.set_node_next(i * 4, i * 4 + 4)

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

    def garbage_collect(self, *lists_roots):
        print("Starting Garbage Collection")
        # mark all as garbage
        for i in range(self.__size):
            self.__set_node_tag(i * 4, False)
        # mark accessible nodes
        for list_root in lists_roots:
            self.__traverse_list_and_mark_tags(list_root)
        # sweep garbage nodes
        for i in range(self.__size):
            if not self.__get_node_tag(i * 4):
                self.free_node(i * 4)
        print("Finished Garbage Collection")

    def __traverse_list_and_mark_tags(self, list_root):
        cur = list_root.root
        prev = None
        moving_backward = False
        ladder_used = False
        print("list traversed: ", end="")
        while True:
            if cur is None:
                prev, cur = cur, prev
                moving_backward = True
            if not moving_backward:
                self.__set_node_tag(cur, True)
                if self.get_node_down(cur) is not None and self.get_node_down(self.get_node_down(cur)) != cur:
                    print("(", end="")
                    if not ladder_used:
                        # Store cur next node in temp to set in label.
                        # Useful when moving backward. This is only used when not in ladder mode
                        temp = self.get_node_next(cur)
                        # Reverse pointer between cur and prev
                        self.set_node_next(cur, prev)                        
                        # Set this label to find the right next node after cur when moving backward.
                        # This is only used when not in ladder mode
                        self.set_node_label(cur, temp)
                    # Get the down node
                    down_node = self.get_node_down(cur)
                    if self.get_node_down(down_node) is not None:
                        # Since these nodes are pointers to other lists, we can play with these nodes' labels.
                        # When moving backward we use this label to access parent node
                        self.set_node_label(down_node, cur)
                        # Nodes which are placed on top of each other are ladder.
                        # When moving with down pointer, we have to set ladder used.
                        ladder_used = True
                    else:
                        # This is a node with no child so we can't play with label.
                        # But its down pointer is None. So by setting this to the parent node we have a loop.
                        # We can detect this loop when moving backwards. So we can identify this node.
                        self.set_node_down(down_node, cur)
                        # When moving with down pointer, we have to set ladder used.
                        # But here the node below us does not have a child
                        ladder_used = False
                    cur = down_node
                    prev = None
                else:
                    # Simple moving next with reversing pointers
                    print(self.get_node_label(cur), end="")
                    temp = self.get_node_next(cur)
                    self.set_node_next(cur, prev)
                    prev = cur
                    cur = temp
            else:
                # Simple moving backward (actually next)
                temp = self.get_node_next(cur)
                self.set_node_next(cur, prev)
                prev = cur
                cur = temp
                # Check if we have finished moving backward
                if cur is None:
                    print(")", end="")
                    moving_backward = False
                    # Now check if we have no child using that loop trick
                    if self.get_node_down(self.get_node_down(prev)) == prev:
                        # we have no child so we get father from down field
                        cur = self.get_node_down(prev)
                        self.set_node_down(prev, None)
                    else:
                        # we have child so we get the father from label
                        cur = self.get_node_label(prev)
                    # Find next node from label
                    if cur == list_root.root:
                        break
                    if self.get_node_label(cur) is None:  # top ladder node
                        temp = self.get_node_label(cur)                      
                        prev = cur
                        cur = temp                        
                    elif self.get_node_down(self.get_node_label(cur)) != cur:  # top ladder node
                        temp = self.get_node_label(cur)
                        prev = cur
                        cur = temp                                               
                    else:  # we need to move next
                        temp = self.get_node_next(cur)
                        prev = cur
                        cur = temp
                        self.set_node_next(prev, None)
        print()


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
        self.root = root

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
        ptr = self.root
        for ch in node_expression[:-1]:
            if ch == "(":
                ptr = self.__memory.get_node_down(ptr)
            else:
                ptr = self.__memory.get_node_next(ptr)
        return ptr, self.__memory.get_node_label(ptr)

    def __str__(self):
        result = []
        stack = Stack(self.__memory)
        stack.push(self.root)
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
                label = self.__memory.get_node_label(top)
                result.append("" if label is None else label)
                stack.pop()
                if self.__memory.get_node_next(top) is None:
                    reached_end = True
                else:
                    stack.push(self.__memory.get_node_next(top))
            else:
                result.append("(")
                stack.push(self.__memory.get_node_down(top))
        return "".join(result)
