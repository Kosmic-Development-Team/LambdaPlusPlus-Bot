#from instances.test_instance import TestProjectInstance
from instances.brainfuck_instance import BrainfuckInstance


USER_INSTANCE_DICT = {}
CURRENT_INSTANCES = []


async def handle_command(message, prefix, bot):
    try:
        command, rest = (message.content[bot.config.prefix_length[prefix]:]).split(None, 1)
        rest = _remove_discord_coding_modifier(rest)
    except:
        command = message.content
        rest = ''
    finally:
        print('[Command] @' + message.author.name, 'in', '#' + message.channel.name + ':', command, rest)
        if command in ['echo', 'say', 'repeat']:
            await _comm_echo(bot, message, rest)
        elif command in ['newinstance', 'newinst', 'ni']:
            await _comm_new_instance(bot, message, rest)
        elif command in ['instance', 'inst', 'i']:
            await _comm_instance(bot, message, prefix, rest)

async def _comm_echo(bot, message, rest):
    await bot.send_message(message.channel, rest)


async def _comm_new_instance(bot, message, rest):
    try:
        inst_type, rest = rest.split(None, 1)
        inst_name = rest.replace(' ', '-')
        if inst_name == '':
            raise Exception()
    except:
        await bot.send_message(message.channel, 'Proper usage: `newinstance [type] [name]`')
    else:
        inst = None
        if inst_type in ['brainfuck', 'bf']:
            inst = BrainfuckInstance(inst_name, bot)
        #elif inst_type in ['test', 'ts']:
        #    inst = TestProjectInstance(inst_name, bot)

        if inst:
            USER_INSTANCE_DICT[message.author.id] = inst
            CURRENT_INSTANCES.append(inst)
            await bot.send_message(message.channel, 'Instance created successfully: `' + inst_name + '` - `' +
                                   message.author.name + '`')
        else:
            await bot.send_message(message.channel, 'Instance type does not exist: `' + inst_type + '`')


async def _comm_instance(bot, message, prefix, rest):
    try:
        command, rest = rest.split(None, 1)
    except:
        command = rest
        rest = ''
    finally:

        if command != '':
            usr = message.author.id
            if usr in USER_INSTANCE_DICT:
                await USER_INSTANCE_DICT[usr].handle_command(message, prefix, command, rest)
            else:
                await bot.send_message(message.channel, 'You must create or join an instance first')
        else:
            await bot.send_message(message.channel, 'Proper usage: `instance [command]`')


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
