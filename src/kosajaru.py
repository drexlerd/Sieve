from collections import defaultdict


class Node:
    def __init__(self, state_id):
        self.state_id = state_id
        self.visited = False
        self.scc = None

class Kosajaru:
    """ https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
    """
    def compute_sccs(self, state_ids, forward_graph, backward_graph):
        # Initialize
        l = []
        nodes = dict()
        for state_id in state_ids:
            nodes[state_id] = Node(state_id)
        # Forward traversal phase
        for state_id in state_ids:
            self._visit(nodes[state_id], nodes, forward_graph, l)
        # Post-order traversal phase
        scc = 0
        for state_id in reversed(l):
            node = root = nodes[state_id]
            scc = self._assign(node, root, nodes, backward_graph, scc)
        sccs = [[] for _ in range(scc)]
        for node in nodes.values():
            sccs[node.scc].append(node.state_id)
        return sccs


    def _visit(self, node, nodes, forward_graph, l):
        if node.visited:
            return
        node.visited = True
        for edge in forward_graph[node.state_id]:
            self._visit(nodes[edge.target_id], nodes, forward_graph, l)
        # post order
        l.append(node.state_id)

    def _assign(self, node, root, nodes, backward_graph, scc):
        if node.scc is not None:
            return scc
        if (root.state_id == node.state_id):
            root.scc = scc
            scc += 1
        node.scc = root.scc
        for edge in backward_graph[node.state_id]:
            scc = self._assign(nodes[edge.source_id], root, nodes, backward_graph, scc)
        return scc
