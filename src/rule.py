from .feature import PositiveLiteral, NegativeLiteral

class Rule:
    """ Rule consists of list of Conditions and list of Effects
    """
    def __init__(self, conditions, effects):
        self.conditions = conditions
        self.effects = effects

    def is_compatible(self, source, target):
        for condition in self.conditions:
            if not condition.literal.is_satisfied(source):
                return False
        for effect in self.effects:
            satisfied_at_least_one = False
            for condition in effect.successor_conditions:
                if condition.literal.index in target:
                    satisfied_at_least_one = True
            if not satisfied_at_least_one:
                return False
        return True


class Rules:
    def __init__(self, features, tokens):
        self.rules = [Rule(conditions, effects) for conditions, effects in self._parse(features, tokens)]

    def _parse(self, features, tokens):
        if not tokens:
            raise Exception("Unexpected EOF.")
        t = tokens.pop(0)
        if t == "[":
            children = []
            while tokens and tokens[0] != "]":
                children.append(self._parse(features, tokens))
            if not tokens:
                raise Exception("Expected ']'.")
            assert tokens.pop(0) == "]"
            return children
        elif t == "(":
            if not tokens:
                raise Exception("Expected condition of effect.")
            feature = tokens.pop(0)
            if not tokens:
                raise Exception("Expected ')'")
            assert tokens.pop(0) == ")"
            return feature
        elif t in ["c_pos", "c_neg", "c_gt", "c_eq"]:
            return features.get_feature(self._parse(features, tokens)).make_condition(t)
        elif t in ["e_pos", "e_neg", "e_dec", "e_inc", "e_unk"]:
            return features.get_feature(self._parse(features, tokens)).make_effect(t)
        else:
            raise Exception(f"Unknown token {t}.")
