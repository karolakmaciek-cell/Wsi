from function import a_star, greedy_best_first
import time
import matplotlib.pyplot as plt


def main():

    tree_30 = {
        "budget": 300,
        "item_costs": [
            25,30,28,20,22,18,15,17,19,24,
            26,29,31,27,23,21,16,14,13,12,
            11,10,9,8,7,6,5,4,3,2
        ],
        "item_ranks": [
            50,60,55,45,47,40,35,37,38,48,
            52,58,62,54,46,42,33,30,28,25,
            23,21,20,18,15,12,10,8,6,4
        ]
    }

    tree_50 = {
        "budget": 1000,
        "item_costs": [
            220,208,198,192,180,180,165,162,160,158,
            155,130,125,122,120,118,115,110,105,101,
            100,100,98,96,95,90,88,82,80,77,
            75,73,72,70,69,66,65,63,60,58,
            56,50,30,20,15,10,8,5,3,1
        ],
        "item_ranks": [
            80,82,85,70,72,70,66,50,55,25,
            50,55,40,48,50,32,22,60,30,32,
            40,38,35,32,25,28,30,22,25,30,
            45,30,60,50,20,65,20,25,30,10,
            20,25,15,10,10,10,4,4,2,1
        ]
    }

    tree_80 = {
        "budget": 1500,
        "item_costs": [
            120,115,110,108,105,102,100,98,96,94,
            92,90,88,86,84,82,80,78,76,74,
            72,70,68,66,64,62,60,58,56,54,
            52,50,48,46,44,42,40,38,36,34,
            32,30,28,26,24,22,20,18,16,14,
            13,12,11,10,9,8,7,6,5,4,
            120,118,116,114,112,109,107,103,101,99,
            97,95,93,91,89,87,85,83,81,79
        ],
        "item_ranks": [
            90,85,82,80,78,76,75,72,70,68,
            66,65,63,60,58,56,55,54,52,50,
            48,47,45,43,41,40,38,36,35,33,
            32,30,28,27,25,24,22,21,20,18,
            17,16,15,14,13,12,11,10,9,8,
            7,6,5,4,3,2,1,1,1,1,
            88,86,84,82,80,79,77,73,71,69,
            67,66,64,62,59,57,55,53,51,49
        ]
    }

    tests = [tree_30, tree_50, tree_80]

    sizes = []

    time_astar = []
    time_greedy = []

    nodes_astar = []
    nodes_greedy = []

    profit_astar = []
    profit_greedy = []

    for data in tests:

        sizes.append(len(data["item_costs"]))

        #A*
        start = time.time()
        profit, path, nodes = a_star(data)
        end = time.time()

        time_astar.append(end - start)
        nodes_astar.append(nodes)
        profit_astar.append(profit)

        #Greedy Best-First
        start = time.time()
        profit, path, nodes = greedy_best_first(data)
        end = time.time()

        time_greedy.append(end - start)
        nodes_greedy.append(nodes)
        profit_greedy.append(profit)

    x = range(len(sizes))
    width = 0.35

    #wykresy
    plt.figure(figsize=(8,5))
    plt.bar([i - width/2 for i in x], time_astar, width, label="A*")
    plt.bar([i + width/2 for i in x], time_greedy, width, label="Greedy Best First")
    plt.xticks(x, sizes)
    plt.xlabel("Liczba przedmiotów")
    plt.ylabel("Czas działania (s)")
    plt.title("Porównanie czasu działania algorytmów")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    #wykres wezlow
    plt.figure(figsize=(8,5))
    plt.bar([i - width/2 for i in x], nodes_astar, width, label="A*")
    plt.bar([i + width/2 for i in x], nodes_greedy, width, label="Greedy Best First")
    plt.xticks(x, sizes)
    plt.xlabel("Liczba przedmiotów")
    plt.ylabel("Liczba rozwiniętych węzłów")
    plt.title("Porównanie liczby rozwiniętych stanów")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    #wykres jakosci
    plt.figure(figsize=(8,5))
    plt.bar([i - width/2 for i in x], profit_astar, width, label="A*")
    plt.bar([i + width/2 for i in x], profit_greedy, width, label="Greedy Best First")
    plt.xticks(x, sizes)
    plt.xlabel("Liczba przedmiotów")
    plt.ylabel("Uzyskany zysk")
    plt.title("Jakość rozwiązania")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()


if __name__ == "__main__":
    main()