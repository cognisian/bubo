""" The Univere

This is the class which provides the interface of the artifical world with the
events occurring on the hardware platform.
Implements the event loop
"""

import asyncio

import from environment import Audio


class Universe:
    """ The Universe class to hold and manage the event loop,
    constructbuild the necessary I/O queues

    loop - the event loop to run
    init_conds - the initial coonditions
    """
    def __init__(self, loop, init_conds):
        self._loop = loop
        self._init_cond = frozenset((k, v) for k, v in init_conds.items())
        print(self._init_cond)

    def run(self):
        """ Gods method. """

        self._big_bang()
        self._inflation()
        self._rolling()

    def _big_bang(self):
        print('bang')

        (capture, playback) = self._init_conds['audio_devices']

        capture_env = capture[1]
        self._capture = Audio(capture_env['rate'], capture_env['channels'],
                              capture_env['periods'])

    def _inflation(self):
        print('boom')
        pass

    def _rolling(self):
        # And we are off
        try:
            print('now we are off to the races')
            self._loop.run_until_complete(self._life())
        finally:
            self._loop.close()

    @asyncio.coroutine
    def _life(self):
        """ The event loop. """
        print("there was still nothing, but at least you could see it")
        pass

    def _create_audio(self):
        pass

    def _create_video(self):
        pass

    def _create_network(self):
        pass
