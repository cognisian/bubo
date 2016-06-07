""" The Univere

This is the class which provides the interface of the artifical world with the
events occurring on the hardware platform.
Implements the event loop
"""

import asyncio

import pycuda.driver as cuda
import pycuda.autoinit

from environment.audio import Audio
from environment.compute import Compute


class Universe(object):
    """ The Universe class to hold and manage the event loop,
    construct the communication ports to manage I/O for:
        + timer
        + CPU <-> HW (input signal)
        + CPU <-> GPU calculations and data streaming

    init_conds - the initial coonditions
    """
    def __init__(self, init_conds):

        self.energy = None

        self._init_cond = init_conds

        self._capture = None
        self._playback = None

        self._computes = []

        self._big_bang()
        self._inflation()

    def _big_bang(self):
        print('bang')

        self.energy = self._init_cond['initial_energy']
        print('we have %d to spend' % self.energy)

        # PLUGIN STRUCTURE HERE
        self._create_time()
        self._create_audio()
        self._create_video()

    def _inflation(self):
        print('boom')

        self.energy -= 100
        for devicenum in range(cuda.Device.count()):
            self._computes.append(Compute(devicenum))

    def _get_energy(self):
        """ Decrement and retrieve the current energy level. """
        self.energy -= self._init_cond['planck_quantum']
        if not self.energy > 1:
            print('bust')
            self.energy = 0

        return self.energy

    def _create_audio(self):
        self._capture = Audio.createCapture(self._init_cond)
        self._playback = Audio.createPlayback(self._init_cond)

    def _create_video(self):
        pass

    def _create_network(self):
        pass

    @asyncio.coroutine
    def life(self):
        """ The event loop. """
        print("there was still nothing, but at least you could see it")

        while self._get_energy():
            # Get current timestamp
            # Read input sources
            data = yield from self._capture.read()

    def big_crunch(self):
        print('ka-blammo!')
        pass
