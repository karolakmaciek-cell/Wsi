from random import randint
from algorithm import Minimax, AlfaBeta, Node
import time
import algorithm

def play_game(algoritm, K, d, N):
    node = Node(N)
    is_max = True

    while node.left_tokens>0:
        best_mv = algoritm(node, K, d, is_max)
        is_max = not is_max
        node = Node(best_mv.left_tokens)

    return not is_max


def test_algorthm(alg_funct, K, d, games=100):
    wins = 0
    total_time=0
    total_nodes = 0
    for _ in range(games):

        N = randint(8,20)

        algorithm.node_counter = 0

        start = time.time()
        result = play_game(alg_funct, K, d, N)
        end = time.time()

        total_time += (end-start)
        total_nodes += algorithm.node_counter
        if result:
            wins+=1

    return wins/games, total_time/games, total_nodes/games

def test_main(d):
    print(f"Test d={d}")
    print("MINIMAX")
    wins, total_time, total_nodes = test_algorthm(Minimax, K=3,d=d)
    print(f"Win rate: {wins}, Avg time: {total_time}, Visited_nodes:{total_nodes}")

    print("\nALPHA-BETA")
    wins, total_time, total_nodes = test_algorthm(AlfaBeta, K=3, d=d)
    print(f"Win rate: {wins}, Avg time: {total_time}, Visited_nodes:{total_nodes}")

if __name__=="__main__":
    for d in range(2,6):
        test_main(d)
