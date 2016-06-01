"""
Model the GPU compute interface between the host's input capture device buffer
and the GPU memory and kernel execution
"""

import asyncio

import numpy as np

import pycuda.driver as cuda
import pycuda.autoinit


class Compute:
    """ Interface around the CPU <-> GPU communications. """

    # Constants to define what memory steps to issue to transfer memory
    # to and from the host and device
    MEMORY_MODEL_UNMANAGED = 0
    MEMORY_MODEL_MANAGED = 1

    def __init__(self, devicenum=0):
        """ Initialize the underlying CUDA device. """

        self.device = cuda.Device(devicenum)
        compute = self.device.compute_capability()
        print("PyCUDA Compute %d.%d" % (compute[0], compute[1]))

        temp = (self.device.max_threads_per_block + self.device.warp_size - 1)
        self.max_warps = temp // self.device.warp_size

        # Initialize our Grid dimenstions (pending blocks)
        self.grid_dim = ()
        # Initialize thread blocks (pending execution based on warp size
        self.block_dim = ()

        # Default memory model is for us to explicitly transfer to and from
        # the host and device
        self._memory_model = Compute.MEMORY_MODEL_UNMANAGED

        # Check CUDA version compatability
        # CUDA v6.0 includes new Unified Memory model which reduces explicit
        # data movement commands between host and device
        # And Dynamic Parallelism in which kernel func can schedule another
        # thread block
        cuda_ver = cuda.VERSION
        if cuda_ver[0] >= 6:
            self._memory_model = Compute.MEMORY_MODEL_MANAGED
