import builtins
import datetime
import inspect
import json

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

def test_submission(func, args):
    input = args[2]
    expected = args[3]
    hasArgs = func.__code__.co_argcount > 0
    failed = False
    
    with work.capture_io(input):
        ret = func(*args[0]) if hasArgs else func()

    if len(args[1]) > 0:
        if ret != args[1][0]:
            print(f"failed for {args[0]}: expected={args[1][0]} got={ret}")
            failed = True

    output = work.get_prints()
    for exp in expected:
        found = False
        for line in output:
            if exp in line:
                found = True
                break
        if not found:
            print(f"'{exp}' is not found in output lines")
            print("---------------------------------------------------")
            for line in output:
                print(line.strip())
            print("---------------------------------------------------")
            failed = True

    if failed:
        return None

    return [ret, output]


def post_results(fname, src, log):
    api = "https://script.google.com/macros/s/AKfycbyLLStYfln3HEJdRNq_-xzc1ZAx8QD0TLFd9rSqVbv05zd2jK5WSg0uAo5NvtzLFQC2tw/exec"
    request = {
        'now': datetime.datetime.now().isoformat(),
        'docId': cfg.docId,
        'branch': work.branch,
        'lesson': work.lesson,
        'fname': fname,
        'src': src,
        'log': log,
        'tags': ' '.join(cfg.tags)
    }
    response = post(api, request)
    return response["msg"]


###################################

def start(desc):
    global work
    notebook = get_notebook_name_from_stack()
    work = ClassWork(notebook, desc)
    post_results("Here😁", "", "")
    print(f"Hi {work.branch} 😁! Let's start the lesson... 🙌")

    
def submit(func):
    fn = fname(func)
    if work == None:
        print("Please, start the class first")
        return
    if fn not in work.desc:
        print(f"function '{fn}' is not part of this lesson")
        return
    src = inspect.getsource(func)

    failed = False
    lines = []
    for args in work.desc[fn]:
        output = test_submission(func, args)
        failed |= output == None
        lines.append(json.dumps(args))
        lines.append(json.dumps(output))

    if failed:
        print(f"Your work has errors. Please, fix and submit again.")
        return

    log = json.dumps(lines, indent=2)
    msg = post_results(func.__name__, src, log)
    print(msg)


def missing(lesson, people):
    now = datetime.datetime.now().isoformat()
    for stu in people:
        request = {
            'now': now,
            'docId': cfg.docId,
            'branch': stu,
            'lesson': lesson,
            'fname': "",
            'src': "",
            'log': "",
            'tags': ' '.join(cfg.tags)
        }
        post(cfg.api, request)


###################################

def store_all_changes_to_github():
    os_cmd("git add -A")
    os_cmd('git commit -m "auto commit..."')
    os_cmd("git push")


def get_next_lesson():
    os_cmd("git pull origin main --no-ff --no-edit && git push")

