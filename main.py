import argparse

from src.tokenizer import Tokenizer
from src.policy_graph import PolicyGraph

# main.py [] [a] [[[gt(a)],[dec(a)]],]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sieve Algorithm")
    parser.add_argument("booleans", type=str, help="A list of names of boolean features, e.g., [b1,b2,b3]")
    parser.add_argument("numericals", type=str, help="A list of names of boolean features, e.g., [n1,n2,n3]")
    parser.add_argument("rules", type=str, help="A list of policy rules, e.g., [[[gt(n1)],[dec(n1)]],]")
    args = parser.parse_args()
    tokens = Tokenizer().tokenize(args.rules)
    print(tokens)
    boolean_names = [x.strip() for x in args.booleans.strip('][').split(',') if x]
    numerical_names = [x.strip() for x in args.numericals.strip('][').split(',') if x]
    policy_graph = PolicyGraph(boolean_names, numerical_names)
    
