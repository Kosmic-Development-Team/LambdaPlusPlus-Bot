import discord
import asyncio

from bot.configs import Config, ConfigDefaults

class LambdaBot(discord.Client):
    def __init__(self, config_file=ConfigDefaults.options_file):
        self.config = Config(config_file)
        super().__init__()


    def _cleanup(self):
        try:
            self.loop.run_until_complete(self.logout())
        except:
            pass

        ongoing = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*ongoing)

        try:  #go through some save function first *********************************************************************
            gathered.cancel()
            self.loop.run_until_complete(gathered)
            gathered.exception()
        except:
            pass

    def run(self, *args, **kwargs):
        try:
            self.loop.run_until_complete(self.start(self.config.token))
        except discord.errors.LoginFailure:
            print('[login] Login failure')
        finally:
            try:
                self._cleanup()
            except Exception as e:
                print('[Cleanup] Error during cleanup:', e)

            self.loop.close()

    async def on_message(self, message):
        await self.wait_until_ready()
        if message.channel.id in self.config.channels:
            if message.author.name != self.user.name:
                if message.content[0] == self.config.prefix:
                    await self.handle_command(message)

    async def handle_command(self, message):
        command, *rest = (message.content[1:]).split(' ', 1)
        print('[Command]', command, rest)
        if command == 'echo':
            await self.send_message(message.channel, rest[0])

if __name__ == '__main__':
    bot = LambdaBot()
    bot.run()
