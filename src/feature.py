import abc


class Condition():
    """
    """
    def __init__(self, feature):
        self.feature = feature

    @abc.abstractmethod
    def is_satisfied(self, state):
        pass

class NegativeBooleanCondition(Condition):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, state):
        return self.feature.index in state.index_set

    def __str__(self):
        return "c_neg(" + self.feature.name + ")"

class PositiveBooleanCondition(Condition):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, state):
        return self.feature.index not in state.index_set

    def __str__(self):
        return "c_pos(" + self.feature.name + ")"

class EqualNumericalCondition(Condition):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, state):
        return self.feature.index in state.index_set

    def __str__(self):
        return "c_eq(" + self.feature.name + ")"

class GreaterNumericalCondition(Condition):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, state):
        return self.feature.index not in state.index_set

    def __str__(self):
        return "c_gt(" + self.feature.name + ")"


class Effect(abc.ABC):
    """
    """
    def __init__(self, feature):
        self.feature = feature

    @abc.abstractmethod
    def is_satisfied(self, source, target):
        pass

class PositiveBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        if self.feature.index not in target.index_set:
            return True
        return False

    def __str__(self):
        return "e_pos(" + str(self.feature.name) + ")"

class NegativeBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        if self.feature.index in target.index_set:
            return True
        return False

    def __str__(self):
        return "e_neg(" + str(self.feature.name) + ")"

class IncrementNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        # gt(n) must hold in target
        if self.feature.index not in target.index_set:
            return True
        return False

    def __str__(self):
        return "e_inc(" + str(self.feature.name) + ")"

class DecrementNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        # gt(n) or eq(n) may hold in target
        # decrement not applicable if eq(n) holds in source
        if self.feature.index not in source.index_set:
            return True
        return False

    def __str__(self):
        return "e_dec(" + str(self.feature.name) + ")"

class UnknownBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        return True

    def __str__(self):
        return "e_unk(" + str(self.feature.name) + ")"

class UnknownNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        return True

    def __str__(self):
        return "e_unk(" + str(self.feature.name) + ")"

class UnchangedBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        return (self.feature.index in source.index_set) == (self.feature.index in target.index_set)

    def __str__(self):
        return "e_same(" + str(self.feature.name) + ")"

class UnchangedNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__(feature)

    def is_satisfied(self, source, target):
        return (self.feature.index in source.index_set) == (self.feature.index in target.index_set)

    def __str__(self):
        return "e_same(" + str(self.feature.name) + ")"



class Feature(abc.ABC):
    def __init__(self, index, name):
        self.index = index
        self.name = name

    @abc.abstractmethod
    def make_condition(self, name):
        """ Return an object representing the specific feature condition.
            Throws an error if the given name is not a legal condition.
        """
        pass

    @abc.abstractmethod
    def make_effect(self, name):
        """ Return an object representing the specific feature effect.
            Throws an error if the given name is not a legal effect.
        """
        pass

    def __str__(self):
        return self.name

class BooleanFeature(Feature):
    def __init__(self, index, name):
        super().__init__(index, name)

    def make_condition(self, name):
        if name == "c_pos":
            return PositiveBooleanCondition(self)
        elif name == "c_neg":
            return NegativeBooleanCondition(self)
        else:
            raise Exception(f"Unknown condition: {name}")

    def make_effect(self, name):
        if name == "e_pos":
            return PositiveBooleanEffect(self)
        elif name == "e_neg":
            return NegativeBooleanEffect(self)
        elif name == "e_unk":
            return UnknownBooleanEffect(self)
        elif name == "e_same":
            return UnchangedBooleanEffect(self)
        else:
            raise Exception(f"Unknown condition: {name}")

class NumericalFeature(Feature):
    def __init__(self, index, name):
        super().__init__(index, name)

    def make_condition(self, name):
        if name == "c_eq":
            return EqualNumericalCondition(self)
        elif name == "c_gt":
            return GreaterNumericalCondition(self)
        else:
            raise Exception(f"Unknown condition: {self.name}")

    def make_effect(self, name):
        if name == "e_inc":
            return IncrementNumericalEffect(self)
        elif name == "e_dec":
            return DecrementNumericalEffect(self)
        elif name == "e_unk":
            return UnknownNumericalEffect(self)
        elif name == "e_same":
            return UnchangedNumericalEffect(self)
        else:
            raise Exception(f"Unknown condition: {name}")


class Features:
    def __init__(self, features, feauture_to_index):
        self.features = features
        self.feature_to_index = feauture_to_index

    def get_feature_by_index(self, index):
        return self.features[index]

    def get_feature_by_name(self, name):
        if name not in self.feature_to_index:
            raise Exception(f"There is no feature with name {name}")
        return self.features[self.feature_to_index[name]]

    def get_num_features(self):
        return len(self.features)


class FeaturesParser:
    def parse(self, boolean_names, numerical_names):
        self.features = []
        self.feature_to_index = dict()
        for b in boolean_names:
            self._add_boolean_feature(b)
        for n in numerical_names:
            self._add_numerical_feature(n)
        return Features(self.features, self.feature_to_index)

    def _add_boolean_feature(self, name):
        b = BooleanFeature(len(self.features), name)
        self.feature_to_index[b.name] = b.index
        self.features.append(b)

    def _add_numerical_feature(self, name):
        n = NumericalFeature(len(self.features), name)
        self.feature_to_index[n.name] = n.index
        self.features.append(n)
