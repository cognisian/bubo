""" The Univere

This is the class which provides the interface of the artifical world with the
events occurring on the hardware platform.
Implements the event loop
"""


class Universe:
    """ The Universe class to hold and manage the event loop,
    constructbuild the necessary I/O queues
    """
    def __init__(self):
        pass

    def run(loop):
        """ Gods method. """

        self._big_bang()
        self._inflation()

        self._and_life()

    def _big_bang(self):
        pass

    def _inflation(self):
        pass

    def _and_life(self):
        # And we are off
        try:
            loop.run_forever()
        finally:
            loop.close()


@asyncio.coroutine
def slow_operation():
    # yield from suspends execution until
    # there's some result from asyncio.sleep
    yield from asyncio.sleep(1)

    # our task is done, here's the result
    return 'Future is done!'


def got_result(future):
    print(future.result())
