""" The Univere

This is the class which provides the interface of the artifical world with the
events occurring on the hardware platform.
Implements the event loop
"""

import asyncio

from environment.audio import Audio


class Universe:
    """ The Universe class to hold and manage the event loop,
    constructbuild the necessary I/O queues

    loop - the event loop to run
    init_conds - the initial coonditions
    """
    def __init__(self, loop, init_conds):
        self._loop = loop
        self._init_cond = init_conds

    def run(self):
        """ Gods method. """

        self._big_bang()
        self._inflation()
        self._rolling()

    def _big_bang(self):
        print('bang')

        self._create_audio

    def _inflation(self):
        print('boom')
        pass

    def _rolling(self):
        # And we are off
        try:
            print('now we are off to the races')
            self._loop.run_until_complete(self._life())
        finally:
            print('and that is all he wrote')
            self._loop.close()

    @asyncio.coroutine
    def _life(self):
        """ The event loop. """
        print("there was still nothing, but at least you could see it")

        # Get current timestamp
        # Read input sources

        # Write ouput
        # update timestamp
        pass

    #
    # Processing methods
    #
    @asyncio.coroutine
    def _read_audio(self):
        pass

    @asyncio.coroutine
    def _write_audio(self):
        pass
    #
    # Creation methods
    #

    def _create_audio(self):
        self._capture = Audio.createCapture(self._init_cond)
        self._playback = Audio.createPlayback(self._init_cond)

    def _create_video(self):
        pass

    def _create_network(self):
        pass
