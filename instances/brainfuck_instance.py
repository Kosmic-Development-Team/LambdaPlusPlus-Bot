from instances.instance_base import ProjectInstance
from interpreters.brainfuck.brainfuck_interpreter import BrainfuckInterpreter


class BrainfuckInstance(ProjectInstance):
    def __init__(self, name, bot):
        super().__init__(name, bot)

        self.use_16bit = self.bot.config.use_16bit
        print(self.use_16bit)
        self.input_mode = self.bot.config.input_mode                # TODO: Remove this
        self.in_out_mode = self.bot.config.use_hex  # TODO: have this be am int denoting between char, hex, and int input
        self.use_extra = self.bot.config.use_extra_chars
        self.use_meta = self.bot.config.use_meta_chars              # TODO: Remove this
        self.max_iterations = self.bot.config.max_iterations
        self.return_fill = self.bot.config.return_fill              # TODO: Remove this

        self.bf_interpreter = BrainfuckInterpreter(self, self.use_16bit, self.use_extra, self.max_iterations)
        self.run_input_mode = self.run_output_mode = self.in_out_mode

    async def interpreter_print(self, channel, out):  # input is a list of integers
        # TODO: configure output based on the output setting
        output = str(out)
        await self.bot.send_message(channel, 'Interpreter and output: `' + self.name + '`\n`' + output + '`')

    async def handle_command(self, message, prefix, command, rest):
        if command in ['start', 's']:
            await self._comm_start(message, rest)
        elif command in ['input', 'in']:
            await self._comm_input(message, rest)

    async def _comm_start(self, message, rest):
        nxt = await self.bf_interpreter.new_run(rest, message.channel)
        if nxt == 0:
            await self.bot.send_message(message.channel, 'Interpreter program ended: `' + self.name + '`')
        elif nxt == 1:
            await self.bot.send_message(message.channel, 'Interpreter needs input: `' + self.name + '`')
        elif nxt == -1:
            await self.bot.send_message(message.channel, 'Interpreter already running a program: `' + self.name + '`')
        elif nxt == -3:
            await self.bot.send_message(message.channel, 'Interpreter encountered an error: `' + self.name + '`')

    async def _comm_input(self, message, rest):
        # TODO: format input using the input_mode
        formatted_input = []
        for i in rest:
            formatted_input.append(ord(i))
        # above is bad
        nxt = await self.bf_interpreter.add_to_buffer(formatted_input, message.channel)
        if nxt == 0:
            await self.bot.send_message(message.channel, 'Interpreter program ended: `' + self.name + '`')
        elif nxt == 1:
            await self.bot.send_message(message.channel, 'Interpreter needs input: `' + self.name + '`')
        elif nxt == -1:
            await self.bot.send_message(message.channel, 'Interpreter not paused to take input: `' + self.name + '`')
        elif nxt == -2:
            await self.bot.send_message(message.channel, 'Interpreter does not have a program running: `' + self.name + '`')
        elif nxt == -3:
            await self.bot.send_message(message.channel, 'Interpreter encountered an error: `' + self.name + '`')
