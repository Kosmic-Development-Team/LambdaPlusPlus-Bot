import os
import configparser


class Config:

    def __init__(self, conf_file):
        self.config_file = conf_file
        config = configparser.ConfigParser()

        if not config.read(conf_file, encoding='utf-8'):
            print('[config] Config file not found')
            os._exit(1)

        config = configparser.ConfigParser(interpolation=None)
        config.read(conf_file, encoding='utf-8')

        confsects = {'Bot', 'Interpreters', 'LambdaCalculus', 'Brainfuck'}.difference(config.sections())
        if confsects:
            print('[config] Config file contains unexpected/missing sections')
            os._exit(1)

        # bot config
        self.token = config.get('Bot', 'Token', fallback=ConfigDefaults.token)
        self.prefix = config.get('Bot', 'Prefix', fallback=ConfigDefaults.prefix).split()
        self.channels = config.get('Bot', 'BindChannel', fallback=ConfigDefaults.channels).split()

        self.prefix_length = []
        for i in range(len(self.prefix)):
            self.prefix[i] = self.prefix[i].replace('_', ' ')
            self.prefix_length.append(len(self.prefix[i]))

        # enabling interpreters
        self.enable_lambda_calc = config.get('Interpreters', 'LambdaCalculus',
                                             fallback=ConfigDefaults.enable_lambda_calc)
        self.enable_bf = config.get('Interpreters', 'Brainfuck', fallback=ConfigDefaults.enable_bf)

        # lambda config
        self.lambda_char = config.get('LambdaCalculus', 'Lambda', fallback=ConfigDefaults.lambda_char)
        self.combine_vars = config.get('LambdaCalculus', 'CombineVariables',
                                       fallback=ConfigDefaults.combine_vars)

        # bf config
        self.input_mode = config.get('Brainfuck', 'InputMode', fallback=ConfigDefaults.input_mode)
        self.use_hex = config.get('Brainfuck', 'UseHexadecimalInput', fallback=ConfigDefaults.use_hex)
        self.use_16bit = config.get('Brainfuck', 'Use16Bit', fallback=ConfigDefaults.use_16bit)
        self.max_iterations = config.get('Brainfuck', 'MaxIterations', fallback=ConfigDefaults.use_16bit)
        self.return_fill = config.get('Brainfuck', 'FillSpaceWhenReturned', fallback=ConfigDefaults.return_fill)
        self.use_extra_chars = config.get('Brainfuck', 'UseExtraSymbols', fallback=ConfigDefaults.use_extra_chars)
        self.use_meta_chars = config.get('Brainfuck', 'UseMetaSymbols', fallback=ConfigDefaults.use_meta_chars)

        # Check the values for correct type and report if not (uses same var) ** ---------------------------------------
        self.enable_lambda_calc = _report_default_use(_to_bool(self.enable_lambda_calc), 'LambdaCalculus',
                                                      ConfigDefaults.enable_lambda_calc)
        self.enable_bf = _report_default_use(_to_bool(self.enable_bf), 'Brainfuck',
                                             ConfigDefaults.enable_bf)

        # LambdaCalculus
        self.combine_vars = _report_default_use(_to_bool(self.combine_vars), 'CombineVariables',
                                                ConfigDefaults.combine_vars)

        # Brainfuck
        self.input_mode = abs(_report_default_use(_to_int(self.input_mode), 'InputMode',
                                                  ConfigDefaults.input_mode)) % 3
        self.use_hex = _report_default_use(_to_bool(self.use_hex), 'UseHexadecimalInput',
                                           ConfigDefaults.use_hex)
        self.use_16bit = _report_default_use(_to_bool(self.use_16bit), 'Use16Bit',
                                             ConfigDefaults.use_16bit)
        self.max_iterations = _report_default_use(_to_int(self.max_iterations), 'MaxIterations',
                                                  ConfigDefaults.max_iterations)
        self.return_fill = _report_default_use(_to_bool(self.return_fill), 'FillSpaceWhenReturned',
                                               ConfigDefaults.return_fill)
        self.use_extra_chars = _report_default_use(_to_bool(self.use_extra_chars), 'UseExtraSymbols',
                                                   ConfigDefaults.use_extra_chars)
        self.use_meta_chars = _report_default_use(_to_bool(self.use_meta_chars), 'UseMetaSymbols',
                                                  ConfigDefaults.use_meta_chars)


def _report_default_use(var, var_name, default_val):
    if var is None:
        print('[Config] Malformed input for config option', var_name + ', using default value instead:', default_val)
        return default_val
    return var

def _to_bool(cnf):
    if cnf == 'True':
        return True
    if cnf == 'False':
        return False
    return None

def _to_int(cnf):
    try:
        return int(cnf)
    except ValueError:
        return None


class ConfigDefaults:
    # bot defaults
    token = None
    prefix = '&'
    channels = ''

    # enabling interpreters/meta settings
    enable_lambda_calc = False
    enable_bf = False
    # ad stuff for instance handling

    # Lambda Calculus defaults
    lambda_char = '~'
    combine_vars = False  # ~xy instead of ~x.~y

    # Brainfuck defaults
    input_mode = 0  # 0-classic 1-deferred 2-buffered
    use_hex = False  # use hex values as input when requesting input (can be changed with meta chars)
    use_16bit = False  # use 16 bit integers instead of 8 bit integers
    max_iterations = 2 ** 16  # max amount of bf iterations
    return_fill = True  # when typing in more than one character, replaces rest of data with 00 (or 0000 for 16bit)
    use_extra_chars = True  # enable extra bf chars for making logic easier
    use_meta_chars = True  # enable meta bf chars for controlling these settings while running the program

    options_file = 'options.ini'

