import os
import sys
import argparse

debug = False

class CodeWriter:
  """
  Generates assembly code from the parsed VM command
  """
  def __init__(self, filename : str, bootstrap = True):
    """
    Opens the output file/stream and gets ready to write into it.

    Writes the assembly instructions that effect the bootstrap code
    that starts the program's execution. This code must be placed at
    the beginning of the generated output file/stream.
    @args
      str: output_filename
    """
    self.function = ""
    self.filename = ""
    self.output = open(filename, "w")
    self.Count=0

    if bootstrap:
      self.__write("// Bootstrap code\n\
                    @256\n\
                    D=A\n\
                    @0\n\
                    M=D\n")
      self.__write("// Call Sys.init\n\
                    @Sys.init\n\
                    0;JMP\n")
      return

  def setFileName(self, filename : str):
    """
    Informs that the translation of a new VM file has started
    (called by the VMTranslator).
    @args
      str: input_filename
    """
    self.filename = filename
    self.function = f"{filename}"
    self.Count=0

  def newCommand(self):
    """
    Debug Function, just put a @12345 line.
    You can use before any command to see in CPUEmulator when a new command start,
    the output.asm has comments for this but CPUEmulator doesn't show them.
    """
    self.__write("@12345\n")

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
              @{self.filename}.NOTEQ.{self.Count}\t//if != 0 (FALSE) -> Jump To Not Equal\n\
              D;JNE\n\
                @SP\t//if == 0 (TRUE) -> M[*SP-1]=!M[*SP-1] Fix To True\n\
                A=M-1\n\
                M=-1\n\
                @{self.filename}.ENDEQ.{self.Count}\n\
                0;JMP\n\
              ({self.filename}.NOTEQ.{self.Count})\n\
                @SP\n\
                A=M-1\n\
                M=0\n\
              ({self.filename}.ENDEQ.{self.Count})\n",

      "gt" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=M-D\n\
              @{self.filename}.ISGT.{self.Count}\t//if > 0  _ok_ (TRUE > 0)\n\
              D;JGT\n\
                @SP\t//else _M[*SP - 1] = 0_ (FALSE <= 0)\n\
                A=M-1\n\
                M=0\n\
                @{self.filename}.ENDGT.{self.Count}\n\
                0;JMP\n\
              ({self.filename}.ISGT.{self.Count})\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              ({self.filename}.ENDGT.{self.Count})\n",

      "lt" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=M-D\n\
              @{self.filename}.ISLT.{self.Count}\t//if < 0  _ok_ (TRUE <= 0)\n\
              D;JLT\n\
                @SP\t//else _M[*SP - 1] = 0_ (FALSE > 0)\n\
                A=M-1\n\
                M=0\n\
                @{self.filename}.ENDLT.{self.Count}\n\
                0;JMP\n\
              ({self.filename}.ISLT.{self.Count})\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              ({self.filename}.ENDLT.{self.Count})\n",

      "and": f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=D&M\n\
              @{self.filename}.ENDAND.{self.Count}\n\
                D;JEQ\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              ({self.filename}.ENDAND.{self.Count})\n",

      "or" : f"@SP\n\
              AM=M-1\n\
              D=M\n\
              A=A-1\n\
              MD=D|M\n\
              @{self.filename}.ENDOR.{self.Count}\n\
                D;JEQ\n\
                @SP\n\
                A=M-1\n\
                M=-1\n\
              ({self.filename}.ENDOR.{self.Count})\n",

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
      "argument": "ARG",
      "this": "THIS",
      "that": "THAT"
    }

    self.__write(f"//{command}\t{segment}\t{index}\n")

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
        self.__write(f"@{self.filename}.{index}\n\
                       D=M\n")
      elif segment == "pointer":
        if index == 0: #THIS
          self.__write("@THIS\n\
                        D=M\n")
        elif index == 1: #THAT
          self.__write("@THAT\n\
                        D=M\n")


      # Put RAM[*SP] = D and update *SP = *SP+1 (ALL CASES)
      self.__write("@SP\n\
                    M=M+1\n\
                    A=M-1\n\
                    M=D\n")

      return

    elif command == "C_POP":
      if segment in mapping:
        self.__write(f"@{mapping[segment]}\n\
                      D=M\n\
                      @{index}\n\
                      D=D+A\n\
                      @R13\n\
                      M=D\n\
                      @SP\n\
                      AM=M-1\n\
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
      elif segment == "pointer":
        if index == 0: #THIS
          self.__write("@SP\n\
                        AM=M-1\n\
                        D=M\n\
                        @THIS\n\
                        M=D\n")
        elif index == 1: #THAT
          self.__write("@SP\n\
                        AM=M-1\n\
                        D=M\n\
                        @THAT\n\
                        M=D\n")

      return
    sys.exit(f"CodeWriter.writePushPop was called by {command}!\nThis function only accepts 'push' and 'pop' commands! Aborting...")

  def writeLabel(self, label : str):
    """
    Writes assembly code that effects the label command
    """
    self.__write(f"// Label\t{label}\n")
    self.__write(f"({self.function}${label})\n")

  def writeGoto(self, label : str):
    """
    Writes assembly code that effects the goto command
    """
    self.__write(f"// Goto\t{label}\n")
    self.__write(f"@{self.function}${label}\n\
                  0;JMP\n")

  def writeIf(self, label : str):
    """
    Writes assembly code that effects the if-goto command
    """
    self.__write(f"// If-goto\t{label}\n")
    self.__write(f"@SP\n\
                  AM=M-1\n\
                  D=M\n\
                  @{self.function}${label}\n\
                  D;JNE\n")

  def writeFunction(self, functionName : str, nVars: int):
    """
    Writes assembly code that effects the function command
    """
    self.function = functionName

    self.__write(f"// Function\t{functionName}\twith\t{nVars}\tvars\n")

    # Inject the entry point label to function
    self.__write(f"({functionName})\n")
    # Initialize local segment
    for i in range(nVars):
      self.__write("@SP\n\
                    AM=M+1\n\
                    A=A-1\n\
                    M=0\n")

  def writeCall(self, functionName : str, nArgs : int):
    """
    Writes assembly code that effects the call command
    """
    self.__write(f"// Call\tfunction\t{self.filename}.{functionName}\twith\t{nArgs}\tvars\n")

    # Save return addres, save context, reposition of ARG & LCL, go to function
        # push retAddrLabel     // Generates and pushes this label
        # push LCL // Saves the caller’s LCL
        # push ARG // Saves the caller’s ARG
        # push THIS // Saves the caller’s THIS
        # push THAT // Saves the caller’s THAT
        # ARG = SP – 5 – nArgs // Repositions ARG
        # LCL = SP // Repositions LCL
        # goto functionName // Transfers control to the callee
        # (retAddrLabel) // Injects this label into the code
    self.__write(f"//Push\tretAddrLabel\n\
                  @{functionName}$ret.{self.Count}\n\
                  D=A\n\
                  @SP\n\
                  AM=M+1\n\
                  A=A-1\n\
                  M=D\n\
                  // Push LCL\n\
                  @LCL\n\
                  D=M\n\
                  @SP\n\
                  AM=M+1\n\
                  A=A-1\n\
                  M=D\n\
                  // Push ARG\n\
                  @ARG\n\
                  D=M\n\
                  @SP\n\
                  AM=M+1\n\
                  A=A-1\n\
                  M=D\n\
                  // Push THIS\n\
                  @THIS\n\
                  D=M\n\
                  @SP\n\
                  AM=M+1\n\
                  A=A-1\n\
                  M=D\n\
                  // Push THAT\n\
                  @THAT\n\
                  D=M\n\
                  @SP\n\
                  AM=M+1\n\
                  A=A-1\n\
                  M=D\n\
                  // Reposition ARG (ARG = RAM[SP] - 5 - nArgs)\n\
                  @SP\n\
                  D=M\n\
                  @5\n\
                  D=D-A\n\
                  @{nArgs}\n\
                  D=D-A\n\
                  @ARG\n\
                  M=D\n\
                  // Reposition LCL (LCL = RAM[SP])\n\
                  @SP\n\
                  D=M\n\
                  @LCL\n\
                  M=D\n\
                  // Goto Function {functionName}\n\
                  @{functionName}\n\
                  0;JMP\n\
                  // Inject the return Label\n\
                  ({functionName}$ret.{self.Count})\n")
    self.Count+=1 # Increment the function counter

  def writeReturn(self):
    """
    Writes assembly code that effects the return command
    """
    self.__write(f"//Returning\n")

    # Replace arguments with return value from function, recycle memory, reinstate the pointers and jump to return address
        # endFrame = LCL // gets the address at the frame’s end
        # retAddr = *(endFrame – 5) // gets the return address
        # *ARG = pop() // puts the return value for the caller
        # SP = ARG + 1 // repositions SP
        # THAT = *(endFrame – 1) // restores THAT
        # THIS = *(endFrame – 2) // restores THIS
        # ARG = *(endFrame – 3) // restores ARG
        # LCL = *(endFrame – 4) // restores LCL
        # goto retAddr // jumps to the return address
    self.__write(f"// endFrame(RAM[R13]) = RAM[LCL]\n\
                  @LCL\n\
                  D=M\n\
                  @R13\n\
                  M=D\n\
                  // retAddr(RAM[R14]) = *(endFrame - 5)\n\
                  @5\n\
                  A=D-A\n\
                  D=M\n\
                  @R14\n\
                  M=D\n\
                  // Pop\tretValue\tin\tRAM[ARG]\n\
                  @SP\n\
                  AM=M-1\n\
                  D=M\n\
                  @ARG\n\
                  A=M\n\
                  M=D\n\
                  // Recycle\tmemory\tRAM[SP]=RAM[ARG]+1\n\
                  D=A+1\n\
                  @SP\n\
                  M=D\n\
                  // Restore \tTHAT\n\
                  @R13\n\
                  AM=M-1\n\
                  D=M\n\
                  @THAT\n\
                  M=D\n\
                  // Restore \tTHIS\n\
                  @R13\n\
                  AM=M-1\n\
                  D=M\n\
                  @THIS\n\
                  M=D\n\
                  // Restore \tARG\n\
                  @R13\n\
                  AM=M-1\n\
                  D=M\n\
                  @ARG\n\
                  M=D\n\
                  // Restore \tLCL\n\
                  @R13\n\
                  AM=M-1\n\
                  D=M\n\
                  @LCL\n\
                  M=D\n\
                  // Jump\tto\tretAddr\n\
                  @R14\n\
                  A=M\n\
                  0;JMP\n")


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
      self.input = [l.split("//")[0].replace("\n", "").strip(" ").strip("\t")
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

if __name__ == "__main__":
  #PARSER ARGS
  argParser = argparse.ArgumentParser(description='Process command line arguments')

  # Define the arguments
  argParser.add_argument('-i', '--input', dest='input', type=str, help='Input file.vm or directory with .vm files')
  argParser.add_argument('-o', '--output', dest='out', type=str, help='Output file.asm')

  # Set default values for the arguments
  argParser.set_defaults(input="", out="")

  # Parse the arguments
  args = argParser.parse_args()

  # Not especified output name
  if args.out == "":
    args.out = args.input
    # Input is a directory
    if args.out.endswith("/"):
      args.out += args.out.split("/")[-2]
    # Input is a .vm
    elif args.out.endswith(".vm"):
      args.out = args.out.replace(".vm", "")

  # Output must be a .asm file
  if not args.out.endswith(".asm"):
    args.out += ".asm"

  print(f"Input: {args.input}")
  print(f"Output: {args.out}")

  # VMTRANSLATER
  # initiate codewriter
  VMCodeWriter = CodeWriter(args.out)

  # If the input is a .vm file
  if args.input.endswith(".vm"):
    # initiate Parser
    VMParser = Parser(args.input)
    # set filename
    VMCodeWriter.setFileName(args.input.split("/")[-2].replace(".asm", ""))
    # iterates commands
    while VMParser.hasMoreCommands():
      VMParser.advance()
      if debug: VMCodeWriter.newCommand()
      ctype = VMParser.commandType()
      if (ctype == "C_ARITHMETIC"):
        VMCodeWriter.writeArithmetic(VMParser.arg1())
      elif (ctype == "C_POP" or ctype == "C_PUSH"):
        VMCodeWriter.writePushPop(ctype, VMParser.arg1(), VMParser.arg2())
      elif (ctype == "C_LABEL"):
        VMCodeWriter.writeLabel(VMParser.arg1())
      elif (ctype == "C_GOTO"):
        VMCodeWriter.writeGoto(VMParser.arg1())
      elif (ctype == "C_IF"):
        VMCodeWriter.writeIf(VMParser.arg1())
      elif (ctype == "C_FUNCTION"):
        VMCodeWriter.writeFunction(VMParser.arg1(), VMParser.arg2())
      elif (ctype == "C_CALL"):
        VMCodeWriter.writeCall(VMParser.arg1(), VMParser.arg2())
      elif (ctype == "C_RETURN"):
        VMCodeWriter.writeReturn()

  else:
    # Get a list of .vm files in the directory
    vm_files = [file.replace(".vm", "") for file in os.listdir(args.input) if file.endswith(".vm")]
    # Process each .vm file
    for file in vm_files:
      file_path = os.path.join(args.input, file)
      # initiate Parser
      VMParser = Parser(file_path)
      # set filename
      VMCodeWriter.setFileName(file)
      # iterates commands
      while VMParser.hasMoreCommands():
        VMParser.advance()
        if debug: VMCodeWriter.newCommand()
        ctype = VMParser.commandType()
        if (ctype == "C_ARITHMETIC"):
          VMCodeWriter.writeArithmetic(VMParser.arg1())
        elif (ctype == "C_POP" or ctype == "C_PUSH"):
          VMCodeWriter.writePushPop(ctype, VMParser.arg1(), VMParser.arg2())
        elif (ctype == "C_LABEL"):
          VMCodeWriter.writeLabel(VMParser.arg1())
        elif (ctype == "C_GOTO"):
          VMCodeWriter.writeGoto(VMParser.arg1())
        elif (ctype == "C_IF"):
          VMCodeWriter.writeIf(VMParser.arg1())
        elif (ctype == "C_FUNCTION"):
          VMCodeWriter.writeFunction(VMParser.arg1(), VMParser.arg2())
        elif (ctype == "C_CALL"):
          VMCodeWriter.writeCall(VMParser.arg1(), VMParser.arg2())
        elif (ctype == "C_RETURN"):
          VMCodeWriter.writeReturn()

  # close output file
  VMCodeWriter.Close()


