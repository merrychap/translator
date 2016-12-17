import abc
import re
import sys
import json

from collections import namedtuple


class TranslatorBase:

    @abc.abstractmethod
    def translate(self, code):
        return

    @abc.abstractmethod
    def escaping(self, code):
        return code

    @abc.abstractmethod
    def get_comments(self, code):
        return

    @abc.abstractmethod
    def is_reserved_correct(self, match, code):
        return True

    def init_translator(self, description):
        with open(description, 'r') as _file:
            try:
                descr = json.loads(_file.read())
                self.parse_descr(descr)
            except Exception:
                print('[-] Error occured')
                sys.exit()

    def parse_descr(self, descr):
        for color, words in descr['reserved']:
            for word in words:
                self.reserved_words[word] = color
        for name, color in descr['basic_colors'].items():
            self.basic_colors[name] = color

    def translate(self, code):
        code = self.escaping(code)

        res_words = self.get_reserved_words(code)
        digits = self.get_digits(code)
        strings = self.get_strings(code)
        comments = self.get_comments(code)

        bounds = res_words + digits + strings + comments
        bounds.sort()

        html = self.get_prefix_html() + self.replace_obj(bounds, code) + \
               self.get_suffix_html()
        self.save_html(html)

    def get_prefix_html(self):
        global BLACK
        return ('<!DOCTYPE html><html><head><style> body '
                '{background-color: %s;}</style></head><body>') % \
                self.basic_colors['background']

    def get_suffix_html(self):
        return '</body></html>'

    def save_html(self, html):
        color = self.basic_colors['text']
        filename = self.filename.rsplit('.', maxsplit=1)[0] + '.html'
        with open(filename, 'w') as _file:
            for line in html.split('\n'):
                indent = len(line) - len(line.lstrip(' '))
                _file.write(('<code style="margin-left: {}px; color: {};">{}'
                             '</code></br>\n').format(indent * 5, color, line))

    def replace_obj(self, bounds, code):
        html = ''
        index = 0
        _st = 0
        while index < len(bounds):
            st, en, txt, clr = (bounds[index][i] for i in range(4))

            index += 1
            while index < len(bounds) and en > bounds[index][0]:
                index += 1
            if index >= len(bounds):
                break
            local_end = bounds[index][0]
            html += code[_st:st] + self.get_span(txt, clr) + code[en:local_end]
            _st = local_end
        html += code[_st:st] + self.get_span(txt, clr) + code[en:]
        return html

    def get_span(self, text, color):
        return '<span style="color:{}">{}</span>'.format(color, text)

    def get_bounds(self, color, pattern, s):
        bounds = []
        for match in re.finditer(pattern, s):
            if not self.is_reserved_correct(match, s):
                continue
            bounds.append((match.start(), match.end(), match.group(0), color))
        return bounds

    def get_reserved_words(self, code):
        bounds = []
        for word, color in self.reserved_words.items():
            bounds += self.get_bounds(color, r'\b%s\b' % word, code)
        return bounds

    def get_strings(self, code):
        color = self.basic_colors['strings']
        return self.get_bounds(color, r'\'.*?\'', code) +\
               self.get_bounds(color, r'\".*?\"', code)

    def get_digits(self, code):
        color = self.basic_colors['digits']
        return self.get_bounds(color, r'\d+', code)
