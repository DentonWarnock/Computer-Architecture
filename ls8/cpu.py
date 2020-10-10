"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
POP = 0b01000110
PUSH = 0b01000101
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100011
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 244 # stack pointer, set to F4 on initialization
        self.reg[7] = self.sp
        self.fl = 0b00000000 # Flags Register - 00000LGE
        self.pc = 0 # Program Counter, address of the currently executing instruction
        self.running = True
        self.bt = {
            HLT : self.hlt,
            LDI : self.ldi,
            PRN : self.prn,
            PUSH: self.push,
            POP : self.pop,
            CALL : self.call,
            RET: self.ret,
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

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
            
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
            
        elif op == CMP:
            # compare the values in reg_a and reg_b - set flags `00000LGE`
            # if reg_a less than reg_b set L flag to 1
            if self.reg[rega] < self.reg[reg_b]:
                self.fl = 0b00000100
            # if reg_a greater than reg_b set G flag to 1
            elif self.reg[rega] > self.reg[reg_b]:
                self.fl = 0b00000010
            # else they are equal set E flag to 1
            else self.reg[rega] == self.reg[reg_b]
                self.fl = 0b00000001            
            
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
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
            
            
            is_alu_op = ((IR >> 5 ) & 0b001) == 1
            
            if is_alu_op:
                self.alu(IR, operand_a, operand_b)                
            else:
                self.bt[IR](operand_a, operand_b)   
                    
            sets_pc = (IR >> 4) & 0b00000001 == 0
            if sets_pc:
                num_operands = IR >> 6
                self.pc += 1 + num_operands         
            
                
    # bt functions            
    
    def hlt(self, operand_a, operand_b):
        self.running = False
                
    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        
    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        
    def push(self, operand_a, operand_b):
        self.sp -= 1
        # copy the value in the given register to the address pointed to by SP
        self.ram_write(self.reg[operand_a], self.sp)   

    def pop(self, operand_a, operand_b):
        # copy the value from the address pointed to by SP to the given register
        self.reg[operand_a] = self.ram_read(self.sp)
        # increment the SP
        self.sp += 1
        
    def call(self, operand_a, operand_b):
        # decrement the SP
        self.sp -= 1
        # write the return address to memory at the SP location
        self.ram_write(self.pc + 2, self.sp)
        # set PC to the address stored in the given register
        self.pc = self.reg[self.ram[operand_a]]
    
    def ret(self, operand_a, operand_b):
        # pop the value from the top of the stack and store it in the PC
        self.pc = self.ram_read(self.sp)
        # increment the SP
        self.sp += 1
                
            
          
                
