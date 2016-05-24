""" Create and initialize resources and returns a running
Virtual Universe Machine

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
-------------------------------------------------------------------------------
Is that true?
I know this one is true
and this too is true
It is true that is this one
and that is this too
If this one is that and this too is that
then
that is true.
only when this one is this too!
so when is that true?
that one is that
that will be that too
that one was true
but that too could be either
is neither this one nor that
not this too
That was true, that too is not true
now that that too is not true

So when will that be true?
-------------------------------------------------------------------------------
So God is the cybernetic knowledge of this system, he creates the symbols, and
the rules to manipulate those symbols.  But God does not learn, God is not
intelligence because there is no feedback loop, no adaptability.  Input comes
in, God does what God does, and an output is generated (stochastic result
returned based on a Probability Distribution Function).  God does not answer
prayers, he answers questions.

A question is a measurement.  A probe.  A question is also relative.  "Why am I
here?" could be answered, validly, in numerous ways: "to lead a good life"; 42,
etc.  And you would spend millions of years figuring out what the hell the
answer means.  A better question, "What is the probabilty that the purpose of
my life is to start a green enterprise?"  Of course this is much easier to
calculate, there is a frame of reference and the answer is not absolute; it is
relative between myself and everything else (frame of reference) and the answer
is only valid within that frame of reference (ie the probability that my
destiny is to start a Green Company may be small while someone else asking same
question could get a higher probabilty).  In addition, the question is
decomposable.  I can look for data based on probability of starting any
business, probability of anyone starting green business, my views on green
tech, etc.  So getting data and then mapping it relative to a frame of
reference, is a Me_Operator multipled by a world PDF to return a Me_PDF.  Then
build the me_Question operator (function) multiply it by the Me_PDF and you
have your answer.  Like the slit experiment it is a signal filter but to limit
the calculations.
Everything is a quanta, God takes one sample of spacetime (x,y,z,t) within
each sample of space time are 2 functions: sigma(x) for position; sigma(rho)
for momentum
"""

import os
import signal
import functools

import numpy as np

import psutil as ps
import asyncio

import pycuda.driver as cuda
import pycuda.autoinit

from universe import Universe

# Gotta start with something
initial_conditions = {
    'debug': True,
    'version': 1,
    'host': '127.0.0.1'
    'port': 5556,
    'clock_rate': 1000,
    'random': np.random,
    'num_cpu': ps.cpu_count(),
    'memory': ps.virtual_memory().available,
    'num_devices': cuda.Device.count(),
    'devices': [],
}

# Create the event loop
loop = asyncio.get_event_loop()

#
# EXTRACTION methods
#


def extract_local_env():
    """ Extract properties from the local/OS environemnt

    So this is the device on which we launch the universe
    """
    pass


# Extract compute env
def extract_compute_env():
    """ Extract properties from the compute environemnt

    In this case we are currently tying this to a CUDA architecture.
    TODO: Abstract this to an OpenCL interface
    """

    # Extract the computing environment
    for devicenum in range(cuda.Device.count()):
        device = cuda.Device(devicenum)

        compute = device.compute_capability()
        device_props['compute'] = "%d.%d" % (compute[0], compute[1])

        maxWarps = ((device.max_threads_per_block + device.warp_size - 1) //
                    device.warp_size)
        device['max_warps_per_block'] = maxWarps

        initial_conditions.devices[devicenum] = device


def extract_audio_env():
    """ Extract properties from the audio hardware environment. """
    pass


def extract_video_env():
    """ Extract properties from the video hardware environment. """
    pass


def extract_network_env():
    """ Extract properties from the network environemnt. """
    pass


#
# EXISTENTIAL mmethods
#


# Being
def let_there_be_not_nothing():
    """ This is where all the magic happens, the Logos

    From the set of initial conditions, create and initialize the universe
    """

    # Hook up God's Wrath
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(apocalypse, signame))

    # Get the engine properties
    extract_local_env()
    extract_compute_env()
    extract_audio_env()
    extract_video_env()
    extract_network_env()

    # now we are cooking with gas, boyo
    return Universe(loop, initial_conditions)


# Nothingness
def apocalypse(signame):
    """ The End Times. """

    print("The END is NIGH for universe %s" % os.getpid())
    print("Apocalypse by %s signal" % signame)
    loop.stop()

# Gotta start somewhere
if '__name__' == '__main__':
    universe = let_there_be_not_nothing()
    if universe is not None:
        universe.run()
