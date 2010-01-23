import sys

sys.path.append('../lib/dodo')

from task import Task, compare_tasks

def run_comparison(task0, task1, result):
    assert compare_tasks(task0, task1) == result

def test_compare_pri():
    task0 = Task(0, 'test-desc-0', 'A')
    task1 = Task(0, 'test-desc-1', 'B')
    yield run_comparison, task0, task1, -1
    
    task0 = Task(0, 'test-desc-0', 'B')
    task1 = Task(0, 'test-desc-1', 'B')
    yield run_comparison, task0, task1, 0

    task0 = Task(0, 'test-desc-0', 'C')
    task1 = Task(0, 'test-desc-1', 'B')
    yield run_comparison, task0, task1, 1

    task0 = Task(0, 'test-desc-0', 'A', '2009-10-10', '2009-10-11')
    task1 = Task(0, 'test-desc-1', 'B')
    yield run_comparison, task0, task1, 1

    task0 = Task(0, 'test-desc-0', 'A')
    task1 = Task(0, 'test-desc-1', 'B', '2009-10-10', '2009-10-12')
    yield run_comparison, task0, task1, -1

    task0 = Task(0, 'test-desc-0', 'A', '2009-10-10', '2009-10-11')
    task1 = Task(0, 'test-desc-1', 'B', '2009-10-10', '2009-10-12')
    yield run_comparison, task0, task1, -1
