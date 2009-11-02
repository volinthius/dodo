from nose.tools import raises
import sys
sys.path.append('../lib/dodo')
from command_parser import CommandParser

cmds = [ 'run', 'walk', 'crawl' ]

args = [ 'tired', 'drunk', 'toddler' ]

def test_known_command():
    parser = CommandParser(cmds)
    result_cmd, result_args = parser.parse([cmds[0]] + args)
    assert result_cmd == cmds[0]
    assert result_args == args

@raises(ValueError)
def test_unknown_command():
    parser = CommandParser(cmds)
    cmd, _ = parser.parse(['greet'] + args)
