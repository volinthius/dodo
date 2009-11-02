import sys
import os
import cStringIO

from nose.tools import with_setup
from nose.plugins.skip import SkipTest

sys.path.append('../lib/dodo')

from todo import Todo
from task_parser_generator import TaskParserGenerator

from helpers import mktmpdir, want_exception

todo_content_simple = ( "$version 1",
                        "A - - test-task-1",
                        "B - - test-task-2" )

todo_content_complex = ( "$version 1",
                         "A - - test-task-1",
                         "B - - test-task-2",
                         "@test-project-1",
                         "C - - test-task-3",
                         "A - - test-task-4",
                         "@test-project-2",
                         "B - - test-task-5" )

def setup():
    pass

def teardown():
    pass

@with_setup(setup, teardown)
def test_todo_ls():
    tmp = mktmpdir()

    todo_file = os.path.join(tmp, 'todo')
    with file(todo_file, 'w') as f:
        f.write('\n'.join(todo_content_complex))

    tasks, last_index = TaskParserGenerator(todo_file).parse()
    todo = Todo.TodoCommands(tasks, last_index)

    output = cStringIO.StringIO()
    saveout = sys.stdout
    sys.stdout = output
    todo.ls('')

    result = output.getvalue()
    sys.stdout = saveout
    
    want = """  1: test-task-1
  2: test-task-2
@test-project-1
  3: test-task-3
  4: test-task-4
@test-project-2
  5: test-task-5
"""

    assert want == result
    output.close()

def test_todo_ls_project():
    tmp = mktmpdir()

    todo_file = os.path.join(tmp, 'todo')
    with file(todo_file, 'w') as f:
        f.write('\n'.join(todo_content_complex))

    tasks, last_index = TaskParserGenerator(todo_file).parse()
    todo = Todo.TodoCommands(tasks, last_index)

    output = cStringIO.StringIO()
    saveout = sys.stdout
    sys.stdout = output
    todo.ls(['@test-project-1', ])

    result = output.getvalue()
    sys.stdout = saveout
    
    want = """@test-project-1
  3: test-task-3
  4: test-task-4
"""

    assert want == result
    output.close()

@with_setup(setup, teardown)
def test_todo_pri():
    raise SkipTest()

@with_setup(setup, teardown)
def test_todo_rm():
    raise SkipTest()

@with_setup(setup, teardown)
def test_todo_archive():
    raise SkipTest()

@with_setup(setup, teardown)
def test_todo_help():
    raise SkipTest()

@with_setup(setup, teardown)
def test_todo_add():
    raise SkipTest()

@with_setup(setup, teardown)
def test_todo_dl():
    raise SkipTest()

@with_setup(setup, teardown)
def test_todo_do():
    raise SkipTest()
