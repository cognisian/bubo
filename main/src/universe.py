""" The Univere

This is the class which provides the interface of the artifical world with the
events occurring on the hardware platform.
Implements the event loop
"""


class Universe:
    """ The Universe class to hold and manage the event loop,
    constructbuild the necessary I/O queues

    loop - the event loop to run
    init_conds - the initial coonditions
    """
    def __init__(self, loop, init_conds):
        self._loop = loop
        self._init_cond = frozenset((k, v) for k, v in init_conds.items())

    def run():
        """ Gods method. """

        self._big_bang()
        self._inflation()

        self._and_action()

    def _big_bang(self):
        pass

    def _inflation(self):
        pass

    def _and_action(self):
        # And we are off
        try:
            self._loop.run_until_complete(self._life())
        finally:
            self._loop.close()

    @asyncio.coroutine
    def _life(self):
        """ The event loop. """
        pass
