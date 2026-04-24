import matplotlib.pyplot as plt
from tests import test_algorthm
from algorithm import Minimax, AlfaBeta
depths = [2,3,4,5]

minimax_nodes = []
alphabeta_nodes = []

for d in depths:
    _, _, n = test_algorthm(Minimax, 3, d)
    minimax_nodes.append(n)

    _, _, n = test_algorthm(AlfaBeta, 3, d)
    alphabeta_nodes.append(n)

plt.plot(depths, minimax_nodes, marker='o', label='Minimax')
plt.plot(depths, alphabeta_nodes, marker='o', label='Alpha-Beta')

plt.xlabel("Depth (d)")
plt.ylabel("Avg visited nodes")
plt.title("Comparison of node visits")
plt.legend()
plt.grid()

plt.show()