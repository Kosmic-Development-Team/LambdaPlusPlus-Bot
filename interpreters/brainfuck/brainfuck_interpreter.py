class BrainfuckInterpreter:

    def __init__(self, bits, input_mode, use_hex, use_extra, use_meta, max_iterations):
        self.bits = bits                # Bits per memory slot. True: 8 bits, False: 16 bits
        self.input_mode = input_mode    # Input mode. 0: Classic, 1: Deferred, 2: Buffered
        self.use_hex = use_hex          # Character input mode. True: Hex, False: Characters
        self.use_extra = use_extra      # Whether to use extra characters (%).
        self.use_meta = use_meta        # Whether to use meta characters ($, &, !).
        self.max_iterations = max_iterations

    def eval(self, program):
        if self.bits:
            memory = [0] * 256     # Program memory. 8 bit: 256 slots, 16 bit: 65536 slots
        else:
            memory = [0] * 65536
        if self.use_meta:
            output = ""            # Output buffer.

        ptr = 0     # pointer to memory slot
        pc = 0      # program counter
        end = len(program)
        iterations = 0
        while iterations < self.max_iterations and pc < end:
            iterations += 1
            char = program[pc]

            if char == '>':     # Increment pointer
                ptr += 1
                if self.bits:
                    ptr %= 256
                else:
                    ptr %= 65536

            elif char == '<':   # Decrement pointer
                ptr -= 1
                if self.bits:
                    ptr += 256
                    ptr %= 256
                else:
                    ptr += 65536
                    ptr %= 65536

            elif char == '+':   # Increment value at pointer
                memory[ptr] += 1
                if self.bits:
                    memory[ptr] %= 256
                else:
                    memory[ptr] %= 65536

            elif char == '-':   # Decrement value at pointer
                memory[ptr] -= 1
                if self.bits:
                    memory[ptr] += 256
                    memory[ptr] %= 256
                else:
                    memory[ptr] += 65536
                    memory[ptr] %= 65536

            elif char == '[':   # Start loop
                if memory[ptr] == 0:   # Find corresponding end bracket and go there
                    brackets = 1
                    while brackets != 0:
                        pc += 1
                        if program[pc] == '[':
                            brackets += 1
                        elif program[pc] == ']':
                            brackets -= 1

            elif char == ']':   # End loop
                if memory[ptr] != 0:   # Loop back to corresponding beginning bracket
                    brackets = 1
                    while brackets != 0:
                        pc -= 1
                        if program[pc] == '[':
                            brackets -= 1
                        elif program[pc] == ']':
                            brackets += 1

            elif char == ',':   # Take input
                memory[ptr] = ord(input()[0])
                # TODO: Full implementation of input
                # if self.input_mode == 0:
                #     get_input_classical(self, use_hex)
                # elif self.input_mode == 1:
                #     pass
                # elif self.input_mode == 2:
                #     get_input_classical(self, use_hex)

            elif char == '.':   # Prepare print
                print(memory[ptr])
                # TODO: Full implementation of print
                # if self.use_meta:
                #     pass
                # else:
                #     pass

            elif char == '%' and self.use_extra:    # Set pointer to value at current pointer
                ptr = memory[ptr]

            elif char == '$' and self.use_meta:     # Take deferred input or clear buffered input
                pass

            elif char == '&' and self.use_meta:     # Toggle between character and hex input
                pass

            elif char == '!' and self.use_meta:     # Flush output and present print
                pass

            pc += 1

    def get_input_classical(self, use_hex):
        pass
