
from collections import defaultdict

class Edge:
    def __init__(self, source_id, target_id, rule):
        self.source_id = source_id
        self.target_id = target_id
        self.rule = rule


class PolicyGraph:
    def __init__(self, features, rules):
        self.num_features = len(features.features)
        self.num_states = 2 ** self.num_features

        # add an edge between each state pair for which there exists a compatible rule.
        self.adj_list = defaultdict(set)
        for source_id in range(self.num_states):
            source = set(self._index_to_propositions(source_id))
            for target_id in range(self.num_states):
                target = set(self._index_to_propositions(target_id))
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

    def sieve(self):
        """ Run the Sieve algorithm to compute whether the policy is termination.
        """
        pass
