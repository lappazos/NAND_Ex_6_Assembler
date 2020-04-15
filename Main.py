import sys
import os
import CodeParser

FILE_LOCATION = 1

NEW_LINE = "\n"

HACK = ".hack"

ASM = ".asm"


def parse_assembly_code(assembly_code):
    """
    main assemble function
    :param assembly_code: an array of assembly lines
    :return: an array of binary lines
    """
    clean_code = CodeParser.clean_lines(assembly_code)
    symbols, label_less_code = CodeParser.parse_labels(clean_code)
    code = CodeParser.main_loop(label_less_code, symbols)
    return code


def assemble_files(file_path):
    """
    handle files side
    :param file_path: the path of the asm files
    """
    if os.path.isdir(file_path):
        for file in os.listdir(file_path):
            if file.endswith(ASM):
                handle_dir_file(file, file_path)
    elif os.path.isfile(file_path):
        if file_path.endswith(ASM):
            handle_single_file(file_path)


def handle_single_file(file_path):
    """
    handle single files
    :param file_path: file path
    """
    f = open(file_path, 'r')
    assembly_code = f.readlines()
    f.close()
    binary = parse_assembly_code(assembly_code)
    hack_file = open(file_path.strip(ASM) + HACK, "w")
    for line in binary:
        hack_file.write(line + NEW_LINE)
    hack_file.close()


def handle_dir_file(file, files_path):
    """
    handle files originated from dir
    :param file: file name
    :param files_path: directory
    :return:
    """
    f = open(os.path.join(filePath, file), 'r')
    assembly_code = f.readlines()
    f.close()
    binary = parse_assembly_code(assembly_code)
    hack_file_name = os.path.join(files_path, file.strip(ASM) + HACK)
    hack_file = open(hack_file_name, "w")
    for line in binary:
        hack_file.write(line + NEW_LINE)
    hack_file.close()


if __name__ == '__main__':
    filePath = sys.argv[FILE_LOCATION]
    assemble_files(filePath)
