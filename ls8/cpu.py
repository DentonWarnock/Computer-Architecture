"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 244 # stack pointer, set to F4 on initialization
        self.pc = 0 # Program Counter, address of the currently executing instruction
        self.running = True
        self.instruction = {
            "HLT" : 0b00000001,
            "LDI" : 0b10000010,
            "PRN" : 0b01000111,
            'MUL' : 0b10100010,
            'SUB' : 0b10100011,
            'PUSH': 0b01000101,
            'POP' : 0b01000110,
        }

    def load(self):
        """Load a program into memory."""

        address = 0
        
        if len(sys.argv) != 2:
            print("no file given to run")
            sys.exit()
            
        try:
            with open(sys.argv[1]) as file:
                program = file.readlines()
                
                for line in program:    
                    code = line[:line.find("#")]
                    if code == "":
                        continue
                    # print(code)
                    num = int(code, 2)
                    self.ram_write(num, address)
                    address += 1
        except FileNotFoundError:
            print(f"could not find file {sys.argv[1]}")
            
    def ram_read(self, op):
        return self.ram[op]      
        

    def ram_write(self, value, op):
        self.ram[op] = value     
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
        
            # Instruction Register, contains a copy of the currently executing instruction
            IR = self.ram[self.pc]
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            num_operands = IR >> 6
            self.pc += 1 + num_operands
            
            # load data into register
            if IR == self.instruction['LDI']:
                self.reg[operand_a] = operand_b
            
            # print data from register
            elif IR == self.instruction['PRN']:
                print(self.reg[operand_a])
                
            elif IR == self.instruction['MUL']:
                self.alu('MUL', operand_a, operand_b)
                
            elif IR == self.instruction['SUB']:
                self.alu('SUB', operand_a, operand_b)
                
            elif IR == self.instruction['POP']:
                 # copy the value from the address pointed to by SP to the given register
                self.reg[operand_a] = self.ram_read(self.sp)
                # increment the SP
                self.sp += 1
                
            elif IR == self.instruction['PUSH']:
                self.sp -= 1
                # copy the value in the given register to the address pointed to by SP
                self.ram_write(self.reg[operand_a], self.sp)
           
            
            # Halt operation or stop loop
            elif IR == self.instruction['HLT']:
                self.running = False
                
                
            
          
                
