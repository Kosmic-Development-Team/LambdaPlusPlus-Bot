from instances.test_instance import ProjectInstance
from interpreters.brainfuck.brainfuck_interpreter import BrainfuckInterpreter


class BrainfuckInstance(ProjectInstance):
    def __init__(self, name, bot):
        super().__init__(name, bot)

        self.use_16bit = self.bot.config.use_16bit
        self.input_mode = self.bot.config.input_mode
        self.input_hex = self.bot.config.use_hex
        self.output_hex = self.bot.config.use_hex  # make a config option *********************************************
        self.use_extra = self.bot.config.use_extra_chars
        self.use_meta = self.bot.config.use_meta_chars
        self.max_iterations = 1024                 # make a config option *********************************************
        self.return_fill = self.bot.config.return_fill

        self.bf_interpreter = BrainfuckInterpreter(self.use_16bit, self.input_mode, self.use_extra, self.use_meta, self.max_iterations)

    def handle_command(self, message, prefix, command, rest):
        pass
