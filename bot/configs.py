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

        confsects = {'Bot', 'Interpreters', 'LambdaCalculus', 'BrainFuck'}.difference(config.sections())
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
        self.enable_bf = config.get('Interpreters', 'BrainFuck', fallback=ConfigDefaults.enable_bf)

        # lambda config
        self.lambda_char = config.get('LambdaCalculus', 'Lambda', fallback=ConfigDefaults.lambda_char)
        self.combine_vars = config.get('LambdaCalculus', 'CombineVariables',
                                              fallback=ConfigDefaults.combine_vars)

        # bf config
        self.input_mode = config.get('BrainFuck', 'InputMode', fallback=ConfigDefaults.input_mode)
        self.use_hex = config.get('BrainFuck', 'UseHexadecimalInput', fallback=ConfigDefaults.use_hex)
        self.use_16bit = config.get('BrainFuck', 'Use16BitIntegers', fallback=ConfigDefaults.use_16bit)
        self.return_fill = config.get('BrainFuck', 'FillNullWhenReturned', fallback=ConfigDefaults.return_fill)
        self.use_extra_chars = config.get('BrainFuck', 'UseExtraCharCodes', fallback=ConfigDefaults.use_extra_chars)
        self.use_meta_chars = config.get('BrainFuck', 'UseMetaCharCodes', fallback=ConfigDefaults.use_meta_chars)

class ConfigDefaults:
    # bot defaults
    token = None
    prefix = '&'
    channels = set()

    # enabling interpreters/meta settings
    enable_lambda_calc = False
    enable_bf = False
    # ad stuff for instance handling

    # lambda calculus defaults
    lambda_char = '~'
    combine_vars = False  # ~xy instead of ~x.~y

    # bf defaults
    input_mode = 0  # 0-classic 1-deferred 2-buffered
    use_hex = False  # use hex values as input when requesting input (can be changed with meta chars)
    use_16bit = False  # use 16 bit integers instead of 8 bit integers
    return_fill = True  # when typing in more than one character, replaces rest of data with 00 (or 0000 for 16bit)
    use_extra_chars = True  # enable extra bf chars for making logic easier
    use_meta_chars = True  # enable meta bf chars for controlling these settings while running the program

    options_file = 'options.ini'

