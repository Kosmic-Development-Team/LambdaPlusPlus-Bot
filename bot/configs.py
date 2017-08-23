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

        #bot config
        self.token = config.get('Chat', 'Token', fallback=ConfigDefaults.token)
        self.prefix = config.get('Chat', 'Prefix', fallback=ConfigDefaults.prefix)
        self.channels = config.get('Chat', 'channel', fallback=ConfigDefaults.channels)

        #enabling interpreters
        self.enable_lambda_calc = config.get('Interpreters', 'LambdaCalculus', fallback=ConfigDefaults.enable_lambda_calc)
        self.enable_bf = config.get('Interpreters', 'BrainFuck', fallback=ConfigDefaults.enable_bf)

        #lambda config
        self.lambda_char = config.get('LambdaCalculus', 'Lambda', fallback=ConfigDefaults.lambda_char)
        self.combine_vars_sintax = config.get('LambdaCalculus', 'CombineVariablesSintax', fallback=ConfigDefaults.combine_vars_sintax)
        self.require_parentheses = config.get('LambdaCalculus', 'RequireParentheses', fallback=ConfigDefaults.require_parentheses)

        #bf config
        self.input_when_changed = config.get('BrainFuck', 'AskInputWhenMutated', fallback=ConfigDefaults.input_when_changed)
        self.use_hex = config.get('BrainFuck', 'UseHexadecimalInput', fallback=ConfigDefaults.use_hex)
        self.use_16bit = config.get('BrainFuck', 'Use16BitIntegers', fallback=ConfigDefaults.use_16bit)
        self.return_finish = config.get('BrainFuck', 'FillNullWhenReturned', fallback=ConfigDefaults.return_finish)
        self.use_meta_chars = config.get('BrainFuck', 'UseMetaCharCodes', fallback=ConfigDefaults.use_meta_chars)


class ConfigDefaults:
    #bot defaults
    token = None
    prefix = '&'
    channels = set()

    #enableling interpreters/meta settings
    enable_lambda_calc = False
    enable_bf = False
    #ad stuff for instance handling

    #lambda calculus defaults
    lambda_char = '~'
    combine_vars_sintax = False  #~xy instead of ~x.~y
    require_parentheses = False  #instead of having to assume things and you having to do debugging

    #bf defaults
    input_when_changed = True  #asks for an n-character input (or hex string) when one of the input addresses are changed, used, or use of meta chars
    use_hex = False  #use hex values as input when requesting input (can be changed with meta chars)
    use_16bit = False  #use 16 bit integers instead of 8 bit integers
    return_finish = True  #when typing in more than one character, replaces rest of data with 00 (or 0000 for 16bit)
    use_meta_chars = True  #enable non-classic bf chars for controling these settings while running the program

