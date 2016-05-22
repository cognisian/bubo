""" Create and initialize resources and returns an running
Universe Virtual Machine

In the begining:
God created 0
nothing, formless and empty
Then God said, "let there not be nothing"
And then there was 1
something, at least
God saw that 1 was good
Then God said, "if 1 is good, then 10 is better"
God blessed the 0 and the 1
And God said to them, "Here are DeMorgans Laws,
I give you dominion over them.
Go forth and multiple"
And God beheld this stack, and it was very good
And on the last instruction God forked, his only begotten daemon
And God said, "Only through my daemon, can a 0 or 1 come"
And 10 begat 00 which begat 01 which begat 11
which begat 011 which 010 which begat 110
which begat 101 which begat 100 which begat 000
which begat 001
Recursively
And God saw that the begatting, over and over
had begotten into a mess
Everywhere Entropy was increasing,
information was less and less
And God saw that to all things and end must come
Then God said, "goto: In the beginning"
"""

import os
import signal
import functools
import numpy as np

import asyncio

import pycuda.driver as cuda
import pycuda.autoinit

import universe


# Create the event loop and add hooks for the ap
loop = asyncio.get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(getattr(signal, signame),
                            functools.partial(apocalypse, signame))

# Gotta start with something
initial_conditions = {
    'version': 1
    'num_devices': cuda.Device.count()
    'clock_rate': 1000
    'random': np.random
    'devices': []
}


# Being
def let_there_be_not_nothing():
    """ This is where all the magic happens, the Logos

    From the set of initial conditions, create and initialize the universe
    """

    for devicenum in range(cuda.Device.count()):
        device = cuda.Device(devicenum)

        compute = device.compute_capability()
        device_props['compute'] = "%d.%d" % (compute[0], compute[1])

        maxWarps = ((device.max_threads_per_block + device.warp_size - 1) //
                    device.warp_size)
        device['max_warps_per_block'] = maxWarps

        initial_conditions.devices[devicenum] = device


# Nothingness
def apocalypse(signame):
    """ The End Times. """

    print("The END is NIGH for universe %s" % os.getpid())
    print("Apocalypse by %s signal" % signame)
    loop.stop()

# Gotta start somewhere
if '__name__' eq '__main__':
    universe = let_there_be_not_nothing()
    if universe is not None:
        universe.run()
