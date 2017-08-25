from instances.instance_base import ProjectInstance


class TestProjectInstance(ProjectInstance):
    def __init__(self, name, bot):
        super().__init__(name, bot)
        self.data = {}

    async def handle_command(self, message, prefix, command, rest):
        if command in ['store', 's']:
            await self._comm_store(message, rest)
        elif command in ['get', 'g']:
            await self._comm_get(message)

    async def _comm_store(self, message, rest):
        self.data[message.author.id] = rest
        await self.bot.send_message(message.channel, 'Data stored: `' + rest + '`')

    async def _comm_get(self, message):
        await self.bot.send_message(message.channel, 'Data: `' + self.data[message.author.id] + '`')

