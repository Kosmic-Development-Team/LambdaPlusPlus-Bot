NEXT_ID = 0


class ProjectInstance:
    def __init__(self, name, bot):
        global NEXT_ID
        self.bot = bot
        self.name = name
        self.id = NEXT_ID
        NEXT_ID += 1

    async def handle_command(self, message, prefix, command, rest):
        pass
