import re
import sys


from ..base_translator import TranslatorBase


class CPPTranslator(TranslatorBase):
    def __init__(self, filename, descr):
        self.filename = filename
        self.reserved_words = {}
        self.basic_colors = {}
        self.init_translator(descr)

    def get_comments(self, code):
        return self.get_bounds(self.basic_colors['comments'], r'//.*?', code)

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
