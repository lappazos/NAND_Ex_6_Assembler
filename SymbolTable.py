pre_def_symbols = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6,
                   'R7': 7, 'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12,
                   'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384, 'KBD': 24576,
                   'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}

FIRST_INDEX = 16


class SymDict:
    """
    class that represents the labels and variables
    """

    def __init__(self):
        """
        init the dict
        """
        self._syDict = pre_def_symbols  # pre defined symbols
        self._index = FIRST_INDEX  # start index for variables

    def add_label(self, name, line):
        """
        add a new label
        :param name: the name of the label
        :param line: the line number where the label is
        :return: the  line of the label
        """
        self._syDict[name] = line

    def get_add_variable(self, variable):
        """
        get or add variable
        :param variable: the variable name
        :return: variable address
        """
        if variable not in self._syDict:
            self._syDict[variable] = self._index
            self._index += 1  # new location in memory
        return self._syDict[variable]
