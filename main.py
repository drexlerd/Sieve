import argparse

from src.policy_graph import PolicyGraph
from src.policy import Policy

# python3 main.py "[b]" "[n]" "[[[c_gt(n)],[e_dec(n)]], [[c_pos(b)], [e_neg(b)]]]"

# tpp
# python3 main.py "[]" "[u, w]" "[[[c_gt(u)], [e_dec(u)]], [[c_gt(w)], [e_unk(u), e_dec(w)]]]"

# barman
# python3 main.py "[c1, c2]" "[u, g]" "[[[c_neg(c1)],[e_unk(u), e_pos(c1)]], [[c_pos(c1), c_neg(c2)],[e_unk(u), e_pos(c2)]], [[c_gt(u)],[e_dec(u)]], [[c_gt(g)],[e_dec(g), e_unk(c1), e_unk(c2)]]]"

# grid
# python3 main.py "[o, t]" "[l, k]" "[[[c_gt(l)],[e_dec(l), e_unk(k), e_unk(o), e_unk(t)]], [[c_eq(l), c_gt(k)],[e_dec(k), e_unk(o), e_unk(t)]], [[c_gt(l), c_neg(o)],[e_pos(o), e_unk(t)]], [[c_eq(l), c_neg(t)],[e_unk(o), e_pos(t)]]]"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sieve Algorithm")
    parser.add_argument("booleans", type=str, help="A list of names of boolean features, e.g., [b,]")
    parser.add_argument("numericals", type=str, help="A list of names of boolean features, e.g., [n,]")
    parser.add_argument("rules", type=str, help="A list of policy rules, e.g., [[[c_gt(n)],[e_dec(n)]], [[c_pos(b)], [e_neg(b)]]]")
    args = parser.parse_args()

    boolean_names = [x.strip() for x in args.booleans.strip('][').split(',') if x]
    numerical_names = [x.strip() for x in args.numericals.strip('][').split(',') if x]
    rules_description = args.rules

    policy = Policy(boolean_names, numerical_names, rules_description)
    policy_graph = PolicyGraph(policy)
    if policy_graph.sieve([i for i in range(policy_graph.num_states)]):
        print("Terminating")
    else:
        print("Non-terminating")
