import abc
import re


PURPLE = '#ad64ff'
ORANGE = '#e79951'
RED = '#ff3b24'
GREEN = '#64ff75'
BLUE = ' #51a9e7'
GRAY = '#606468'
BLACK = '#323231'
WHITE = '#ead09a'


class TranslatorBase:

    @abc.abstractmethod
    def translate(self, code):
        return

    @abc.abstractmethod
    def init_words(self):
        return

    @abc.abstractmethod
    def init_colors4reserved_words(self):
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
                '{background-color: %s;}</style></head><body>') % BLACK

    def get_suffix_html(self):
        return '</body></html>'

    def save_html(self, html):
        global WHITE
        filename = self.filename.rsplit('.', maxsplit=1)[0] + '.html'
        with open(filename, 'w') as _file:
            for line in html.split('\n'):
                indent = len(line) - len(line.lstrip(' '))
                _file.write(('<code style="margin-left: {}px; color: {};">{}'
                             '</code></br>\n').format(indent * 5, WHITE, line))

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
        global GREEN
        return self.get_bounds(GREEN, r'\'.*?\'', code) +\
               self.get_bounds(GREEN, r'\".*?\"', code)

    def get_digits(self, code):
        global BLUE
        return self.get_bounds(BLUE, r'\d+', code)
