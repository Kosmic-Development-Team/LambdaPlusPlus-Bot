import discord
import asyncio
from bot.commands import handle_command

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
                comm = self.is_command(message.content)
                if comm != -1:
                    await handle_command(message, comm, self)
                else:
                    print('[Message] @' + message.author.name, 'in', '#' + message.channel.name + ':', message.content)

    def is_command(self, msg):
        msg_length = len(msg)
        for i in range(len(self.config.prefix)):
            if msg_length > self.config.prefix_length[i]\
                    and msg[0:self.config.prefix_length[i]] == self.config.prefix[i]:
                return i
        return -1


if __name__ == '__main__':
    bot = LambdaBot()
    bot.run()
