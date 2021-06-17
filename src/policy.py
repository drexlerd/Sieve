from .feature import FeaturesParser
from .rule import RulesParser


class Policy:
    def __init__(self, boolean_names, numerical_names, rules_description):
        self.features = FeaturesParser().parse(boolean_names, numerical_names)
        self.rules = RulesParser().parse(self.features, rules_description)

    def get_num_features(self):
        return len(self.features.features)
