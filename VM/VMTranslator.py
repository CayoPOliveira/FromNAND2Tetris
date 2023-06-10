import sys
import argparse

class CodeWriter:
  """
  Generates assembly code from the parsed VM command
  """
  def __init__(self, filename : str):
    """
    Opens the output file/stream and gets ready to write into it.
    @args
      str: output_filename
    """
    self.filename = filename
    self.output = open(filename, "w")
    self.Count=0

  def __write(self, com : str):
    self.output.write(com.replace(' ', ''))

  def writeArithmetic(self, command : str):
    """
    Writes to the output file the assembly code
    that implements the given arithmetic command.
    @args
      str: command_type
    """
    Acommands = {
      "add": "@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              M=D+M\n",

      "sub": "@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              M=M-D\n",

      "neg": "@SP\n\
              A=M-1\n\
              M=-M\n",

      "eq" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=D-M\n\
              @NOTEQ{self.Count}\t//if != 0 (FALSE) -> Jump To Not Equal\n\
              D;JNE\n\
                @SP\t//if == 0 (TRUE) -> M[*SP-1]=!M[*SP-1] Fix To True\n\
                A=M-1\n\
                M=-1\n\
                @ENDEQ{self.Count}\n\
                0;JMP\n\
              (NOTEQ{self.Count})\n\
                @SP\n\
                A=M-1\n\
                M=0\n\
              (ENDEQ{self.Count})\n",

      "gt" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=M-D\n\
              @ISGT{self.Count}\t//if > 0  _ok_ (TRUE > 0)\n\
              D;JGT\n\
                @SP\t//else _M[*SP - 1] = 0_ (FALSE <= 0)\n\
                A=M-1\n\
                M=0\n\
                @ENDGT{self.Count}\n\
                0;JMP\n\
              (ISGT{self.Count})\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              (ENDGT{self.Count})\n",

      "lt" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=M-D\n\
              @ISLT{self.Count}\t//if < 0  _ok_ (TRUE <= 0)\n\
              D;JLT\n\
                @SP\t//else _M[*SP - 1] = 0_ (FALSE > 0)\n\
                A=M-1\n\
                M=0\n\
                @ENDLT{self.Count}\n\
                0;JMP\n\
              (ISLT{self.Count})\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              (ENDLT{self.Count})\n",

      "and": f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=D&M\n\
              @ENDAND{self.Count}\n\
                D;JEQ\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              (ENDAND{self.Count})\n",

      "or" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=D|M\n\
              @ENDOR{self.Count}\n\
                D;JEQ\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              (ENDOR{self.Count})\n",

      "not": "@SP\n\
              A=M-1\n\
              M=!M\n"
    }
    if command in Acommands:
      self.__write(f"//{command}\n{Acommands[command]}")
      self.Count+=1

  def writePushPop(self, command : str, segment : str, index : int):
    """
    Writes the output file the assembly code that implements
    the given command, where command is either C_PUSH or C_POP.
    @args
      str: command_type
      str: segment
      int: index
    """
    mapping = {
      "local": "LCL",
      "argment": "ARG",
      "this": "THIS",
      "that": "THAT"
    }

    self.__write(f"//{command}\t{segment}\t{index}\n")

    if segment == "pointer":
        if index == 0:
          self.writePushPop(command, "this", 0)
        elif index == 1:
          self.writePushPop(command, "that", 0)

    if command == "C_PUSH":
      # Put the value in D
      if segment in mapping:
        self.__write(f"@{index}\n\
                        D=A\n\
                        @{mapping[segment]}\n\
                        A=M+D\n\
                        D=M\n")
      elif segment=="constant":
        if index < 0:
          self.__write(f"@{-index}\n\
                         D=-A\n")
        else:
          self.__write(f"@{index}\n\
                        D=A\n")
      elif segment == "temp":
        self.__write(f"@{5+index}\n\
                       D=M\n")
      elif segment == "static":
        self.__write(f"@{filename}.{index}\n\
                       D=M\n")

      # Put RAM[*SP] = D and update *SP = *SP+1 (ALL CASES)
      self.__write("@SP\n\
                    M=M+1\n\
                    A=M-1\n\
                    M=D\n")
      return
    elif command == "C_POP":
      if segment in mapping:
        self.__write(f"@SP\n\
                      AM=M-1\n\
                      @{mapping[segment]}\n\
                      D=M\n\
                      @{index}\n\
                      D=D+A\n\
                      @R13\n\
                      M=D\n\
                      @SP\n\
                      A=M\n\
                      D=M\n\
                      @R13\n\
                      A=M\n\
                      M=D\n")
      elif segment == "temp":
        self.__write(f"@SP\n\
                      AM=M-1\n\
                      D=M\n\
                      @{5+index}\n\
                      M=D\n")
      elif segment == "static":
        self.__write(f"@SP\n\
                      AM=M-1\n\
                      D=M\n\
                      @{self.filename}.{index}\n\
                      M=D\n")
      return
    sys.exit(f"CodeWriter.writePushPop was called by {command}!\nThis function only accepts 'push' and 'pop' commands! Aborting...")

  def Close(self):
    """
    Closes the output file
    """
    self.output.close()

