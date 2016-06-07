""""
Provides the signal environment

This is designed to be a plugin based system
"""


class EnvObject(object):
    """ Provide the interface of objects wishing to register themselves as an
    environmental object. """

    def on_load(self):
        pass

    def on_reload(self):
        pass

    def on_unload(self):
        pass

    def input(self, signal):
        """ The input signal from the environment to this object.  This is a
        callback in response to this object submitting a measurement request.

        signal - The response from the measure request
        """
        pass

    def output(self):
        """ The input signal from the environment to this object.  This is a
        callback in response to this object submitting a measurement request.

        signal - The response from the measure request
        """
        pass


class Signal(object):
    """ Provides the abstraction of a signal.

    More concretely, it wraps a NumPy array containing the samples of one
    period from an async signal source.  This array will be the memory that is
    transfered between host and device depending on CUDA memory model.
    """

    def __init__(self, sample):
        """ Wrap the numpy array. """
        pass


class Environment(object):
    """ Implements the Environment.

    Simply, the environment is just a list of current signals (and operations
    to add, remove, combine and propigate signals).
    """

    def __init__(self, init_conds):
        """ Construct the environment. """
        self.envs = set()
        pass

    def measure(self):
        """ Get a sample from the underlying hardware. """
        pass

    def action(self, signal):
        """ Update the environment to include new signal. """
        pass

    def _load_environment(self):

        for root, dirs, files in os.walk('.'):
            candidates = [fname for fname in files if fname.endswith('.py') and
                          not fname.startswith('__')]
        classList = []
        if candidates:
            for c in candidates:
                modname = os.path.splitext(c)[0]
                try:
                    module = __import__(modname)
                except (ImportError, NotImplementedError):
                    continue
                for cls in dir(module):
                    cls = getattr(module, cls)
                    if (inspect.isclass(cls) and
                        inspect.getmodule(cls) == module and
                            issubclass(cls, base)):
                        # print('found in {f}: {c}'.format(
                        # f=module.__name__,c=cls))
                        classList.append(cls)
        print(classList)
