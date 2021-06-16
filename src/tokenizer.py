

class Tokenizer():
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