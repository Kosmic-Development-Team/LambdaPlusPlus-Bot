
async def handle_command(message, prefix, bot):
    try:
        command, rest = (message.content[bot.config.prefix_length[prefix]:]).split(None, 1)
        rest = _remove_discord_coding_modifier(rest)
        print('[Command] @' + message.author.name, 'in', '#' + message.channel.name + ':', command, rest)
    except:
        pass
    else:
        if command in ['echo', 'say', 'repeat']:
            await _comm_echo(bot, message, rest)



async def _comm_echo(bot, message, rest):
    await bot.send_message(message.channel, '```' + rest + '```')


def _remove_discord_coding_modifier(msg):  # i.e. removes all unescaped graves (`)
    msg_split = msg.split('\\\\')
    new_msg = ''
    first = True
    for ms in msg_split:
        ms = _remove_unescaped_graves(ms)
        if not first:
            new_msg += '\\\\'
        else:
            first = False
        new_msg += ms
    return new_msg


def _remove_unescaped_graves(msg):
    msg_split = msg.split('\\`')
    new_msg = ''
    first = True
    for ms in msg_split:
        ms = ms.replace('`', '')
        if not first:
            new_msg += '\\`'
        else:
            first = False
        new_msg += ms
    return new_msg
