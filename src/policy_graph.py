from collections import defaultdict
from .kosajaru import Kosajaru
from .feature import IncrementNumericalEffect, DecrementNumericalEffect, NegativeBooleanEffect, PositiveBooleanEffect, UnknownBooleanEffect, UnknownNumericalEffect


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
        self.forward_graph = defaultdict(set)
        self.backward_graph = defaultdict(set)
        for source_id in range(self.num_states):
            source = State(policy.features, self._index_to_propositions(source_id))
            for target_id in range(self.num_states):
                target = State(policy.features, self._index_to_propositions(target_id))
                for rule in policy.rules:
                    if rule.is_compatible(source, target):
                        print("%s, %s, %s" % (source, target, rule))
                        edge = Edge(source_id, target_id, rule)
                        self.forward_graph[source_id].add(edge)
                        self.backward_graph[target_id].add(edge)
        print([str(State(self.policy.features, self._index_to_propositions(i))) for i in range(self.num_states)])

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


    def _print_graphs(self):
        print("Forward graph:")
        for source_id, edges in self.forward_graph.items():
            for edge in edges:
                print("%s %s" % (edge.source_id, edge.target_id))
        print("Backward graph:")
        for source_id, edges in self.backward_graph.items():
            for edge in edges:
                print("%s %s" % (edge.source_id, edge.target_id))
        print()


    def sieve(self, state_ids):
        """ Run the Sieve algorithm to compute whether the policy is termination.
        """
        # 1. Compute strongly connected components
        sccs = Kosajaru().compute_sccs(state_ids, self.forward_graph, self.backward_graph)
        print(sccs)
        # 2. Remove edges between different sccs because they are traversed only once.
        for scc in sccs:
            scc_set = set(scc)
            for source_id in scc:
                remove = []
                for edge in self.forward_graph[source_id]:
                    if edge.target_id not in scc_set:
                        remove.append(edge)
                for edge in remove:
                    self.forward_graph[edge.source_id].discard(edge)
                    self.backward_graph[edge.target_id].discard(edge)
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
        # 1. if g' is acyclic return "Terminating"
        if len(state_ids) == 1:
            return True
        # 1. Iteratively remove edges.
        rules = set()
        for source_id in state_ids:
            for edge in self.forward_graph[source_id]:
                rules.add(edge.rule)
        # Collect rules that decrement some feature that no other rule increments in this scc
        incremented_features = set()
        decremented_features = set()
        decremented_rules = defaultdict(set)
        for rule in rules:
            for effect in rule.effects:
                if isinstance(effect, DecrementNumericalEffect) or \
                   isinstance(effect, NegativeBooleanEffect):
                    decremented_features.add(effect.feature.index)
                    decremented_rules[effect.feature.index].add(rule)
                elif isinstance(effect, IncrementNumericalEffect) or \
                     isinstance(effect, UnknownNumericalEffect) or \
                     isinstance(effect, PositiveBooleanEffect) or \
                     isinstance(effect, UnknownBooleanEffect):
                    incremented_features.add(effect.feature.index)
        decremented_features.difference(incremented_features)
        removable_rules = set()
        for d in decremented_features:
            for rule in decremented_rules[d]:
                removable_rules.add(rule)
        # Remove edges
        removed = False
        for source_id in state_ids:
            remove = []
            for edge in self.forward_graph[source_id]:
                if edge.rule in removable_rules:
                    remove.append(edge)
                    removed = True
            for edge in remove:
                self.forward_graph[edge.source_id].discard(edge)
                self.backward_graph[edge.target_id].discard(edge)
        # 3. if no edges were removed from g' return "Non-terminating"
        if not removed:
            self._print_graphs()
            return False
        # 4. if at least one edge was removed then return the result of another call to sieve.
        else:
            return self.sieve(state_ids)
