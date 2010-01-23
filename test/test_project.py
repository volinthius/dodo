import sys

sys.path.append('../lib/dodo')

from task import Project, Task

def test_sort():
    task0 = Task(0, 'test-desc-0', 'A')
    task1 = Task(0, 'test-desc-1', 'B')
    task2 = Task(0, 'test-desc-2', 'C')

    project = Project('test-project')
    project.append(task2)
    project.append(task1)
    project.append(task0)

    assert project.tasks[0] == task2
    assert project.tasks[1] == task1
    assert project.tasks[2] == task0

    project.sort_tasks()

    assert project.tasks[0] == task0
    assert project.tasks[1] == task1
    assert project.tasks[2] == task2
