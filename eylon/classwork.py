import io
from eylon.utils import *

class ClassWork:
    def __init__(self, notebook, desc):
        self.notebook = notebook
        self.lesson = notebook.split('.')[0]
        self.branch = get_current_branch()
        self.desc = {fname(f): io for f, io in desc.items()}

        self._print_buf = []
        self._print_on = False
        self._input_buf = []
        self._input_at = 0

    def capture_io(self, inBuf):
        self._input_buf = inBuf
        return self
    
    def __enter__(self):
        self._print_buf = []
        self._print_on = True
        self._input_at = 0
        pass

    def __exit__(self, *args):
        self._print_on = False
        self._input_buf = []
        self._input_at = 0
        pass

    def print(self, *args, **kwargs):
        if not self._print_on:
            return
        with io.StringIO() as buf:
            print(*args, file=buf, **kwargs)
            self._print_buf.append(buf.getvalue())

    def input(self):
        if self._input_at >= len(self._input_buf):
            return None
        answer = self._input_buf[self._input_at]
        self._input_at += 1
        return answer

    def get_prints(self):
        return self._print_buf
