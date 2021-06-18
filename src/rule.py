
class Rule:
    """ Rule consists of list of Conditions and list of Effects
    """
    def __init__(self, features, conditions, effects):
        self.features = features
        self.conditions = conditions
        self.effects = effects

    def is_compatible(self, source, target):
        for condition in self.conditions:
            if not condition.is_satisfied(source):
                return False
        checked = set()
        for effect in self.effects:
            checked.add(effect.feature.index)
            if not effect.is_satisfied(source, target):
                return False
        for index in range(self.features.get_num_features()):
            if index not in checked:
                unchanged_effect = self.features.get_feature_by_index(index).make_effect("e_same")
                if not unchanged_effect.is_satisfied(source, target):
                    return False
        return True

    def __str__(self):
        return str([str(c) for c in self.conditions]) + "->" + str([str(e) for e in self.effects])


class Tokenizer():
    """ Tokenizes the rule description.
    """
    def tokenize(self, text):
        tokens = []
        word = ""
        for c in text:
            if c in {"[", "]", "(", ")"}:
                if word:
                    tokens.append(word)
                    word = ""
                tokens.append(c)
            elif c in {" ", "\t", ","}:
                pass
            else:
                word += c
        return tokens


class RulesParser:
    def parse(self, features, rules_description):
        tokens = Tokenizer().tokenize(rules_description)
        return [Rule(features, conditions, effects) for conditions, effects in self._parse(features, tokens)]

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
            return features.get_feature_by_name(self._parse(features, tokens)).make_condition(t)
        elif t in ["e_pos", "e_neg", "e_dec", "e_inc", "e_unk", "e_same"]:
            return features.get_feature_by_name(self._parse(features, tokens)).make_effect(t)
        else:
            raise Exception(f"Unknown token {t}.")
