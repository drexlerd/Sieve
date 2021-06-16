
from collections import defaultdict

from .valuation import Valuation

def compute_valuations(boolean_names : list, numerical_names):
    valuations = []
    for b in boolean_names:
        valuations.append(Valuation(len(valuations), f"pos({b})"))
        valuations.append(Valuation(len(valuations), f"neg({b})"))
    for n in numerical_names:
        valuations.append(Valuation(len(valuations), f"gt({n}"))
        valuations.append(Valuation(len(valuations), f"eq({n}"))
    return valuations


class PolicyGraph:
    def __init__(self, boolean_names, numerical_names):
        self.valuations = compute_valuations(boolean_names, numerical_names)
        print(self.valuations)
        
        self.adj_list = defaultdict(set)

    def add_edges(self, rule):
        """ Adds edges for given rule
        """
        pass


