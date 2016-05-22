import numpy as np

import networkx as nx


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

    def action(self, delta):
        print('action from %s' % delta)

    def adjust(self):
        print('adjusting self output in terms of feedback')


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
