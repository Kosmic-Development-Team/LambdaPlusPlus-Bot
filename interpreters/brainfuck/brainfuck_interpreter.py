class BrainfuckInterpreter:

    def __init__(self, inst, bits, use_extra, max_iterations):

        self.instance = inst

        self.bits = bits                # Bits per memory slot. False: 8 bits, True: 16 bits
        self.use_extra = use_extra      # Whether to use extra characters (%).
        # use meta characters ($, &, !).
        self.max_iterations = max_iterations  # TODO have a server max to prevent this being set to some ungodly value

        self.run = None

    # ideally, it should never return -3
    async def new_run(self, program, channel):  # 0-success 1-ask for input -1-instance already running -3-faulty run
        if self.run is None:
            self.run = BFData(program, self.bits)
            return await self.program_run(channel)
        return -1

    async def add_to_buffer(self, buffer, channel):  # 0-success 1-ask for input -1-not paused -2-no current program -3-faulty run
        if self.run is not None:
            if self.run.paused:
                self.run.input += buffer
                self.run.paused = False
                return await self.program_run(channel)
            return -1
        return -2

    async def program_run(self, channel):
        if self.run is not None:
            running = True

            while running and not self.run.stopped and not self.run.paused:
                if self.run.iterations > self.max_iterations or self.run.pc >= self.run.end:
                    running = False
                else:
                    char = self.run.program[self.run.pc]

                    if char == '>':  # Increment pointer
                        self.run.ptr += 1
                        if self.bits:
                            self.run.ptr %= 65536
                        else:
                            self.run.ptr %= 256

                    elif char == '<':  # Decrement pointer
                        self.run.ptr -= 1
                        if self.bits:
                            self.run.ptr += 65536
                            self.run.ptr %= 65536
                        else:
                            self.run.ptr += 256
                            self.run.ptr %= 256

                    elif char == '+':  # Increment value at pointer
                        self.run.memory[self.run.ptr] += 1
                        if self.bits:
                            self.run.memory[self.run.ptr] %= 65536
                        else:
                            self.run.memory[self.run.ptr] %= 256

                    elif char == '-':  # Decrement value at pointer
                        self.run.memory[self.run.ptr] -= 1
                        if self.bits:
                            self.run.memory[self.run.ptr] += 65536
                            self.run.memory[self.run.ptr] %= 65536
                        else:
                            self.run.memory[self.run.ptr] += 256
                            self.run.memory[self.run.ptr] %= 256

                    elif char == '[':  # Start loop
                        if self.run.memory[self.run.ptr] == 0:  # Find corresponding end bracket and go there
                            brackets = 1
                            while brackets != 0:
                                self.run.pc += 1
                                if self.run.program[self.run.pc] == '[':
                                    brackets += 1
                                elif self.run.program[self.run.pc] == ']':
                                    brackets -= 1

                    elif char == ']':  # End loop
                        if self.run.memory[self.run.ptr] != 0:  # Loop back to corresponding beginning bracket
                            brackets = 1
                            while brackets != 0:
                                self.run.pc -= 1
                                if self.run.program[self.run.pc] == '[':
                                    brackets -= 1
                                elif self.run.program[self.run.pc] == ']':
                                    brackets += 1

                    elif char == ',':  # Take input
                        np = self.run.get_next()
                        if np == -1:
                            self.run.paused = True
                            return 1
                        else:
                            self.run.memory[self.run.ptr] = np

                    elif char == '.':  # Prepare print
                        self.run.output.append(self.run.memory[self.run.ptr])

                    elif char == '%' and self.use_extra:  # Set pointer to value at current pointer
                        self.run.ptr = self.run.memory[self.run.ptr]

                    elif char == '$':  # clear buffered input
                        self.run.output = []

                    elif char == '&':  # Toggle between character and hex input  TODO: toggle through 3 states
                        pass

                    elif char == '!':  # Flush output and present print
                        await self.instance.interpreter_print(channel, self.run.get_output())

                    else:
                        self.run.iterations -= 1

                    self.run.iterations += 1
                    self.run.pc += 1

            if not running or self.run.stopped:
                # TODO: Closing procedures here
                self.run = None
                return 0
            return -3

    # TODO: Remove this method
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


class BFData:
    def __init__(self, program, bits):
        self.memory = [0] * 256  
        self.program = program   # program string
        self.end = len(program)  # length of the program to be run
        self.input = []          # input buffer (buffered input mode only)
        self.output = []         # output buffer
        self.ptr = 0             # pointer to memory slot
        self.pc = 0              # program counter
        self.iterations = 0      # iterations which have passed
        self.paused = False      # awaiting more input data
        self.stopped = False     # halt requested from outside
        if not bits:
            self.memory = [0] * 65536

    def get_next(self):  # for buffered input mode only
        if self.input:
            nxt, *self.input = self.input
            return nxt
        return -1

    def get_output(self):
        out = self.output
        self.output = []
        return out
