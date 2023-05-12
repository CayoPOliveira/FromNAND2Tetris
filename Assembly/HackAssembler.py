import re
import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='Process command line arguments')

    # Define the arguments
    parser.add_argument('-hack', dest='hack', action='store_true',
                        help='Generate program in binary commands with .hack extension')
    parser.add_argument('-hex', dest='hex', action='store_true',
                        help='Generate program in hexadecimal commands with .hex extension')
    parser.add_argument('-f', '--file', dest='file',
                        type=str, help='File path')
    parser.add_argument('-o', '--output', dest='out',
                        type=str, help='Output file')

    # Set default values for the arguments
    parser.set_defaults(hack=False, hex=False, file="", out="")

    # Parse the arguments
    args = parser.parse_args()

    # Not especified output name
    if args.out == "":
        args.out = args.file

    return args


def tdest(dest):
    ans = 0
    if 'M' in dest:
        ans += 1
    if 'D' in dest:
        ans += 2
    if 'A' in dest:
        ans += 4
    return f"{ans:03b}"


def tjump(jump):
    return {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }[jump]


def tcomp(comp):
    if 'M' in comp:
        resp = "1"
    else:
        resp = "0"
    return resp + ({
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "D": "001100",
        "A": "110000",
        "M": "110000",
        "!D": "001101",
        "!A": "110001",
        "!M": "110001",
        "-D": "001111",
        "-A": "110011",
        "-M": "110011",
        "D+1": "011111",
        "A+1": "110111",
        "M+1": "110111",
        "D-1": "001110",
        "A-1": "110010",
        "M-1": "110010",
        "D+A": "000010",
        "D+M": "000010",
        "D-A": "010011",
        "D-M": "010011",
        "A-D": "000111",
        "M-D": "000111",
        "D&A": "000000",
        "D&M": "000000",
        "D|A": "010101",
        "D|M": "010101"
    }[comp])

def handle_symbols(lines):
    # predefined symbol
    symbols = {
        "@R0": "@0",
        "@R1": "@1",
        "@R2": "@2",
        "@R3": "@3",
        "@R4": "@4",
        "@R5": "@5",
        "@R6": "@6",
        "@R7": "@7",
        "@R8": "@8",
        "@R9": "@9",
        "@R10": "@10",
        "@R11": "@11",
        "@R12": "@12",
        "@R13": "@13",
        "@R14": "@14",
        "@R15": "@15",
        "@SCREEN": "@16384",
        "@KBD": "@24576",
        "@SP": "@0",
        "@LCL": "@1",
        "@ARG": "@2",
        "@THIS": "@3",
        "@THAT": "@4"
    }

    # Label symbols
    lineNumber = 0
    while lineNumber < len(lines):
        if lines[lineNumber].startswith("(") and lines[lineNumber].endswith(")"):
            l = lines.pop(lineNumber)
            symbols["@" + l.split("(")[1].split(")")[0]] = f"@{lineNumber}"
            continue # No increment
        lineNumber+=1

    variableValue = 16
    noSymbolLines = []
    for l in lines:
        if l in symbols:
            noSymbolLines.append(symbols[l])
        elif l.startswith("@") and l[1:].isalpha():  # É uma variável nova que ainda não está em symbols
            symbols[l] = f"@{variableValue}"
            variableValue+=1
            noSymbolLines.append(symbols[l])
        else:
            noSymbolLines.append(l)

    # print(symbols)
    return noSymbolLines



def assembly(args):
    # Remove white spaces and comments
    with open(args.file, 'r') as input:
        lines = [l.split("//")[0].strip()
                 for l in input.readlines() if l.strip() and not l.startswith("//")]

    #handle symbols
    lines = handle_symbols(lines)

    codasm = []
    for l in lines:
        # A instruction @n (15bits > 0)
        if l.startswith("@"):
            n = int(l[1:]) % 2**16
            codasm.append(f"0{n:015b}")
        # C instruction 111accccccdddjjj -> dest=comp:jump
        else:
            ddd, aux = l.split("=") if "=" in l else ("", l)
            acccccc, jjj = aux.split(";") if ";" in aux else (aux, "")
            codasm.append(f"111{tcomp(acccccc)}{tdest(ddd)}{tjump(jjj)}")

    with open(args.out+".bin", 'w') as out:
        flag = 0
        for asm in codasm:
            if flag: out.write("\n")
            flag = 1
            out.write(asm)
    if(args.hack):
        with open(args.out+".hack", 'w') as out:
            flag = 0
            for asm in codasm:
                if flag: out.write("\n")
                flag = 1
                out.write(asm)
    if(args.hex):
        with open(args.out+".hex", 'w') as out:
            flag = 0
            for asm in codasm:
                if flag: out.write("\n")
                flag = 1
                out.write(hex(int(asm, 2))[2:].zfill(4))


if __name__ == "__main__":
    args = get_args()
    if args.file.endswith(".asm"):
        # O arquivo é um código assembly, podemos processá-lo
        if args.file == args.out:
            args.out = args.out.split(".asm")[0]
        assembly(args)
    else:
        # O arquivo não é um código assembly, não podemos processá-lo
        print('O arquivo não é um código assembly.')
