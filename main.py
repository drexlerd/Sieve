import argparse

from src.policy_graph import PolicyGraph
from src.policy import Policy

# test
# python3 main.py "[b]" "[n]" "[[[c_gt(n)],[e_dec(n)]], [[c_pos(b)], [e_neg(b)]]]"

# floortile
# python3 main.py "[v]" "[g]" "[[[c_pos(v), c_gt(g)],[e_dec(g)]]]"

# tpp
# python3 main.py "[]" "[u, w]" "[[[c_gt(u)], [e_dec(u)]], [[c_gt(w)], [e_unk(u), e_dec(w)]]]"

# barman
# python3 main.py "[c1, c2]" "[u, g]" "[[[c_neg(c1)],[e_unk(u), e_pos(c1)]], [[c_pos(c1), c_neg(c2)],[e_unk(u), e_pos(c2)]], [[c_gt(u)],[e_dec(u)]], [[c_gt(g)],[e_dec(g), e_unk(c1), e_unk(c2)]]]"

# grid
# python3 main.py "[o, t]" "[l, k]" "[[[c_gt(l)],[e_dec(l), e_unk(k), e_unk(o), e_unk(t)]], [[c_eq(l), c_gt(k)],[e_dec(k), e_unk(o), e_unk(t)]], [[c_gt(l), c_neg(o)],[e_pos(o), e_unk(t)]], [[c_eq(l), c_neg(t)],[e_unk(o), e_pos(t)]]]"

# childsnack
# python3 main.py "[s_g^k, s^k, s_g^t, s^t]" "[c_g, c_r]" "[[[c_gt(c_g),c_neg(s_g^k),c_neg(s_g^t)],[e_pos(s_g^k),e_pos(s^k)]], [[c_eq(c_g),c_gt(c_r),c_neg(s^k),c_neg(s^t)],[e_pos(s^k)]], [[c_gt(c_g),c_pos(s_g^k),c_neg(s_g^t)],[e_unk(s_g^k),e_unk(s^k),e_pos(s_g^t),e_pos(s^t)]], [[c_eq(c_g),c_gt(c_r),c_pos(s^k),c_neg(s^t)],[e_unk(s_g^k),e_unk(s^k),e_unk(s_g^t),e_pos(s^t)]], [[c_gt(c_g),c_pos(s_g^t)],[e_dec(c_g),e_unk(s_g^t),e_unk(s^t)]], [[c_eq(c_g),c_gt(c_r),c_pos(s^t)],[e_dec(c_r),e_unk(s_g^t),e_unk(s^t)]]]"

# driverlog
# python3 main.py "[b, l]" "[p, t, d_g, d_t]" "[[[c_gt(p),c_neg(b)], [e_unk(d_g),e_unk(d_t),e_pos(b)]], [[c_gt(p),c_neg(l)], [e_unk(t),e_unk(d_g),e_unk(d_t),e_pos(l)]], [[c_gt(p)], [e_dec(p), e_unk(t), e_unk(d_g), e_unk(d_t), e_unk(l)]], [[c_eq(p),c_gt(t),c_gt(d_t)], [e_unk(d_g),e_dec(d_t),e_unk(b)]], [[c_eq(p),c_gt(t),c_eq(d_t)], [e_dec(t),e_unk(d_g),e_unk(d_t)]], [[c_eq(p),c_eq(t),c_gt(d_g)], [e_dec(d_g),e_unk(b)]]]"

# schedule
# python3 main.py "[h, o]" "[p1, p2, p3]" "[[[c_gt(p1)],[e_dec(p1),e_unk(p2),e_unk(p3),e_pos(o)]], [[c_eq(p1),c_gt(p2)],[e_dec(p2),e_unk(p3),e_pos(o)]], [[c_eq(p1), c_eq(p2), c_gt(p3)],[e_dec(p3), e_pos(o)]], [[c_pos(o)],[e_neg(o)]]]"


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
