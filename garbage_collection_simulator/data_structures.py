class NotEnoughMemoryCellsError(MemoryError):
    pass


class Memory:
    def __init__(self, size):
        """
        A memory simulator instance is created with given number of cells.
        Each cell occupies 4 consequent indices with names: tag, label, next, down.
        Thus cells array have 4 * size indices.
        """
        self.__cells = [None] * (size * 4)
        self.__size = size
        self.__avail_list_head = 0
        self.__init_avail_list()

    def __init_avail_list(self):
        for i in range(0, 4 * (self.__size - 1), 4):
            self.set_cell_next(i, i + 4)

    def allocate_cell(self):
        if self.__avail_list_head is None:
            raise NotEnoughMemoryCellsError("Can not allocate cells due to insufficient memory space.")
        next_avail_cell = self.get_cell_next(self.__avail_list_head)
        allocated_cell = self.__avail_list_head
        self.set_cell_next(allocated_cell, None)
        self.__avail_list_head = next_avail_cell
        return allocated_cell

    def free_cell(self, cell):
        self.set_cell_next(cell, self.__avail_list_head)
        self.__avail_list_head = cell

    def set_cell_next(self, cell, new_next):
        self.__cells[cell + 2] = new_next

    def set_cell_down(self, cell, new_down):
        self.__cells[cell + 3] = new_down

    def set_cell_label(self, cell, new_label):
        self.__cells[cell + 1] = new_label

    def get_cell_label(self, cell):
        return self.__cells[cell + 1]

    def get_cell_down(self, cell):
        return self.__cells[cell + 3]

    def get_cell_next(self, cell):
        return self.__cells[cell + 2]

    def __get_cell_tag(self, cell):
        return self.__cells[cell]

    def __set_cell_tag(self, cell, new_tag):
        self.__cells[cell] = new_tag

    def status(self):
        return [
            (
                self.__cells[4 * i],  # tag
                self.__cells[4 * i + 1],  # label
                self.__cells[4 * i + 2],  # next
                self.__cells[4 * i + 3]  # down
            ) for i in range(self.__size)
        ]

    def __str__(self):
        return "\n".join(
            [
                f"cell #{i + 1} : "
                f"(tag = {self.__cells[4 * i]}, "
                f"label = {self.__cells[4 * i + 1]}, "
                f"next = {self.__cells[4 * i + 2]}, "
                f"down = {self.__cells[4 * i + 3]})" for i in range(self.__size)
            ]
        )

    def garbage_collect(self, *lists_roots):
        pass


class GeneralList:
    def __init__(self, memory, root):
        self.__memory = memory
        self.__root = root

    @classmethod
    def convert_expression_to_general_list(cls, memory: Memory, expression: str):
        return cls(
            memory,
            cls.__convert_expression_to_general_list(memory, list(expression), 0)
        )

    @staticmethod
    def __convert_expression_to_general_list(memory: Memory, expression: list, idx):
        pass


    def find_node_by_expression(self, node_expression):
        pass

    def __str__(self):
        pass

