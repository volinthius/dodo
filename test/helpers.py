import inspect
import os
import shutil
import sys

class want_exception:
    def __init__(self, exception):
        assert isinstance(exception, Exception)
        self._wanted_exception = exception.__class__
        self._wanted_expression = str(exception)

    def __enter__(self):
        sys.exc_clear()

    def __exit__(self, type, value, traceback):
        assert type is not None, 'wanted exception {0}'.format(self._wanted_exception.__name__)
        return isinstance(value, self._wanted_exception) and self._wanted_expression == str(value)

def mktmpdir():
    """Create and return temporary directory

    Temporary directory is created in the directory by the calling
    module. Directory is named by the concatenating 'tmp', calling
    module and calling function.

    In case the directory already exists it is deleted and
    recreated."""
    dir = os.path.dirname(inspect.stack()[1][1])
    curfile = os.path.basename(inspect.stack()[1][1])
    function = inspect.stack()[1][3]
    tmpdir = os.path.join(
        dir,
        'tmp',
        os.path.splitext(curfile)[0] + ':' + function
        )
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir)
    return tmpdir
