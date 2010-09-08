import sys
import os
import re
import copy

from datetime import datetime,date

from task import Task, Project

from task_parser_generator import TaskParserGenerator
from command_parser import CommandParser

tool_name = "dodo"
_todo_file = os.path.join(os.getenv('HOME'), '.dodo', 'todo')
_archive_tmpl = os.path.join(os.getenv('HOME'), '.dodo', 'archive')
_version_file = os.path.join(os.path.dirname(__file__), '.version')

class TodoError(Exception):
    """
    Error raised in Todo class
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Todo:
    """
    Contains commands for handling list of tasks.

    Commands returns list of tasks if changes were made, otherwise
    None.
    """

    # ( help, command, options, ... )
    cmds = (
        ( 'List tasks', 'ls', '[@PROJECT]' ),
        ( 'Add new task', 'add', '[@PROJECT]', 'DESC' ),
        ( 'Remove task', 'rm', 'INDEX | @PROJECT' ),
        ( 'Change priority of a task', 'pri', 'INDEX | @PROJECT', 'PRIORITY' ),
        ( 'Add deadline to a task', 'dl', 'INDEX | @PROJECT', 'DATE' ),
        ( 'Do a task', 'do', 'INDEX | @PROJECT' ),
        ( 'Archive old tasks', 'archive' ),
        ( 'Print program version', 'version' ),
        ( 'Show projects', 'projects' ),
        ( 'Show help', 'help' ),
        )

    class TodoCommands():
        def __init__(self, tasks, last_index):
            self.tasks = tasks
            self.last_index = last_index

        def __find_task_or_project(self, tasks, what):
            if what.startswith('@'):
                for task in tasks:
                    if isinstance(task, Project) and task.name == what[1:]:
                        return task

            else:
                what = int(what)
                for task in tasks:
                    if isinstance(task, Project):
                        for project_task in task.tasks:
                            if project_task.index == what:
                                return project_task
                    elif task.index == what:
                        return task

            return None

        def ls(self, args):
            if not self.tasks:
                return

            # list project
            if len(args) > 0 and args[0].startswith('@'):
                project = self.__find_task_or_project(self.tasks, args[0])
                if project:
                    print(project.get_pretty())

            # list tasks and projects matching re
            elif len(args) > 0:
                m = re.compile('.*{0}.*'.format(' '.join(args)))
                for task in self.tasks:
                    p = task.get_pretty(m)
                    if p: print p

            # list everything
            else:
                for task in self.tasks:
                    print('{0}'.format(task.get_pretty()))

        def projects(self, args):
            if not self.tasks:
                return

            for task in self.tasks:
                if isinstance(task, Project):
                    print('{0}'.format(task.get_pretty_name()))

        def add(self, args):
            if len(args) < 1:
                raise TodoError('insufficient arguments')

            # handle project
            if args[0].startswith('@'):
                if len(args) < 2:
                    raise TodoError('insufficient arguments')

                task = self.__find_task_or_project(self.tasks, args[0])

                if task:
                    task.append(Task(self.last_index, ' '.join(args[1:])))
                    return True

                else:
                    project = Project(args[0][1:])
                    project.append(Task(self.last_index, ' '.join(args[1:])))

                    self.tasks.append(project)
                    self.last_index += 1

                    return True

            # handle task
            else:
                self.tasks.append(Task(self.last_index, ' '.join(args)))
                self.last_index += 1

                return True

        def rm(self, args):
            if len(args) < 1:
                raise TodoError('insufficient arguments')

            if args[0].startswith('@'):
                task = self.__find_task_or_project(self.tasks, args[0])
                if task:
                    self.tasks.remove(task)
                    return True

            else:
                index = int(args[0])

                for task in self.tasks:
                    if isinstance(task, Project):
                        for project_task in task.tasks:
                            if project_task.index == index:
                                task.tasks.remove(project_task)
                                if len(task.tasks) == 0:
                                    self.tasks.remove(task)
                                return True

                    elif task.index == index:
                        self.tasks.remove(task)
                        return True

            raise TodoError("index or project not found: {0}".format(args[0]))

        def dl(self, args):
            if len(args) < 2:
                raise TodoError('insufficient arguments')

            first_arg = args[0]
            deadline = args[1]

            try:
                deadline = datetime.strptime(
                    deadline,
                    '%Y-%m-%d').date()
            except ValueError as e:
                raise TodoError('incorrect date given: {0}'.format(e))

            task = self.__find_task_or_project(self.tasks, first_arg)
            if task:
                if isinstance(task, Project):
                    for project_task in task.tasks:
                        project_task.deadline = deadline

                else:
                    task.deadline = deadline

                return True

        def pri(self, args):
            if len(args) < 2:
                raise TodoError('insufficient arguments')

            first_arg = args[0]
            new_pri = args[1].upper()

            if new_pri not in Task.priorities:
                raise TodoError('given priority not expected')

            task = self.__find_task_or_project(self.tasks, first_arg)
            if task:
                if isinstance(task, Project):
                    for project_task in task.tasks:
                        project_task.pri = new_pri

                else:
                    task.pri = new_pri

                return True

        def do(self, args):
            if len(args) < 1:
                raise TodoError('insufficient arguments')

            first_arg = args[0]

            task = self.__find_task_or_project(self.tasks, first_arg)
            if task:
                if isinstance(task, Project):
                    for project_task in task.tasks:
                        project_task.pri = Task.task_done
                        project_task.done = date.today()

                else:
                    task.pri = Task.task_done
                    task.done = date.today()

                return True

        def archive(self, args):
            archived = []
            project = None

            for task in self.tasks:
                if isinstance(task, Project):
                    archived_project = None
                    archived_tasks = task.get_done()
                    if archived_tasks:
                        archived_project = Project(task.name,
                                                   archived_tasks)
                        archived.append(archived_project)

                elif task.done:
                    archived.append(task)
                    self.tasks.remove(task)

            if archived:
                date = datetime.now().isoformat()
                name = _archive_tmpl + '_' + date

                with file(name, 'w') as f: pass

                parserGenerator = TaskParserGenerator(name)
                parserGenerator.generate(archived)

                return True

        def help(self, args):
            print('usage: {0} [COMMAND] [OPTS]'.format(tool_name))

            cmd_width = max(map(len, [cmd[1] for cmd in Todo.cmds]))
            opt_width = max(map(len, [' '.join(cmd[2:]) for cmd in Todo.cmds]))

            for cmd in Todo.cmds:
                print(
                    '  {0:<{cmd_width}}{1:<{opt_width}}{2}'.format(
                        cmd[1],
                        ' '.join(cmd[2:]),
                        cmd[0],
                        cmd_width = cmd_width + 5,
                        opt_width = opt_width + 5,
                        )
                    )

            sys.exit(0)

        def version(self, args):
            with file(_version_file, 'r') as fobj:
                print fobj.read()

    def __init__(self, args):
        if not os.path.exists(os.path.dirname(_todo_file)):
            os.mkdir(os.path.dirname(_todo_file))

        if not os.path.exists(_todo_file):
            with file(_todo_file, 'w') as f: pass

        try:
            parserGenerator = TaskParserGenerator(_todo_file)
            tasks, last_index = parserGenerator.parse()

            commandParser = CommandParser([ cmd[1] for cmd in Todo.cmds ])
            command, args_left = commandParser.parse(args)

            changes = getattr(Todo.TodoCommands(tasks, last_index),
                              command)(args_left)

            if changes:
                parserGenerator.generate(tasks)

        except (TodoError, IOError, ValueError) as err:
            print('error: {0}'.format(err))
