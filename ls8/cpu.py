"""CPU functionality."""

import sys



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.running = True
        self.instruction = {
            "HLT" : 0b00000001,
            "LDI" : 0b10000010,
            "PRN" : 0b01000111,
            'MUL' : 0b10100010,
        }

    def load(self):
        """Load a program into memory."""

        address = 0
        
        if len(sys.argv) != 2:
            print("no file given to run")
            
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
            
    def ram_read(self, address):
        # print(self.ram[address])
        return self.ram[address]      
        

    def ram_write(self, value, address):
        self.ram[address] = value        
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        
            # Internal Register
            IR = self.ram[self.pc]
            
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            # load data
            if IR == self.instruction['LDI']:
                # do something
                self.reg[operand_a] = operand_b
                self.pc += 2
            
            # print register number
            elif IR == self.instruction['PRN']:
                print(self.reg[operand_a])
                self.pc += 1
                
            elif IR == self.instruction['MUL']:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 2
            
            # Halt operation or exit()
            elif IR == self.instruction['HLT']:
                self.running = False
                
                
            self.pc += 1
                
            
            
            
            
cpu = CPU()

cpu.load()
cpu.run()