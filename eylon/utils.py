import os
import traceback

from git import Repo


def fname(f):
    return f"{f.__name__}()"

def get_notebook_name(str):
    suffixAt = str.find(".ipynb")
    if suffixAt == -1: return -1
    return str[:suffixAt:].split('/')[-1]

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

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printAt(y, x, str):
    print(f'\x1b[{y};{x}H{str}')

