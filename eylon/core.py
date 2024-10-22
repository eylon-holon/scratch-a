import builtins
import datetime
import inspect

from eylon.utils import *
from eylon.post import post
from eylon.classwork import ClassWork
from config import cfg


work = None


###################################

def print(*args, **kwargs):
    if work != None:
        work.print(*args, **kwargs)
    builtins.print(*args, **kwargs)

def input(prompt):
    answer = work.input() if work != None else None
    if (answer == None):
        answer = builtins.input(prompt)
    return answer


###################################

def test_submission(func, input, expected):
    with work.capture_io(input):
        func()
    return expected

def post_results(fname, src, input, output, expected):
    request = {
        'now': datetime.datetime.now().isoformat(),
        'docId': cfg.docId,
        'branch': work.branch,
        'lesson': work.lesson,
        'fname': fname,
        'src': src,
        'input': "\n".join(input),
        'output': "\n".join(output),
        'expected': "\n".join(expected),
        'tags': ' '.join(cfg.tags)
    }
    response = post(cfg.api, request)
    return response["msg"]


###################################

def start(desc):
    global work
    notebook = get_notebook_name_from_stack()
    work = ClassWork(notebook, desc)
    post_results("Here😁", "", [], [], [])
    print("Let's start 🙌, those are waiting 🛠️: ", ','.join(map(lambda f: f"'{fname(f)}'", desc.keys())))

    
def submit(func, input):
    fn = fname(func)
    if work == None:
        print("Please, start the class first")
        return
    if fn not in work.desc:
        print(f"function '{fn}' is not part of this lesson")
        return
    src = inspect.getsource(func)
    expected = work.desc[fn][1]
    output = test_submission(func, input, expected)
    if output == None:
        print(f"Your work has errors. Please, fix and submit again.")
        return
    msg = post_results(func.__name__, src, input, output, expected)
    print(msg)

###################################

def get_next_class():
    pass

