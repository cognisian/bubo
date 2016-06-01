""" Create and initialize resources and returns a running Virtual Universe
Machine

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
decomposable.  I can obtain a measurement/data based on probability of starting
any business, probability of anyone starting green business, my views on green
tech, etc.  So getting data and then mapping it relative to a frame of
reference, is a Me_Operator multipled by a world PDF to return a Me_PDF.  Then
build the me_Question operator (function) multiply it by the Me_PDF and you
have your answer.  Like the slit experiment it is a signal filter but to limit
the calculations.
Everything is a quanta, God takes one sample of spacetime (x,y,z,t) within
each sample of space time are 2 functions: sigma(x) for position; sigma(rho)
for momentum
"""
import numpy as np

import signal
import os
import asyncio
import psutil as ps
import functools

from universe import Universe

# Create the event loop
loop = asyncio.get_event_loop()

# Gotta start with something
initial_conditions = {
    'debug': True,
    'version': 1,
    'host': '127.0.0.1',
    'random': np.random.random,
    'num_cpu': ps.cpu_count(),
    'memory': ps.virtual_memory().available,
    'sample_rate': 44100,
    'num_samples': 1024,
    'sample_data_size': np.int16,
    'internal_data_size': np.float16,
    'initial_energy': 512 * (2 ** np.dtype(np.int16).itemsize),
}


def apocalypse(signame, universe):
    """ Nothingness. The End Times. """

    # TEAR IT ALL DOWN
    print("The END is NIGH for God %s" % os.getpid())
    print("Apocalypse by %s signal" % signame)

    universe.big_crunch()

    # And done
    if not loop.is_running():
        loop.stop()

    if not loop.is_closed():
        loop.close()


# Being in of itself
def main():

    # Hook up God's Wrath
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(apocalypse, signame))

    print("in the beginning")

    # now we are cooking with gas, boyo
    universe = Universe(initial_conditions)
    if universe is not None:
        try:
            # And we are off
            print('official race start time %d' % loop.time())
            loop.run_until_complete(universe.life())
        finally:
            print('and that is all he wrote')
            apocalypse('SIGGOD', universe)


# Gotta start somewhere
if __name__ == '__main__':
    main()
