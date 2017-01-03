import sys
import argparse

from translators.trans_distr import TransDistributor
from translators.python.python_trans import PythonTranslator
from translators.cpp.cpp_translator import CPPTranslator


def get_code(filname):
    with open(filname, 'r') as _file:
        return _file.read()

def main():
    distr = TransDistributor()

    parser = argparse.ArgumentParser()
    parser.add_argument('--ext', action='store', type=str,
                        help='Extension of programming language')
    parser.add_argument('--file', action='store', type=str,
                        help='File with source code')
    parser.add_argument('--descr', action='store', type=str,
                        help=('Description of source code (See structure'
                              ' in readme)'))
    args = parser.parse_args()

    filename = args.file
    descr = args.descr
    ext = args.ext

    if descr is None or filename is None:
        print('[-] Error occured')
        sys.exit()

    Translator = distr.get_translator(filename, ext)
    if Translator is None:
        sys.exit()
    Translator(filename, descr).translate(get_code(filename))


if __name__ == '__main__':
    main()
