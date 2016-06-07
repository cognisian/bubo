"""
Model the audio physical environment and translate to and from the
Virtual Universe Machine

"""
import math
import asyncio

import numpy as np

import alsaaudio as alsa

# import enviornment as env


class Audio(object):
    """
    A class implementing buffered audio I/O.

    A frame is the size (in bytes) of one sample on one channel.  The
    frame_size is the total size (in bytes) of all the frames for each channel
    (sample data type size (int16) * num of channels)
    A period is the number of frames read/write per hardware cycle.  The
    period_size should be the total number of bytes in one period
    (frame_size * period)
    """

    """ Translate NumPY dtypes to ALSA sizes. """
    translate = {
        'int16': alsa.PCM_FORMAT_S16_LE,
        'uint16': alsa.PCM_FORMAT_U16_LE,
        'int32': alsa.PCM_FORMAT_S32_LE,
        'uint32': alsa.PCM_FORMAT_U32_LE
    }

    @staticmethod
    def createCapture(init_conds):
        sample_rate = init_conds['sample_rate']
        num_samples = init_conds['num_samples']
        samp_data_sz = init_conds['sample_data_size']
        internal_data_size = init_conds['internal_data_size']

        return AudioCapture(rate=sample_rate, frame_buffer_size=num_samples,
                            in_data_format=samp_data_sz,
                            buf_data_format=internal_data_size)

    @staticmethod
    def createPlayback(init_conds):
        sample_rate = init_conds['sample_rate']
        num_samples = init_conds['num_samples']
        samp_data_sz = init_conds['sample_data_size']
        internal_data_size = init_conds['internal_data_size']

        return AudioPlayback(rate=sample_rate, frame_buffer_size=num_samples,
                             in_data_format=samp_data_sz,
                             buf_data_format=internal_data_size)

    def __init__(self, sample_type=np.int16, intern_type=np.float16):
        """ Constructor.

        Set the data types which will impact how frequently the audio card will
        respond.  The time the card takes to return will determine the
        period (T) used in analysis of the signal

        sample_type - np.dtype The data type to return samples in
        intern_type - np.dtype The data type to do analysis in
        """

        # Set the data that is fixed, when changing the __alsa_format, the
        # __format_type MUST also change accordingly
        self._format_type = sample_type
        self._internal_type = intern_type
        self._alsa_format = Audio.translate[np.dtype(sample_type).name]
        self._bytes_frame = np.dtype(self._format_type).itemsize

    def speed_of_audio(self, temp):
        """ Returns the speed of sound in air at 1atm based on the current
        energy (temperature) of the environment

        return speed is in meters per second
        """
        return 20.05 * math.sqrt(temp + 273.15)

    """
    Normalize the audio samples from an array of integers into an array of
    floats (-1, 1).
    """
    def normalize(self, data):
        temp = np.zeros(shape=data.shape, dtype=self._internal_type)
        dt_info = np.iinfo(self._format_type)
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
        temp = np.zeros(shape=data.shape, dtype=self._format_type)
        dt_type = np.iinfo(self._format_type)
        # ratio of integers to float(-1,1)
        bias = (dt_type.max - dt_type.min) / 2.
        np.put(temp, np.arange(data.size),
               np.clip(
                   [int((item * bias) + 0.5) for item in data],
                   dt_type.min, dt_type.max))

        return temp


class AudioCapture(Audio):
    """ Create an concrete instance of the Audio, specific to audio
    capture.
    """

    def __init__(self, rate=44100, channels=1, frame_buffer_size=1024,
                 in_data_format=np.int16,
                 buf_data_format=np.float16):
        """
        A frame is the size (in bytes) of one sample on one channel.  The
        frame_size is the total size (in bytes) of all the frames for each
        channel (sample data type size (int16) * num of channels)
        A period is the number of frames read/write per hardware cycle.  The
        period_size should be the total number of bytes in one period
        (frame_size * period)


        rate 44.1KHz sample frequency
        channels 1 mono
        period 1024 (# of frames per read/write chunk)
        """

        super().__init__(in_data_format, buf_data_format)

        # Set the ALSA properties
        self._rate = rate
        self._channels = channels
        self._frame_size = self._bytes_frame * channels
        self._period_size = frame_buffer_size

        self._buffer_shape = (channels, self._period_size)
        self._device = None

    def on_load(self):
        """ Setup capture parameters. """

        self._device = alsa.PCM(type=alsa.PCM_CAPTURE, mode=alsa.PCM_ASYNC)
        self._device.setchannels(self._channels)
        self._device.setrate(self._rate)
        self._device.setformat(self._alsa_format)
        self._device.setperiodsize(self._period_size)

    # @asyncio.coroutine
    def read(self):
        """ Read one period of frame data. """
        reading = True
        while reading:
            elems, data = self._device.read()
            if elems > 0:
                reading = False

        return self.normalize(np.fromstring(data, dtype=self._format_type).
                              reshape(self._buffer_shape))


class AudioPlayback(Audio):
    """ Create an concrete instance of the Audio, specific to audio
    playback.
    """

    def __init__(self, rate=44100, channels=1, frame_buffer_size=1024,
                 in_data_format=np.int16,
                 buf_data_format=np.float16):
        """
        Create and initialize the playback audio buffer
        """

        super().__init__(in_data_format, buf_data_format)

        # Set the ALSA properties
        self._rate = rate
        self._channels = channels
        self._frame_size = self._bytes_frame * channels
        self._period_size = self._frame_size * frame_buffer_size

        self._buffer_shape = (channels, frame_buffer_size)

        self._initialize()

    def _initialize(self):
        """
        Initialize ALSA device for PCM_PLAYBACK and PCM_ASYNC.
        """

        self._device = alsa.PCM(type=alsa.PCM_PLAYBACK, mode=alsa.PCM_ASYNC)

        self._device.setchannels(self._channels)
        self._device.setrate(self._rate)
        self._device.setformat(self._alsa_format)
        self._device.setperiodsize(self._period_size)

    # Write buffers
    @asyncio.coroutine
    def write(self, data):
        """
        Writes audio to an ALSA audio device from the write queue.
        Supposed to run in its own process.

        data - nparray of data to write
        """
        yield from self._device.write(self.denormalize(data).tostring())
