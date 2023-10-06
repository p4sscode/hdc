# Dependencies

import numpy as np
import functools as ft
import networkx as nx


# Basic arithemitic operations

def hdv(d):
    return np.random.choice([-1, 1], d)


def bind(xs):
    return ft.reduce(lambda x, y: x * y, xs)


def bundle(xs):
    return ft.reduce(lambda x, y: x + y, xs)


def similarity(A, B):
    return np.dot(A, B) / len(A)


def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)

    if norm_A == 0 or norm_B == 0:
        return 0

    return dot_product / (norm_A * norm_B)


# Memory

class ItemMemory:
    def __init__(self, vectors=[]):
        self.vectors = vectors

    def addVector(self, label, V):
        self.vectors.append((label, V))

    def cleanup(self, V):
        return max(self.vectors, key=lambda x: cosine_similarity(V, x[1]))


# Graph pre-processing

def processDataset(dataset):
    graphs = []
    labels = []

    for graph in dataset:
        G = nx.Graph()
        G.add_edges_from(zip(graph["edge_index"][0], graph["edge_index"][1]))
        graphs.append(G)
        labels.append(graph["y"][0])

    return (graphs, labels)

def transform(X, alpha, digits):
    graphs = []
    for graph in X:
        gpr = nx.pagerank(graph, alpha)
        nodes = dict()
        for key, value in gpr.items():
            nodes[key] = str(round(value, digits))
        H = nx.relabel_nodes(graph, nodes)
        graphs.append(H)
    return graphs