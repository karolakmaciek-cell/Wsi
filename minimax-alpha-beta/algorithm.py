import random

node_counter = 0

class Node:
    def __init__(self, left_tokens, last_move=None):
        self.left_tokens = left_tokens
        self.last_move = last_move
        self.successors = None
        self.heuristic = None

    def successors_make(self,K):
        if self.successors is None:
            self.successors = []
            max_tokens = min(self.left_tokens,K)
            for n in range(1,max_tokens+1):
                self.successors.append(Node(self.left_tokens-n,n ))
        return self.successors


    def heuristic_make(self, is_max, K):
        if self.left_tokens == 0:
            self.heuristic= 1000 if is_max else -1000
            return
        curr_mod = self.left_tokens % (K+1)
        if is_max:
            if curr_mod == 1:
                self.heuristic = 10
            else:
                self.heuristic=-10
        else:
            if curr_mod == 1:
                self.heuristic = -10
            else:
                self.heuristic = 10


def Minimax(node, K, d, is_max=True):
    global node_counter
    node_counter+=1
    if node.left_tokens == 0 or d == 0:
        node.heuristic_make(is_max,K)
        return node
    successors = node.successors_make(K)
    w = []
    for u in successors:
        w.append(Minimax(u, K, d-1, not is_max))
    if is_max:
        random.shuffle(w)
        best_node = max(w ,key=lambda x:x.heuristic)
    else:
        random.shuffle(w)
        best_node = min(w ,key=lambda x:x.heuristic)
    node.heuristic=best_node.heuristic
    return best_node

def AlfaBeta(node, K, d, alfa=float("-inf"), beta=float("inf"), is_max=True):
    global node_counter
    node_counter+=1
    if node.left_tokens == 0 or d == 0:
        node.heuristic_make(is_max, K)
        return node

    successors = node.successors_make(K)
    random.shuffle(successors)

    best_node = None

    if is_max:
        for u in successors:
            child = AlfaBeta(u, K, d-1, alfa, beta, not is_max)

            if best_node is None or child.heuristic > best_node.heuristic:
                best_node = child

            alfa = max(alfa, child.heuristic)

            if alfa >= beta:
                break

        node.heuristic = best_node.heuristic
        return best_node

    else:
        for u in successors:
            child = AlfaBeta(u, K, d-1, alfa, beta, not is_max)

            if best_node is None or child.heuristic < best_node.heuristic:
                best_node = child

            beta = min(beta, child.heuristic)

            if alfa >= beta:
                break

        node.heuristic = best_node.heuristic
        return best_node
