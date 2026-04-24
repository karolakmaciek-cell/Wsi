from algorithm import Node, Minimax, AlfaBeta

if __name__=="__main__":
    print(Minimax(Node(20), 3, 2).last_move)
    print(AlfaBeta(Node(20),3, 2).last_move)