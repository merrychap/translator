import os

from .cpp.cpp_translator import CPPTranslator
from .python.python_trans import PythonTranslator


class TransDistributor:
    def __init__(self):
        self.translators = {
            '.py': PythonTranslator,
            '.cpp': CPPTranslator
        }

    def get_translator(self, filename, ext):
        try:
            if ext is None:
                filename, ext = os.path.splitext(filename)
            return self.translators[ext]
        except KeyError as e:
            print("[-] Error occurred")
