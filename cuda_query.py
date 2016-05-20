import numpy as np

import networkx as nx

import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation as anim
matplotlib.use("Gtk3Agg")

print("PyCUDA %s" % pycuda.VERSION_TEXT)

for devicenum in range(cuda.Device.count()):
    device = cuda.Device(devicenum)

    compute = device.compute_capability()
    print("PyCUDA Compute %d.%d" % (compute[0], compute[1]))

    print("=== Compute Attributes for CUDA device %d \n" % devicenum)
    print(" " * 3, "%s: %d" % ('CLOCK_RATE', device.clock_rate))
    print(" " * 3, "%s: %d" % ('CONCURRENT_KERNELS',
                               device.concurrent_kernels))
    print(" " * 3, "%s: %d" % ('MANAGED_MEMORY', device.managed_memory))
    print(" " * 3, "%s: %d" % ('TOTAL_MEMORY', device.total_memory()))
    print(" " * 3, "%s: %d" % ('TOTAL_CONSTANT_MEMORY',
                               device.total_constant_memory))

    print(" " * 3, "%s: %d" % ('STREAM_PRIORITIES_SUPPORTED',
                               device.stream_priorities_supported))

    print(" " * 3, "%s: %d" % ('MAX_GRID_DIM_X', int(device.max_grid_dim_x)))
    print(" " * 3, "%s: %d" % ('MAX_GRID_DIM_Y', int(device.max_grid_dim_y)))
    print(" " * 3, "%s: %d" % ('MAX_GRID_DIM_Z', int(device.max_grid_dim_z)))

    print(" " * 3, "%s: %d" % ('MULTIPROCESSOR_COUNT',
                               device.multiprocessor_count))
    print(" " * 3, "%s: %d" % ('MAX_THREADS_PER_MULTIPROCESSOR',
                               device.max_threads_per_multiprocessor))
    print(" " * 3, "%s: %d" % ('MAX_SHARED_MEMORY_PER_MULTIPROCESSOR',
                               device.max_shared_memory_per_multiprocessor))
    print(" " * 3, "%s: %d" % ('MAX_REGISTERS_PER_MULTIPROCESSOR',
                               device.max_registers_per_multiprocessor))

    print(" " * 3, "%s: %d" % ('MAX_THREADS_PER_BLOCK',
                               device.max_threads_per_block))
    print(" " * 3, "%s: %d" % ('MAX_REGISTERS_PER_BLOCK',
                               device.max_registers_per_block))
    print(" " * 3, "%s: %d" % ('MAX_BLOCK_DIM_X', int(device.max_block_dim_x)))
    print(" " * 3, "%s: %d" % ('MAX_BLOCK_DIM_Y', int(device.max_block_dim_y)))
    print(" " * 3, "%s: %d" % ('MAX_BLOCK_DIM_Z', int(device.max_block_dim_z)))

    print(" " * 3, "%s: %d" % ('WARP_SIZE', int(device.warp_size)))
    maxWarps = ((device.max_threads_per_block + device.warp_size - 1) //
                device.warp_size)

    print(" " * 3, "%s: %d" % ('MAX_WARPS_PER_BLOCK', maxWarps))

membraneResist = 1
thresholdV = 0.3
recoverRatio = 1.12
current = 0.66
temp = np.sqrt((thresholdV + 1)**2 - (3 * thresholdV))


def recovery(v):
    return recoverRatio * v


def recovery_func(array):
    return [recovery(elem) for elem in array]


def excitation(v):

    v1 = 1/3.0 * (thresholdV + 1 - temp)
    v2 = 1/3.0 * (thresholdV + 1 + temp)

    cool1 = (-1 * v1 * (thresholdV - v1) * (1 - v1)) + current
    cool2 = (-1 * v2 * (thresholdV - v2) * (1 - v2)) + current

    result = 0
    if v <= 0:
        result = 0
    elif v <= v1:
        result = -1 * (cool1 / v1) * v
        # print("v (%d) <= v1 (%d)" % (v, v1))
    elif v <= v2:
        result = (((cool2 - cool1) / (v2 - v1)) * (v - v1)) + cool1
        # print("v (%d) <= v2 (%d)" % (v, v2))
    elif v >= 1:
        result = (-1 * cool2 / (1 - v2)) * (v - v2)
        # print("v (%d) > v2 (%d)" % (v, v2))

    return result


def excitation_func(array):
    return [excitation(elem) for elem in array]

# First set up the figure, the axis, and the plot element we want to animate
# x = np.linspace(0.0, 1.0, num=50)
# y = np.linspace(0.0, 1.0, num=50)
# plt.plot(x, recovery_func(x))
# plt.plot(y, excitation_func(y))
# plt.show()


class PreSynaptic:
    'Presynaptic Model'

    MAX_RELEASE = 5
    MIN_RELEASE = 2
    MAX_READY = 10
    MIN_READY = 5

    ready = MIN_READY
    ready_tail = ready

    release = MIN_RELEASE

    target = (ready - release) / 2

    refresh_rate = 1

    def __init__(self):
        print('Presynaptic Model')

    def __str__(self):
        return '<presynapse %s>' % id(self)

    def __repr__(self):
        return '<presynapse %s>' % id(self)

    def input(self, signal):
        print('received signal of %d ' % signal)
        print('extracting feeddback signal')

    def output(self):
        print('sent signal of %d ' % release)
        return release

    def update(self):
        print('updating')

    def adjust(self):
        print('adjusting output in terms of feedback')


class PostSynaptic:

    def __init__(self):
        print('PostSynaptic Model')

    def __str__(self):
        return '<postsynapse %s>' % id(self)

    def __repr__(self):
        return '<postsynapse %s>' % id(self)

    def input(self, signal):
        print('received signal of %d ' % signal)
        print('extracting feeddback signal')

    def output(self):
        print('sent signal')
        return 1

    def update(self):
        print('updating')

    def adjust(self):
        print('adjusting output in terms of feedback')


synaptic_graph = nx.DiGraph(name='synaptic connections')

presyn1 = PreSynaptic()
presyn2 = PreSynaptic()
presyn3 = PreSynaptic()
synaptic_graph.add_node(presyn1)
synaptic_graph.add_node(presyn2)
synaptic_graph.add_node(presyn3)

postsyn1 = PostSynaptic()
postsyn2 = PostSynaptic()
postsyn3 = PostSynaptic()
synaptic_graph.add_node(postsyn1)
synaptic_graph.add_node(postsyn2)
synaptic_graph.add_node(postsyn3)

synaptic_graph.add_edge(presyn1, postsyn1)
synaptic_graph.add_edge(presyn2, postsyn2)
synaptic_graph.add_edge(presyn3, postsyn3)
synaptic_graph.add_edge(postsyn1, presyn1)
synaptic_graph.add_edge(postsyn2, presyn2)
synaptic_graph.add_edge(postsyn3, presyn3)

print(synaptic_graph.edges())
