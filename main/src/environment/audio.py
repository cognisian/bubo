"""
Model the physical environment and translate to and from the
Virtual Universe Machine

"""

import asyncio

import numpy as np

import alsaaudio as alsa


class Audio:
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
        if 'sample_rate' in init_conds.keys():
            sample_rate = init_conds.sample_rate

        if 'num_samples' in init_conds.keys():
            num_samples = init_conds.num_samples

        if 'sample_data_size' in init_conds.keys():
            sample_data_size = init_conds.sample_data_size

        if 'internal_data_size' in init_conds.keys():
            internal_data_size = init_conds.internal_data_size

        return AudioCapture(rate=sample_rate, frame_buffer_size=num_samples,
                            in_data_format=translate[sample_data_size.name],
                            buf_data_format=internal_data_size)

    @staticmethod
    def createPlayback(init_conds):
        if 'sample_rate' in init_conds.keys():
            sample_rate = init_conds.sample_rate

        if 'num_samples' in init_conds.keys():
            num_samples = init_conds.num_samples

        if 'sample_data_size' in init_conds.keys():
            sample_data_size = init_conds.sample_data_size

        if 'internal_data_size' in init_conds.keys():
            internal_data_size = init_conds.internal_data_size

        return AudioPlayback(rate=sample_rate, frame_buffer_size=num_samples,
                             input_type=translate[sample_data_size.name],
                             intern_type=internal_data_size)

    """ Constructor.

    Set the data types which will impact how frequently the audio card will
    respond.  The time the card takes to return will determine the period (T)
    used in analysis of the signal
    """
    def __init__(self, in_data_format=alsa.PCM_FORMAT_S16_LE,
                 buf_data_format=np.float16):

        # Set the data that is fixed, when changing the __alsa_format, the
        # __format_type MUST also change accordingly
        self._alsa_format = alsa.PCM_FORMAT_S16_LE
        self._format_type = np.int16
        self._internal_type = np.float16
        self._bytes_frame = np.dtype(self.__format_type).itemsize

    """
    Normalize the audio samples from an array of integers into an array of
    floats (-1, 1) with unity level.
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

    def __init__(self, rate=44100, channels=1, period=1024,
                 in_data_format=alsa.PCM_FORMAT_S16_LE,
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
        self._period_size = self._frame_size * period

        self._initialize()

    def _initialize(self):
        """ Setup capture parameters. """

        self._device = alsa.PCM(type=alsa.PCM_CAPTURE, mode=alsa.PCM_ASYNC)
        self._device.setchannels(self._channels)
        self._device.setrate(self._rate)
        self._device.setformat(self._alsa_format)
        self._device.setperiodsize(self._period_size)

    @asyncio.coroutine
    def read(self):
        _, data = capture.read()
        yield from np.fromstring(data, dtype=self._format_type)


class AudioPlayback(Audio):
    """ Create an concrete instance of the Audio, specific to audio
    playback.
    """

    def __init__(self, rate=44100, channels=1, period=1024):
        """
        Create and initialize the playback audio buffer
        """

        super().__init__(in_data_format, buf_data_format)

        # Set the ALSA properties
        self._rate = rate
        self._channels = channels
        self._frame_size = self._bytes_frame * channels
        self._period_size = self._frame_size * period

        self._recording = False

        self._initialize()

    def _initialize(self):
        """
        Initialize write queue to avoid buffer underrun.
        """

        self._device = alsa.PCM(type=alsa.PCM_PLAYBACK, mode=alsa.PCM_ASYNC)

        self._device.setchannels(self._channels)
        self._device.setrate(self._rate)
        self._device.setformat(self._alsa_format)
        self._device.setperiodsize(self._period_size)

        self._recording = True

    @asyncio.coroutine
    def write(self, data):
        """
        Writes audio to an ALSA audio device from the write queue.
        Supposed to run in its own process.

        data - nparray of data to write
        """
        yield from self._device.write(data.tostring())