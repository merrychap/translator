import re
import sys

from ..base_translator import TranslatorBase


class CPPTranslator(TranslatorBase):
    def __init__(self, filename, descr):
        self.filename = filename
        self.reserved_words = {}
        self.basic_colors = {}
        self.init_translator(descr)

    def escaping(self, code):
        tmp = re.sub('<', '&lt;', code)
        tmp = re.sub('>', '&gt;', tmp)
        return tmp

    def is_reserved_correct(self, match, code):
        offset = 11
        ind = match.start() - 1
        if code[ind] == ';':
            if 'include' in code[ind - offset:ind]:
                return False
        return True

    def get_comments(self, code):
        color = self.basic_colors['comments']
        g_bounds = []
        bounds = self.get_bounds(color, r'\/\*((.|\s)*?)\*\/', code)
        for bnd in bounds:
            st = bnd[0]
            for line in bnd[2].split('\n'):
                ind = len(line) - len(line.lstrip(' '))
                st += ind
                g_bounds.append((st, st + len(line) - ind + 1,
                                 line + '\n', color))
                st += len(line) - ind + 1
        return self.get_bounds(color, r'//.*', code) + g_bounds
