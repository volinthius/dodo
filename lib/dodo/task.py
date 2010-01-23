import os

from datetime import datetime,date

from termcap import Termcap

term = Termcap()

def compare_tasks(task_a, task_b):
    if task_a.done and not task_b.done:
        return 1
    elif not task_a.done and task_b.done:
        return -1

    if task_a.pri > task_b.pri:
        return 1
    elif task_a.pri == task_b.pri:
        return 0
    else:
        return -1

class Task:
    priorities = ( 'A', 'B', 'C' )
    task_done = 'x'
    default_priority = priorities[-1]
    capital_a_index = 65

    color_priorities = [ term.white, term.green, term.magenta ]
    color_done = term.black
    color_reset = term.reset
    color_late = term.red

    def __init__(self,
                 index,
                 desc,
                 pri=default_priority,
                 deadline=None,
                 done=None):
        self.index = index
        self.desc = desc.strip()
        self.pri = pri

        self.deadline = deadline and datetime.strptime(
            deadline, '%Y-%m-%d').date()

        self.done = done and datetime.strptime(
            done, '%Y-%m-%d').date()

    def colorize(self, string):
        color = ''

        if self.deadline and self.deadline <= date.today():
            color = Task.color_late

        elif self.pri == Task.task_done:
            color = Task.color_done

        else:
            color = Task.color_priorities[ord(self.pri) - Task.capital_a_index]

        return color + string + Task.color_reset

    def get_pretty(self, regex=None):
        if regex and not regex.match(self.desc):
            return

        string = '  {0}: {1}'.format(self.index, self.desc)

        if self.done:
            string += ' ={0}'.format(self.done)
        if self.deadline:
            string += ' >{0}'.format(self.deadline)

        return self.colorize(string)

class Project:
    color_project = term.yellow
    color_reset = term.reset

    def __init__(self, name, tasks=None):
        self.name = name
        self.tasks = tasks or []

    def append(self, task):
        self.tasks.append(task)

    def colorize(self, string):
        return '{0}{1}{2}'.format(Project.color_project,
                                  string,
                                  Project.color_reset)

    def get_pretty_name(self):
        return self.colorize('@{0}'.format(self.name))

    def get_pretty(self, regex=None):
        found = False
        string = ''

        if regex and regex.match(self.name):
            found = True
            regex = None

        for task in self.tasks:
            if regex and not regex.match(task.desc):
                continue
            found = True
            string += '{0}\n'.format(task.get_pretty(regex))

        if string:
            string = string[:-1] # remove linefeed
            return '{0}\n{1}'.format(self.get_pretty_name(), string)

    def get_done(self, remove=False):
        done = []

        for task in self.tasks:
            if task.done:
                done.append(task)
                if remove:
                    self.tasks.remove(task)

        return done

    def sort_tasks(self, field='pri'):
        self.tasks.sort(compare_tasks)
