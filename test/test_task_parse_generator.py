import nose
import inspect
import sys
import os
import shutil

from datetime import date

sys.path.append('../lib/dodo')

from task import Task, Project
from task_parser_generator import TaskParserGenerator
from termcap import Termcap
from helpers import mktmpdir, want_exception

todo_content_simple = ( "$version 1",
                        "A - - test-task-1",
                        "A - - test-task-2" )

todo_content_complex = ( "$version 1",
                         "A - - test-task-1",
                         "B - - test-task-2",
                         "@test-project-1",
                         "B - - test-task-3",
                         "B - - test-task-4",
                         "@test-project-2",
                         "C - - test-task-5" )

term = Termcap()

def test_done_task_str():
    task = Task(1, 'test-task', 'A', str(date.today()), str(date.today()))
    want = '  {1}1: test-task ={0} >{0}{2}'.format(
        str(date.today()),
        term.black,
        term.reset)
    assert task.get_pretty() == want

def test_undone_task_str():
    task = Task(1, 'test-task', 'A', str(date.today()))
    want = '  {1}1: test-task >{0}{2}'.format(
        str(date.today()),
        term.white,
        term.reset)
    assert task.get_pretty() == want

def test_project_add_task_str():
    task = Task(1, 'test-task', 'A', str(date.today()))
    project = Project('test-project')
    project.append(task)
    want = '{3}@test-project{1}\n  {0}1: test-task >{2}{1}'.format(
        term.white,
        term.reset,
        str(date.today()),
        term.yellow
        )
    assert project.get_pretty() == want

def test_project_add_many_task_str():
    task1 = Task(1, 'test-task1', 'A', str(date.today()))
    task2 = Task(2, 'test-task2', 'B', str(date.today()))
    project = Project('test-project')
    project.append(task1)
    project.append(task2)
    want = '{3}@test-project{1}\n  {0}1: test-task1 >{2}{1}\n  {4}2: test-task2 >{2}{1}'.format(
        term.white,
        term.reset,
        str(date.today()),
        term.yellow,
        term.green
        )
    print project.get_pretty()
    print want
    assert project.get_pretty() == want

def run_through_task_parse_generator(todo_file):
    taskparsergenerator = TaskParserGenerator(todo_file)
    return taskparsegenerator.parse()

def test_task_parser_generator_contents():
    for content in (todo_content_simple,
                    todo_content_complex):
        yield check_content, content

def check_content(content):
    tmpdir = mktmpdir()
    todo_file = os.path.join(tmpdir, 'todo')
    with file(todo_file, 'w') as f:
        f.write('\n'.join(content))
    
    tasks, _ = TaskParserGenerator(todo_file).parse()

    with file(todo_file) as f:
        want = '\n'.join(content)
        result = f.read()
        assert want == result

def test_task_parser_missing_version():
    tmpdir = mktmpdir()
    todo_file = os.path.join(tmpdir, 'todo')
    with file(todo_file, 'w') as f:
        f.write('\n'.join(todo_content_complex[1:]))

    taskparsergenerator = TaskParserGenerator(todo_file)
    with want_exception(
        ValueError('incorrect version in todo file')
        ):
        tasks, _ = taskparsergenerator.parse()
