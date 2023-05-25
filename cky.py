from typing import Dict, List, Tuple
import string
import copy
def cky(words: List[str], grammar: Dict[str, List]):
    """
    The CKY algorithm finds all possible parses of an ambiguous sentence or phrase generated by a CFG.
    words: the sentence with each word occupies a box in the list of str (starting from index 1)
    grammar: grammar + lexicon (eg. grammar: NP -> Det N; lexicon: N -> meals)
    """

    # init the 2d table with all elements as {}(empty set), the element type considered
    table = [[set() for j in range(len(words))] for i in range(len(words) - 1)]

    for j in range(1, len(words)):

        # feed non-terminals into table from terminals in words
        for g in grammar:
            if words[j] in grammar[g]: # find lexicon in grammar
                table[j-1][j].add(g)

        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for b in table[i][k]:
                    for c in table[k][j]:
                        bc = str(b + ' ' + c) # eg. "Det N"
                        for g in grammar:
                            if bc in grammar[g]:
                                table[i][j].add(g)

    return table



def senstence_to_words(sentence: str) -> List:
    """
    convert a sentence to a list of words
    the first element in words doesn't contain info about sentence
    (can be optimized)
    """
    words = []
    words.append(0) # the first element doesn't contain any word

    word = ""
    for s in sentence:
        if s != ' ' and s not in string.punctuation: word += s
        else:
            if word != "": words.append(word)
            word = ""

    return words


def pcky(words: List[str], grammar: Dict[Tuple[str, str], float]):
    """
    Ney's variant of the CKY algorithm finds a most probable parse for a phrase or sentence
    in the language generated by an ambiguous Probabilistic Context-Free Grammar.
    words: the sentence with each word occupies a box in the list of str (starting from index 1)
    grammar: grammar + lexicon (with probability) (eg. grammar: (NP, Det N) -> float; lexicon: (N, meals) -> float)
    """
    # init the 2d table with all elements as {}(dict), the element type considered
    # each element in the table is a (non-terminal: probability)
    table = [[dict() for j in range(len(words))] for i in range(len(words) - 1)]

    # for building the parsing tree
    back = [[set() for j in range(len(words))] for i in range(len(words) - 1)]

    for j in range(1, len(words)):

        # init
        for g in grammar: # g is a tuple of rules or productions, eg. (NP, Det, N) or (N, meals)
            if words[j] == g[1]:
                table[j-1][j][g[0]] = grammar[g] # probability

        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for b in table[i][k]:
                    for c in table[k][j]:
                        prob_b = table[i][k][b]
                        prob_c = table[k][j][c]
                        if prob_b <= 0 or prob_c <= 0: break
                        for g in grammar:
                            if g[1] == str(b + " " + c):
                                if table[i][j].get(g[0]) is None or table[i][j].get(g[0]) < grammar[g] * prob_b * prob_c:
                                    table[i][j][g[0]] = grammar[g] * prob_b * prob_c
                                    back[i][j][g[0]] = {k, b, c}

    return table[1][len(words)-1]

def print_table(table: List[List]):
    for i in range(len(table)):
        for j in range(1, len(table[i])):
            print(table[i][j], end=' ')
        print()

# the parsing tree
class Node:
    def __init__(self, non_terminal, i, j):
        self.non_terminal = non_terminal
        self.pos = (i, j)
        self.children = []

    def add_left(self, child):
        self.children.append(child)

    def __str__(self):
        out = f"{self.non_terminal}"
        # if the node has the left child, it must have the right child
        for i in range(len(self.children)):
            out += f"{self.children[i]}"
        return f"[{out}]"
'''
def parse_table(table: List[List]):
    """
    table from cky
    """
    all_parse = []
    # start symbols (root)
    for s in table[0][len(table[0]) - 1]:
        all_parse.append(Node(s, 0, len(table[0])-1))

def parsing(root: Node, current: Node, table: List[List], grammar: Dict[str, List], all_parse: List):
    for k in range(current.pos[0]+1, current.pos[1]):
        L = table[current.pos[0]][k]
        R = table[k][current.poss[1]]
        list_all = [] # store all possible expansions

        for l in L:
            for r in R:
                if str(l + " " + r) == grammar(current.non_terminal):
                    list_all.append((l, r))

        for (l, r) in list_all:
            all_parse.remove(root)
            current.add_left(Node(l, current.pos[0], k))
            current.add_right(Node(r, k, current.poss[1]))
            new_root = copy.deepcopy(root)
            all_parse.append(new_root)
            parsing(new_root, current.left, table, grammar, all_parse)
            parsing(new_root, current.right, table, grammar, all_parse)
'''

def main():
    grammar = { "S": ["A B", "B C"],
                "A": ["B A", "a"],
                "B": ["C C", "b"],
                "C": ["A B", "a"]}

    words = [0, 'b', 'a', 'a', 'b', 'a']

    print_table(cky(words, grammar))

if __name__ == "__main__":
    main()

