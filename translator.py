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

def get_translator(filname, ext):
    global translators

    try:
        if ext is None:
            ext = filname.rsplit('.', maxsplit=1)[-1]
        return translators[ext]
    except KeyError:
        print("[-] Error occurred")
        sys.exit()


def main():
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

    Translator = get_translator(filename, ext)
    Translator(filename, descr).translate(get_code(filename))


if __name__ == '__main__':
    main()
