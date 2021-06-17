from collections import defaultdict
from .kosajaru import Kosajaru


class Edge:
    def __init__(self, source_id, target_id, rule):
        self.source_id = source_id
        self.target_id = target_id
        self.rule = rule


class State:
    def __init__(self, features, index_vec):
        self.features = features
        self.index_vec = index_vec
        self.index_set = set(index_vec)

    def __str__(self):
        return str([str(self.features.get_feature_by_index(i)) for i in self.index_vec])


class PolicyGraph:
    def __init__(self, features, rules):
        self.num_features = len(features.features)
        self.num_states = 2 ** self.num_features

        # add an edge between each state pair for which there exists a compatible rule.
        self.adj_list = defaultdict(set)
        for source_id in range(self.num_states):
            source = State(features, self._index_to_propositions(source_id))
            for target_id in range(self.num_states):
                target = State(features, self._index_to_propositions(target_id))
                for rule in rules.rules:
                    if rule.is_compatible(source, target):
                        print("%s, %s, %s" % (source, target, rule))
                        self.adj_list[source_id].add(Edge(source_id, target_id, rule))

    def _index_to_propositions(self, index):
        """ Compute propositions from a state index.
        """
        propositions = []
        p = 0
        while index > 0:
            if index & 1 > 0:
                propositions.append(p)
            index >>= 1
            p += 1

        return propositions


    def sieve(self, states):
        """ Run the Sieve algorithm to compute whether the policy is termination.
        """
        # 1. Compute strongly connected components
        sccs = Kosajaru().compute_sccs(states, self.adj_list)
        # 2. Call sieve_scc for each strongly connected components g' in SCC(g).
        #    Return "Non-terminating", if at least one call returns "Non-terminating".
        #    Return "Terminating", otherwise.
        for scc in sccs:
            if not self._sieve_scc(scc):
                return False
        return True

    def _sieve_scc(self, states):
        """
        """
        # 1. iteratively remove edges.
        # 2. if g' is acyclic return "Terminating"
        # 3. if no edges were removed from g' return "Non-terminating"
        # 4. if at least one edge was removed then return the result of another call to sieve.
