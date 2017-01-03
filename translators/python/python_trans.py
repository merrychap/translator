import re

from ..base_translator import TranslatorBase


reserved_words = {}


class PythonTranslator(TranslatorBase):
    def __init__(self, filename, descr):
        self.filename = filename
        self.reserved_words = {}
        self.basic_colors = {}
        self.init_translator(descr)

    def init_words(self):
        self.bool_w = ['False', 'True', 'None']
        self.logic_w = ['and', 'in', 'is', 'not', 'or', 'tuple', 'list', 'str',
                        'open']
        self.other_w = ['as', 'assert', 'break', 'class', 'continue', 'def',
                        'del', 'elif', 'else', 'except', 'finally', 'for',
                        'from', 'global', 'if', 'import', 'nonlocal', 'pass',
                        'raise', 'return', 'try', 'while', 'with', 'yield']

    def get_comments(self, code):
        return self.get_bounds(self.basic_colors['comments'], r'#.*', code)
