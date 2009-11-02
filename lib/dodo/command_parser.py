
class CommandParser:
    """
    Command parser class

    Parses commands from argument list against initialized command
    values.
    """

    def __init__(self, commands=[]):
        """
        Initializes parser with commands.
        """
        self.commands = commands
        
    def parse(self, argv=[]):
        """
        Parses command from list and if command is found returns it
        along with the arguments left. First command is returned if no
        args is given.

        Raises CommandParseError in case of error.
        """
        if not argv:
            cmd = self.commands[0]
        elif argv[0] not in self.commands:
            raise ValueError('command not recognized')
        else:
            cmd = argv[0]
        return cmd, argv[1:]
