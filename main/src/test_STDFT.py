import math
import numpy as np
from scipy import signal as sg

from environment.audio import Audio

initial_conditions = {
    'debug': True,
    'version': 1,
    'host': '127.0.0.1',
    'random': np.random.random,
    'sample_rate': 8000,
    'num_samples': 1024,
    'sample_data_size': np.int16,
    'internal_data_size': np.float16,
    'planck_quantum': 6.626 * 10**-2,  # Energy per sec
    'initial_energy': float(2 ** (np.dtype(np.int16).itemsize * 8)),
    'environments': ['Time', 'AudioCapture'],
}

capture = Audio.createCapture(initial_conditions)
playback = Audio.createPlayback(initial_conditions)


def freq(energy):
    pass


def main():
    samp_period = float(initial_conditions['num_samples'] /
                        initial_conditions['sample_rate'])
    samp_time = samp_period / initial_conditions['num_samples']
    print('Sample period=%f' % samp_period)
    print('Time per sample=%f' % samp_time)

    capture.on_load()

    # Get 1 sample of audio data
    data = capture.read()
    print("Size %d" % data.size)

    # Because we have normalized the data, the data becomes a normal
    # distibution with E[X] = 0 and variance = sum(X[n]**2)/N which
    # so variance can b e interpreted as the average power or energy per period
    instant_power = np.asarray([x**2.0 for x in np.nditer(data)])
    avg_power = np.sum(instant_power) / (2 * initial_conditions['num_samples'])
    sample_energy = avg_power * samp_period
    print("Avg Power %f" % avg_power)
    print("Energy of sample %f" % sample_energy)
    # The energy delivered over the entire sample, this is the initial energy
    # deivered at t0. At t0 the highest frequency will have the highest energy.
    # If the energy of the first frame (amp**2) is less than the theortical
    # energy of the energy barrier at t1 then no freq component.  If greater
    # then the actual amount of energy of the amp is substraced from
    # energy_samp
    energy_buckets = [(sample_energy / (2. * i)) for i in range(1, 1024)]

    # From physical properties of ear wavelength = 4L L length of cochlea
    velocity = capture.speed_of_audio(25.)

if __name__ == '__main__':
    main()
