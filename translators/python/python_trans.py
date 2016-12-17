import re

from ..base_translator import TranslatorBase, BLUE, ORANGE, PURPLE, RED, GRAY


reserved_words = {}


class PythonTranslator(TranslatorBase):
    def __init__(self, filename):
        self.filename = filename
        self.reserved_words = {}
        self.init_words()
        self.init_colors4reserved_words()

    def init_words(self):
        self.bool_w = ['False', 'True', 'None']
        self.logic_w = ['and', 'in', 'is', 'not', 'or', 'tuple', 'list', 'str',
                        'open']
        self.other_w = ['as', 'assert', 'break', 'class', 'continue', 'def',
                        'del', 'elif', 'else', 'except', 'finally', 'for',
                        'from', 'global', 'if', 'import', 'nonlocal', 'pass',
                        'raise', 'return', 'try', 'while', 'with', 'yield']

    def init_colors4reserved_words(self):
        global PURPLE, ORANGE, RED
        for words_class, color in [(self.bool_w, PURPLE), (self.logic_w, ORANGE),
                                (self.other_w, RED)]:
            for word in words_class:
                self.reserved_words[word] = color

    def get_comments(self, code):
        global GRAY
        return self.get_bounds(GRAY, r'#.*?', code)
