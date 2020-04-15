import re
import SymbolTable

BIN_FORMAT = '016b'

END = -1

START = 0

DOT_SEPERATOR = ';'

EQUALS = '='

C_INSTRUCTION_OP_CODE = '1'

SYMBOL_MARKER = '@'

CLOSE_LABEL = ')'

OPEN_LABEL = '('

EMPTY_STRING = ""

commentPat = re.compile('^[^ /]*')

Comp = {
    "0": "110101010",
    "1": "110111111",
    "-1": "110111010",
    "-A": "110110011",
    "D+1": "110011111",
    "A+1": "110110111",
    "D-1": "110001110",
    "A-1": "110110010",
    "D": "110001100",
    "A": "110110000",
    "!D": "110001101",
    "!A": "110110001",
    "A-D": "110000111",
    "D&A": "110000000",
    "D|A": "110010101",
    "M": "111110000",
    "!M": "111110001",
    "-M": "111110011",
    "M+1": "111110111",
    "-D": "110001111",
    "D+A": "110000010",
    "D-A": "110010011",
    "M-1": "111110010",
    "D+M": "111000010",
    "D-M": "111010011",
    "M-D": "111000111",
    "D&M": "111000000",
    "D|M": "111010101",
    "M<<": "011100000",
    "M>>": "011000000",
    "D<<": "010110000",
    "D>>": "010010000",
    "A<<": "010100000",
    "A>>": "010000000",
}

Dest = {
    None: "000",
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

Jump = {
    None: "000",
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}


def main_loop(lines, symbols):
    """
    perform the program second pass, for A and C instruction
    :param lines: assembly lines array without labels, whitespaces
    :param symbols: symbols object
    :return: binary code array
    """
    code = []
    for line in lines:
        if line.startswith(SYMBOL_MARKER):  # A instructions
            line = line.strip(SYMBOL_MARKER)
            if line.isdigit():
                code.append(format(int(line), BIN_FORMAT))
            else:
                address = symbols.get_add_variable(line)
                code.append(format(address, BIN_FORMAT))
        else:  # it a C instructions
            if EQUALS in line:
                dest, right = line.split(EQUALS)
                if DOT_SEPERATOR in right:
                    comp, jmp = right.split(DOT_SEPERATOR)
                else:
                    comp = right
                    jmp = None
            else:
                comp, jmp = line.split(DOT_SEPERATOR)
                dest = None
            code.append(C_INSTRUCTION_OP_CODE + Comp[comp] + Dest[dest] + Jump[jmp])
    return code


def clean_lines(file):
    """
    get an array of lines and clear the whitespaces and comments
    :param file: assembly lines array
    :return: cleaned assembly lines array
    """
    lines = []
    for line in file:
        # check if start with a comment
        line = re.sub(r'\s+', EMPTY_STRING, line)
        match = commentPat.match(line)
        line = match.group(0)
        if line == EMPTY_STRING:
            continue
        lines.append(line)
    return lines


def parse_labels(file):
    """
    extract and remove labels from assembly lines
    :param file: cleaned assembly lines
    :return: symbols object
    """
    symbols = SymbolTable.SymDict()
    line_index = 0
    lines = []
    for line in file:
        if (line[START] == OPEN_LABEL) and (line[END] == CLOSE_LABEL):
            symbols.add_label(line[1:-1], line_index)
        else:
            lines.append(line)
            line_index += 1
    return symbols, lines
