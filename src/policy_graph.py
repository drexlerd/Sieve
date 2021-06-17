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
    def __init__(self, policy):
        self.policy = policy
        self.num_features = policy.get_num_features()
        self.num_states = 2 ** self.num_features

        # add an edge between each state pair for which there exists a compatible rule.
        self.adj_list = defaultdict(set)
        for source_id in range(self.num_states):
            source = State(policy.features, self._index_to_propositions(source_id))
            for target_id in range(self.num_states):
                target = State(policy.features, self._index_to_propositions(target_id))
                for rule in policy.rules:
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


    def sieve(self, state_ids):
        """ Run the Sieve algorithm to compute whether the policy is termination.
        """
        # 1. Compute strongly connected components
        sccs = Kosajaru().compute_sccs(state_ids, self.adj_list)
        # 2. Remove edges between different sccs because they are traversed only once.
        for scc in sccs:
            scc_set = set(scc)
            for source_id in scc:
                remove = []
                for edge in self.adj_list[source_id]:
                    if edge.target_id not in scc_set:
                        remove.append(self.adj_list[source_id])
                for edge in remove:
                    self.adj_list[source_id].discard(edge)
        # 3. Call sieve_scc for each strongly connected components g' in SCC(g).
        #    Return "Non-terminating", if at least one call returns "Non-terminating".
        #    Return "Terminating", otherwise.
        for scc in sccs:
            if not self._sieve_scc(scc):
                return False
        return True

    def _sieve_scc(self, state_ids):
        """
        """
        # 1. iteratively remove edges.
        # 2. if g' is acyclic return "Terminating"
        # 3. if no edges were removed from g' return "Non-terminating"
        # 4. if at least one edge was removed then return the result of another call to sieve.
        print(state_ids)
        print([str(State(self.policy.features, self._index_to_propositions(state_id))) for state_id in state_ids])
        # dominik:
        # 1. Collect all features that are decremented in some edge (for boolean change from 1 to 0)
        # - decrement means DecrementNumericalEffect, NegativeBooleanEffect
        # 2. Collect all features that are incremented in some edge (for boolean change from 0 to 1)
        for source_id in state_ids:
            for edge in self.adj_list[source_id]:
                pass

        return True
