
class Node:
    def __init__(self, state_id):
        self.state_id = state_id
        self.visited = False
        self.scc = None

class Kosajaru:
    """ https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
    """
    def compute_sccs(self, state_ids, adj_list):
        # Initialize
        l = []
        nodes = [Node(state_id) for state_id in state_ids]
        # Forward traversal phase
        for state_id in state_ids:
            self._visit(nodes[state_id], nodes, adj_list, l)
        # Post-order traversal phase
        scc = 0
        for state_id in reversed(l):
            node = root = nodes[l[state_id]]
            scc = self._assign(node, root, nodes, adj_list, scc)
        sccs = [[] for _ in range(scc)]
        for node in nodes:
            sccs[node.scc].append(node.state_id)
        return sccs


    def _visit(self, node, nodes, adj_list, l):
        if node.visited:
            return
        node.visited = True
        for edge in adj_list[node.state_id]:
            self._visit(nodes[edge.target_id], nodes, adj_list, l)
        # post order
        l.append(node.state_id)

    def _assign(self, node, root, nodes, adj_list, scc):
        if node.scc is not None:
            return scc
        if (root.state_id == node.state_id):
            root.scc = scc
            scc += 1
        node.scc = root.scc
        for edge in adj_list[node.state_id]:
            scc = self._assign(nodes[edge.target_id], root, nodes, adj_list, scc)
        return scc
