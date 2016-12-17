import sys
import argparse


from translators.python.python_trans import PythonTranslator
from translators.cpp.cpp_translator import CPPTranslator


translators = {
    'py': PythonTranslator,
    'cpp': CPPTranslator
}


def get_code(filname):
    with open(filname, 'r') as _file:
        return _file.read()

def get_translator(filname, lang):
    global translators

    try:
        if lang is None:
            lang = filname.rsplit('.', maxsplit=1)[-1]
        return translators[lang]
    except KeyError:
        print("[-] Error occurred")
        sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ext', action='store', type=str,
                        help='Extension of programming language')
    parser.add_argument('--file', action='store', type=str,
                        help='File with source code')
    args = parser.parse_args()

    filename = args.file
    ext = args.ext

    translator = get_translator(filename, ext)
    translator(filename).translate(get_code(filename))


if __name__ == '__main__':
    main()
