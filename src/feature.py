import abc


class Literal(abc.ABC):
    """ Literal represents boolean feature valuation.
    """
    def __init__(self, index : int):
        self.index = index

    @abc.abstractmethod
    def is_satisfied(self, state : set):
        pass

class PositiveLiteral(Literal):
    def __init__(self, index):
        super().__init__(index)

    def is_satisfied(self, state : set):
        return self.index in state

class NegativeLiteral(Literal):
    def __init__(self, index):
        super().__init__(index)

    def is_satisfied(self, state : set):
        return self.index not in state


class Condition():
    """ Conditions for deriving boolean feature valuations.
        We call the boolean feature valuations as propositions
        because they can be either true or false.
    """
    def __init__(self,  literal):
        self.literal = literal


class PositiveBooleanCondition(Condition):
    def __init__(self, feature):
        super().__init__(PositiveLiteral(feature.index))

class NegativeBooleanCondition(Condition):
    def __init__(self, feature):
        super().__init__(NegativeLiteral(feature.index))

class EqualNumericalCondition(Condition):
    def __init__(self, feature):
        super().__init__(PositiveLiteral(feature.index))

class GreaterNumericalCondition(Condition):
    def __init__(self, feature):
        super().__init__(NegativeLiteral(feature.index))


class Effect():
    """ Effects for deriving successor conditions.
    """
    def __init__(self, successor_conditions):
        self.successor_conditions = successor_conditions


class PositiveBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__([PositiveBooleanCondition(feature)])

class NegativeBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__([NegativeBooleanCondition(feature)])

class IncrementNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__([GreaterNumericalCondition(feature)])

class DecrementNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__([GreaterNumericalCondition(feature), EqualNumericalCondition(feature)])

class UnknownBooleanEffect(Effect):
    def __init__(self, feature):
        super().__init__([PositiveBooleanCondition(feature), NegativeBooleanCondition(feature)])

class UnknownNumericalEffect(Effect):
    def __init__(self, feature):
        super().__init__([GreaterNumericalCondition(feature), EqualNumericalCondition(feature)])


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

class BooleanFeature(Feature):
    def __init(self, index, name):
        super().__init(index, name)

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
        else:
            raise Exception(f"Unknown condition: {name}")

class NumericalFeature(Feature):
    def __init(self, index, name):
        super().__init(index, name)

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
        else:
            raise Exception(f"Unknown condition: {name}")


class Features:
    def __init__(self, boolean_names, numerical_names):
        self.features = []
        self.feature_to_index = dict()
        for b in boolean_names:
            self._add_boolean_feature(b)
        for n in numerical_names:
            self._add_numerical_feature(n)

    def _add_boolean_feature(self, name):
        b = BooleanFeature(len(self.features), name)
        self.feature_to_index[b.name] = b.index
        self.features.append(b)

    def _add_numerical_feature(self, name):
        n = NumericalFeature(len(self.features), name)
        self.feature_to_index[n.name] = n.index
        self.features.append(n)

    def get_feature(self, name):
        if name not in self.feature_to_index:
            raise Exception(f"There is no feature with name {name}")
        return self.features[self.feature_to_index[name]]
