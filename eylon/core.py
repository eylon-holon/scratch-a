import builtins
import datetime
import inspect
import os
import traceback
from git import Repo

from eylon.post import post
from config import cfg


###################################

def fname(f):
    return f"{f.__name__}()"

def get_notebook_name(str):
    suffixAt = str.find(".ipynb")
    if suffixAt == -1: return -1
    return str[:suffixAt+6:].split('/')[-1]

def get_notebook_name_from_stack():
    for trace, _ in traceback.walk_stack(None):
        cellId = trace.f_locals.get('cell_id', -1)
        if cellId == -1: continue
        name = get_notebook_name(cellId)
        if name != -1: return name
    return 'unknown'

def get_current_branch():
    repo = Repo(os.getcwd())
    branch = repo.active_branch
    return branch.name

###################################

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printAt(y, x, str):
    builtins.print(f'\x1b[{y};{x}H{str}')

def print(*args, **kwargs):
    builtins.print("==>", *args, **kwargs)

def input(msg):
    return builtins.input(msg)

###################################

class ClassWork:
    def __init__(self, notebook, desc):
        self.notebook = notebook
        self.lesson = notebook.split('.')[0]
        self.branch = get_current_branch()
        self.desc = {fname(f): io for f, io in desc.items()}


work = None

###################################

def test_submission(func, input):
    return True

def post_results(func, input, output):
    request = {
        'now': datetime.datetime.now().isoformat(),
        'docId': cfg.docId,
        'branch': work.branch,
        'lesson': work.lesson,
        'fname': func.__name__,
        'src': inspect.getsource(func),
        'input': "\n".join(input),
        'output': "\n".join(output),
        'tags': ' '.join(cfg.tags)
    }
    response = post(cfg.api, request)
    return response["msg"]

###################################

def start_class(desc):
    global work
    notebook = get_notebook_name_from_stack()
    work = ClassWork(notebook, desc)
    print("You have started class in", notebook)
    print("Please implement the following funcitons:", ','.join(map(lambda f: f"'{fname(f)}'", desc.keys())))

    
def submit(func, input):
    fn = fname(func)
    if work == None:
        print("Please, start the class first")
        return
    if fn not in work.desc:
        print(f"function '{fn}' is not part of the class work")
        return
    src = inspect.getsource(func)
    file = get_notebook_name_from_stack()
    if not test_submission(func, input):
        print(f"Your work has errors. Please, fix and submit again.")
        return
    msg = post_results(func, input, ["no-output-yet"])
    print(msg)

###################################

def get_next_class():
    pass

