import os

from task import Task, Project

__version__ = 1

class TaskParserGenerator:
    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        tasks = []
        index = 0

        with file(self.file_name) as f:
            project = None
            first_line = True

            for line in f.readlines():
                if first_line:
                    first_line = False
                    if not line.startswith('$version 1'):
                        raise ValueError('incorrect version in todo file')

                elif line.strip() == '' or line.startswith('#'):
                    continue

                elif line.startswith('@'):
                    if project: tasks.append(project)
                    project = Project(line[1:].strip())

                else:
                    (pri, dl, done, desc) = line.split(' ', 3)

                    # projectless tasks
                    if not project:
                        index += 1
                        tasks.append(Task(index, desc, pri,
                                          dl if dl != '-' else None,
                                          done if done != '-' else None))

                    # tasks in projects
                    else:
                        index += 1
                        project.append(Task(index, desc, pri,
                                            dl if dl != '-' else None,
                                            done if done != '-' else None))

            if project: tasks.append(project)

        return tasks, index

    def generate(self, tasks):
        tmp_file = self.file_name + '.tmp'

        with file(tmp_file, 'w') as fobj:
            fobj.write('$version {0}\n'.format(__version__))

            for task in tasks:
                if isinstance(task, Task):
                    fobj.write('{0} {1} {2} {3}\n'.format(
                            task.pri,
                            task.deadline or '-',
                            task.done or '-',
                            task.desc
                            ))

            for task in tasks:
                if isinstance(task, Project):
                    task.sort_tasks()
                    fobj.write('@{0}\n'.format(task.name))
                    for project_task in task.tasks:
                        fobj.write('{0} {1} {2} {3}\n'.format(
                                project_task.pri,
                                project_task.deadline or '-',
                                project_task.done or '-',
                                project_task.desc
                                ))

        os.remove(self.file_name)
        os.rename(tmp_file, self.file_name)
