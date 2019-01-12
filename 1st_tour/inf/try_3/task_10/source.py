from collections import defaultdict
import sys
import random
import re
import string

def dfs(graph, root, p_inv=1, visited=None, leaves=None):
    visited = set() if visited is None else visited
    leaves = {} if leaves is None else leaves

    visited.add(root)
    children = graph[root]
    if len(children) == 0:
        leaves[root] = p_inv
    for child in children - visited:
        dfs(graph, child, p_inv * len(children), visited, leaves)

    return leaves


def solve():
    dataset = sys.stdin.read()
    edges = [tuple(int(v) for v in edge.split()) for edge in dataset.splitlines()[1:]]

    graph = defaultdict(set)
    for src, dst in edges:
        graph[src].add(dst)

    probs = dfs(graph, 0)
    return print('\n'.join('{}: {}'.format(v, '1' if probs[v] == 1 else '1/{}'.format(probs[v])) for v in sorted(probs.keys())))