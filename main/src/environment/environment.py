"""
Model the physical environment and translate to and from the
Virtual Universe Machine

"""


import alsaaudio as alsa
import numpy as np

from queue import Queue
from threading import Thread


class Audio:
    """
    A class implementing buffered audio I/O
    """

    DEBUG = False

    """
    Initialize the audio buffer as signed 16bit LE int with defaults:

    A frame is the size (in bytes) of one sample on one channel.  The
    frame_size is the total size (in bytes) of all the frames for each channel
    (sample data type size (int16) * num of channels)
    A period is the number of frames read/write per hardware cycle.  The
    period_size should be the total number of bytes in one period
    (frame_size * period)

    This class sets the sample data type as a signed 16bit integer (2 bytes)
    little endian encoded

    rate 44.1KHz sample frequency
    channels 1 mono
    period 1024 (# of frames per read/write chunk)
    """
    def __init__(self, rate=44100, channels=1, period=1024):

        # Set the data that is fixed, when changing the __alsa_format, the
        # __format_type MUST also change accordingly
        self.__alsa_format = alsa.PCM_FORMAT_S16_LE
        self.__format_type = np.int16
        self.__internal_type = np.float16
        self.__bytes_frame = np.dtype(self.__format_type).itemsize

        # Set the ALSA properties
        self._rate = rate
        self._channels = channels
        self._frame_size = self.__bytes_frame * channels
        self._period_size = self._frame_size * period

        self.__running = True
        self._read_process = Thread(target=self.__read,
                                    name='Audio Read thread')
        self._write_process = Thread(target=self.__write,
                                     name='Audio Write thread')

        # Set up our buffers
        self._read_queue = Queue()
        self._write_queue = Queue()

    """
    Reads audio from an ALSA audio device into the read queue.
    Supposed to run in its own process.
    """
    def __read(self):
        capture = alsa.PCM(type=alsa.PCM_CAPTURE, mode=alsa.PCM_NORMAL)

        capture.setchannels(self._channels)
        capture.setrate(self._rate)
        capture.setformat(self.__alsa_format)
        capture.setperiodsize(self._period_size)

        while self.__running:
            _, data = capture.read()
            amp = np.fromstring(data, dtype=self.__format_type)
            self._read_queue.put(amp.normalize())

    """
    Writes audio to an ALSA audio device from the write queue.
    Supposed to run in its own process.
    """
    def __write(self):
        playback = alsa.PCM(type=alsa.PCM_PLAYBACK, mode=alsa.PCM_NORMAL)

        playback.setchannels(self._channels)
        playback.setrate(self._rate)
        playback.setformat(self.__alsa_format)
        playback.setperiodsize(self._period_size)

        while self.__running:
            data = self._write_queue.get()
            result = playback.write(data.tostring(self.denormalize()))

    """
    Iitialize write queue to avoid buffer underrun.
    """
    def _initialize(self):
        zeros = np.zeros(self._period_size, dtype=self.__format_type)

        # Initialize 4 entire periods of bytes
        for i in range(0, 4):
            self._write_queue.put(zeros)

    """
    Runs the read and write processes.
    """
    def run(self):
        self._initialize()

        self._read_process.start()
        self._write_process.start()

    """
    Runs the read and write processes.
    """
    def stop(self):
        self.__running = False

    """
    Reads audio samples from the queue captured from the reading thread.

    Returns: a ndata array normalized to float (-1,1)
    """
    def read(self):
        return self._read_queue.get()

    """
    Writes audio samples to the queue to be played by the writing thread.
    """
    def write(self, data):
        # if type of data is ndarray, and dtype matchs self.__format_type
        self._write_queue.put(data)

    """
    Normalize the audio samples from an array of integers into an array of
    floats (-1, 1) with unity level.
    """
    def normalize(self, data):
        temp = np.zeros(shape=data.shape, dtype=self.__internal_type)
        dt_info = np.iinfo(self.__format_type)
        # ratio of float(-1,1) to integers
        bias = 2 / (dt_info.max - dt_info.min)
        # bias = (dt_info.max - dt_info.min) / 2.
        np.put(temp, np.arange(data.size),
               np.clip(
                       [(item * bias) for item in data], -1, 1))

        return temp

    """
    Denormalize the data from an array of floats (-1,1) into an
    array of integers.
    """
    def denormalize(self, data):
        temp = np.zeros(shape=data.shape, dtype=self.__format_type)
        dt_type = np.iinfo(self.__format_type)
        # ratio of integers to float(-1,1)
        bias = (dt_type.max - dt_type.min) / 2.
        np.put(temp, np.arange(data.size),
               np.clip(
                   [int((item * bias) + 0.5) for item in data],
                   dt_type.min, dt_type.max))

        for i in temp[:5]:
            print("DENORM %d" % i)
        return temp


audio = Audio()
audio.run()

reads = 60
curr_reads = 0
while True:
    print("SAMPLE: %d" % (curr_reads + 1))

    data = audio.read()
    audio.write(data)

    curr_reads += 1
    if curr_reads >= reads:
        break

audio.stop()
