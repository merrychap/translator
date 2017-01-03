import unittest

from translators.trans_distr import TransDistributor
from translators.cpp.cpp_translator import CPPTranslator
from translators.python.python_trans import PythonTranslator


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.distr = TransDistributor()

        self.cpp_trans = self.distr.get_translator('', '.cpp')('', './lang_descr/cpp_descr.json')
        self.py_trans = self.distr.get_translator('', '.py')('', './lang_descr/python_descr.json')

    def execute(self, trans, code, get_func, ans):
        bnd = get_func(code)
        bnd.sort()
        self.assertEqual(trans.replace_obj(bnd, code), ans)

    def test_cpp_digits(self):
        code = 'int a = 253627'
        self.execute(self.cpp_trans, code, self.cpp_trans.get_digits,
                     'int a = <span style="color:#51a9e7">253627</span>')

    def test_python_digits(self):
        code = 'a = 236823'
        self.execute(self.py_trans, code, self.py_trans.get_digits,
                     'a = <span style="color:#51a9e7">236823</span>')

    def test_cpp_py_strings(self):
        code = ('str = "this is test string"\n'
                'str2 = \'string with another brackets\'')
        ans = ('str = <span style="color:#64ff75">"this is test string"</span>'
               '\nstr2 = <span style="color:#64ff75">\'string with another '
               'brackets\'</span>')
        self.execute(self.cpp_trans, code, self.cpp_trans.get_strings, ans)

        self.execute(self.py_trans, code, self.py_trans.get_strings, ans)

    def test_cpp_reserved_words(self):
        code = ('#include <cstdio>\n'
                '#include <vector>\n\n'
                'using namespace std;\n\n'
                'int main() {\n'
                '    vector<int> v;\n'
                '}')
        ans = ('#<span style="color:#e79951">include</span> &lt;cstdio&gt;\n'
               '#<span style="color:#e79951">include</span> &lt;vector&gt;\n\n'
               '<span style="color:#ff3b24">using</span> '
               '<span style="color:#ff3b24">namespace</span> std;\n\n'
               '<span style="color:#ff3b24">int</span> main() {\n'
               '    <span style="color:#e79951">vector</span>&lt;'
               '<span style="color:#ff3b24">int</span>&gt; v;\n}')
        code = self.cpp_trans.escaping(code)

        self.execute(self.cpp_trans, code,
                     self.cpp_trans.get_reserved_words, ans)

    def test_py_reserved_words(self):
        code = ('import re\n'
                'import socket\n\n'
                'from test.package import TestClass\n\n\n'
                'def solve(arg1, arg2):\n'
                '    if arg1 > 0 and arg2 > 0:\n'
                '        return arg1 + arg2\n'
                '    else:\n'
                '        return True')
        ans = ('<span style="color:#ff3b24">import</span> re\n'
               '<span style="color:#ff3b24">import</span> socket\n\n'
               '<span style="color:#ff3b24">from</span> test.package '
               '<span style="color:#ff3b24">import</span> TestClass\n\n\n'
               '<span style="color:#ff3b24">def</span> solve(arg1, arg2):\n'
               '    <span style="color:#ff3b24">if</span> arg1 > 0 <span '
               'style="color:#e79951">and</span> arg2 > 0:\n'
               '        <span style="color:#ff3b24">return</span> arg1 + arg2\n'
               '    <span style="color:#ff3b24">else</span>:\n'
               '        <span style="color:#ff3b24">return</span>'
               ' <span style="color:#ad64ff">True</span>')
        self.execute(self.py_trans, code,
                     self.py_trans.get_reserved_words, ans)

    def test_cpp_one_line_comments(self):
        code = ('int a = 0;\n'
                '//string str = "testtesttest";\n'
                'bool flag = true; //false')
        ans = ('int a = 0;\n'
               '<span style="color:#606468">//string '
               'str = "testtesttest";</span>\n'
               'bool flag = true; <span style="color:#606468">//false</span>')
        self.execute(self.cpp_trans, code, self.cpp_trans.get_comments, ans)

    def test_cpp_mult_line_comments(self):
        code = ('int a = 0;\n'
                '/*vector<int> v;\n'
                'v.push_back(1);\n'
                'v.pop_back();\n'
                'printf("%d", v.size());*/\n'
                'printf("%d", a)')
        ans = ('int a = 0;\n'
               '<span style="color:#606468">/*vector<int> v;</span>\n'
               '<span style="color:#606468">v.push_back(1);</span>\n'
               '<span style="color:#606468">v.pop_back();</span>\n'
               '<span style="color:#606468">printf("%d", v.size());*/</span>\n'
               'printf("%d", a)')
        self.execute(self.cpp_trans, code, self.cpp_trans.get_comments, ans)

    def test_py_comments(self):
        code = ('a = 0\n'
                '# b = a + 2\n'
                '# s = \'test string\'\n'
                's = \'uncommented string\'')
        ans = ('a = 0\n'
               '<span style="color:#606468"># b = a + 2</span>\n'
               '<span style="color:#606468"># s = \'test string\'</span>\n'
               's = \'uncommented string\'')
        self.execute(self.py_trans, code, self.py_trans.get_comments, ans)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
