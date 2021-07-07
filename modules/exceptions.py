from discord.ext.commands import CommandError

class ClassroomError(Exception):
    pass

class EmptyQueue(Exception):
    """Cannot skip because queue is empty"""


class NotConnectedToVoice(Exception):
    """Cannot create the player because bot is not connected to voice"""


class NotPlaying(Exception):
    """Cannot <do something> because nothing is being played"""

class GuildExceptions(CommandError):

    handled = True

    def __init__(self, handled=None):
        self.handled = handled or self.handled


class NotEnoughPointsError(GuildExceptions):

    pass


class RoleNotFoundError(GuildExceptions):

    pass


class FunctionIsInescapable(GuildExceptions):

    ...


#all custom errors will be defined here