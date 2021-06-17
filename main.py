import argparse

from src.tokenizer import Tokenizer
from src.policy_graph import PolicyGraph
from src.feature import Features
from src.rule import Rules

# python3 main.py "[b]" "[n]" "[[[c_gt(n)],[e_dec(n)]], [[c_pos(b)], [e_neg(b)]]]"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sieve Algorithm")
    parser.add_argument("booleans", type=str, help="A list of names of boolean features, e.g., [b,]")
    parser.add_argument("numericals", type=str, help="A list of names of boolean features, e.g., [n,]")
    parser.add_argument("rules", type=str, help="A list of policy rules, e.g., [[[c_gt(n)],[e_dec(n)]], [[c_pos(b)], [e_neg(b)]]]")
    args = parser.parse_args()

    boolean_names = [x.strip() for x in args.booleans.strip('][').split(',') if x]
    numerical_names = [x.strip() for x in args.numericals.strip('][').split(',') if x]
    rules = args.rules

    tokens = Tokenizer().tokenize(rules)
    features = Features(boolean_names, numerical_names)
    rules = Rules(features, tokens)
    policy_graph = PolicyGraph(features, rules)
    policy_graph.sieve([i for i in range(len(features.features))])
