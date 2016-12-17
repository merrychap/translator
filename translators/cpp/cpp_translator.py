import re

from ..base_translator import TranslatorBase, ORANGE, PURPLE, RED, GRAY


reserved_words = {}


class CPPTranslator(TranslatorBase):
    def __init__(self, filename):
        self.filename = filename
        self.reserved_words = {}
        self.init_words()
        self.init_colors4reserved_words()

    def init_words(self):
        self.bool_w = ['false', 'true', 'cin', 'cout']
        self.logic_w = ['and_eq', 'and', 'bitand', 'bitor', 'compl', 'map',
                        'dynamic_cast', 'not', 'not_eq', 'nullptr', 'import'
                        'module', 'or', 'or_eq', 'private', 'include','public',
                        'protected', 'reinterpret_cast', 'requires', 'sizeof',
                        'synchronized', 'typeid', 'xor', 'xor_eq', 'vector']
        self.other_w = ['alignas', 'alignof', 'asm', 'atomic_cancel',
                        'atomic_commit', 'atomic_noexcept', 'auto', 'bool',
                        'break', 'case', 'catch', 'char', 'char16_t',
                        'char32_t', 'class', 'concept', 'const', 'constexpr',
                        'const_cast', 'continue', 'decltype', 'default',
                        'delete', 'do', 'double', 'else', 'enum', 'explicit',
                        'export', 'extern', 'float', 'for', 'friend', 'goto',
                        'if', 'inline', 'int', 'long', 'mutable', 'namespace',
                        'new', 'noexcept', 'operator', 'register', 'return',
                        'short', 'signed', 'static', 'static_assert',
                        'static_cast', 'struct', 'switch', 'template', 'this',
                        'thread_local', 'throw', 'typedef', 'typename',
                        'union', 'unsigned', 'using', 'virtual', 'void',
                        'volatile', 'while', 'string']

    def init_colors4reserved_words(self):
        global PURPLE, ORANGE, RED
        for words_class, color in [(self.bool_w, PURPLE), (self.logic_w, ORANGE),
                                (self.other_w, RED)]:
            for word in words_class:
                self.reserved_words[word] = color

    def get_comments(self, code):
        global GRAY
        return self.get_bounds(GRAY, r'//.*?', code)

    def escaping(self, code):
        tmp = re.sub('<', '&lt;', code)
        tmp = re.sub('>', '&gt;', tmp)
        return tmp

    def is_reserved_correct(self, match, code):
        ind = match.start() - 1
        if code[ind] == ';':
            if 'include' in code[ind-11:ind]:
                return False
        return True