class Parser:
  """
  - Handles the parsing of a single .vm file
  - Reads a VM command, parses the command into its lexical
  components, and provides convenient access to these components
  - Ignores all whit space and comments
  """

  def __init__(self, filename : str):
    """
    Opens the input file/stream and gets ready to parse it
    @args
      str: input_filename
    """
    if not filename.endswith(".vm"):
      filename+=".vm"
    with open(filename, "r") as f:
      self.input = [l.split("//")[0].replace("\n", "")
                 for l in f.readlines() if l.strip() and not l.startswith("//")]
    self.seek = 0
    self.current_command = None

  def hasMoreCommands(self):
    """
    Are there more commands in the input?
    @return
      boolean: Say if there is more commands
    """
    return self.seek < len(self.input)

  def advance(self):
    """
    Reads the next command from the input and makes it the currente command.
    Should be called only if hasMoreCommands() is true.
    Initially there is no currente command.
    """
    if(self.hasMoreCommands()):
      self.current_command = self.input[self.seek]
      self.seek += 1

  def commandType(self):
    """
    Returns a constant representanting the type of the current command.
    C_ARITHMETIC is returned for al the arithmetic/logical commands.
    @return
      str: Command type in string format
    """
    head = self.current_command.split(" ")[0]
    if head in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
      return "C_ARITHMETIC"
    if head == "if-goto":
      return "C_IF"
    if head in ['pop', 'push', 'label', 'goto', 'function', 'call', 'return']:
      return f"C_{head.upper()}"
    sys.exit(f"Command '{head}' is a type unknow! Aborting...")

  def arg1(self):
    """
    Returns the first argument of the current command.
    In the case of C_ARITHMETIC, the command itself(add, sub, etc.)
      is returned.
    Should not be called if the currente command is C_RETURN
    @return
      str: The first argumment of the command or itself
    """
    ct = self.commandType()
    if ct == "C_RETURN":
      sys.exit("Command type C_RETURN is calling parser.arg1()! Aborting...")
    if ct == "C_ARITHMETIC":
      return self.current_command
    return self.current_command.split(" ")[1].split(" ")[0]

  def arg2(self):
    """
    Returns the second argument of the currente command.
    Should be called only if the current command is
      C_PUSH, C_POP, C_FUNCTION or C_CALL.
    @return
      int: The second argument of the currente command.
    """
    ct = self.commandType()
    if ct not in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
      sys.exit(f"Command type {ct} is calling parser.arg2()! Aborting...")
    return int(self.current_command.split(" ")[2])


class Main():
  def __init__(self):
    args = self.argParser()

    # initiate parser and codewriter
    self.vm_parser = Parser(args.file)
    self.vm_cw = CodeWriter(args.out)

    # iterates commands
    while self.vm_parser.hasMoreCommands():
      self.vm_parser.advance()
      ctype = self.vm_parser.commandType()
      if (ctype == "C_ARITHMETIC"):
        self.vm_cw.writeArithmetic(self.vm_parser.arg1())
      elif (ctype == "C_POP" or ctype == "C_PUSH"):
        self.vm_cw.writePushPop(ctype, self.vm_parser.arg1(), self.vm_parser.arg2())

    #close output file
    self.vm_cw.Close()

  def argParser(self):
    #PARSER ARGS
    parser = argparse.ArgumentParser(description='Process command line arguments')

    # Define the arguments
    parser.add_argument('-f', '--file', dest='file', type=str, help='File path')
    parser.add_argument('-o', '--output', dest='out', type=str, help='Output file')

    # Set default values for the arguments
    parser.set_defaults(file="", out="")

    # Parse the arguments
    args = parser.parse_args()

    # Not especified output name
    if args.out == "":
      args.out = args.file
    if not args.out.endswith(".vm"):
      sys.exit("The current file is not .vm! Aborting...")
    args.out = args.out.replace(".vm", ".asm")

    # Return args structure
    return args

if __name__ == "__main__":
  main = Main()



