
class Node:
    def __init__(self,floor=-1,cost=0,profit=0,path=[]):
        self.floor = floor
        self.cost = cost
        self.profit = profit
        self.prediction = 0
        self.path  =  path if path is not None else []

    def bound(self,sorted_items,budget):
        remaining_capacity = budget-self.cost
        bound = 0
        item_index = self.floor+1
        while item_index<(len(sorted_items)) and remaining_capacity>0:
            if sorted_items[item_index][1] <= remaining_capacity:
                remaining_capacity -= sorted_items[item_index][1]
                bound += sorted_items[item_index][3]
            else:
                fraction = remaining_capacity/sorted_items[item_index][1]
                fractional_profit = sorted_items[item_index][3]*fraction
                bound += fractional_profit
                remaining_capacity = 0
            item_index += 1
        self.prediction  = bound



def select_best_node_by_weight_plus_bound(list_of_node):
    best = list_of_node[0]
    for x in list_of_node:
        if x.prediction+x.profit>best.prediction+best.profit:
            best=x
    return best

def a_star(json):
    budget = json["budget"]
    ranks = json["item_ranks"]
    item_costs = json["item_costs"]
    indeks = [i+1 for i in range(len(ranks))]
    pro_to_weig = [ranks[i]/item_costs[i] for i in range(len(item_costs)) ]
    lista_obiektow = list(zip(pro_to_weig, item_costs, indeks,ranks))
    sorted_items = sorted(lista_obiektow,key = lambda element: element[0], reverse = True)
    start_node =  Node()
    start_node.bound(sorted_items,budget)
    priority_queue = [start_node]
    best_profit = 0
    best_path = []
    expanded_nodes = 0
    while priority_queue:
        x = select_best_node_by_weight_plus_bound(priority_queue)
        priority_queue.remove(x)
        next_floor = x.floor+1
        if len(item_costs)>next_floor:
            expanded_nodes += 1
            left_child = Node(next_floor,x.cost+sorted_items[next_floor][1], x.profit+sorted_items[next_floor][3],x.path + [sorted_items[next_floor][2]])#biore dziecko
            right_child = Node(next_floor,x.cost, x.profit,x.path)
            left_child.bound(sorted_items,budget)
            right_child.bound(sorted_items,budget)
            if left_child.cost <= budget:
                if left_child.prediction+left_child.profit > best_profit:
                    if left_child.profit > best_profit:
                        best_profit = left_child.profit
                        best_path = left_child.path
                    priority_queue.append(left_child)
            if right_child.prediction+right_child.profit>best_profit:
                priority_queue.append(right_child)
    return best_profit, best_path, expanded_nodes



def select_best_node_by_bound(list_of_node):
    best=list_of_node[0]
    for x in list_of_node:
        if x.prediction>best.prediction:
            best = x
    return best

def best_first(json):
    budget = json["budget"]
    ranks = json["item_ranks"]
    item_costs = json["item_costs"]
    indeks = [i+1 for i in range(len(ranks))]
    pro_to_weig = [ranks[i]/item_costs[i] for i in range(len(item_costs)) ]
    lista_obiektow = list(zip(pro_to_weig, item_costs, indeks,ranks))
    sorted_items = sorted(lista_obiektow,key = lambda element: element[0], reverse = True)
    start_node= Node()
    start_node.bound(sorted_items,budget)
    priority_queue = [start_node]
    best_profit = 0
    best_path=[]
    expanded_nodes = 0
    while priority_queue:
        x=select_best_node_by_bound(priority_queue)
        priority_queue.remove(x)
        next_floor = x.floor+1
        if len(item_costs)>next_floor:
            expanded_nodes += 1
            left_child = Node(next_floor,x.cost+sorted_items[next_floor][1], x.profit+sorted_items[next_floor][3],x.path + [sorted_items[next_floor][2]])#biore dziecko
            right_child = Node(next_floor,x.cost, x.profit,x.path)
            left_child.bound(sorted_items,budget)
            right_child.bound(sorted_items,budget)
            if left_child.cost <= budget:
                if left_child.prediction+left_child.profit > best_profit:
                    if left_child.profit > best_profit:
                        best_profit = left_child.profit
                        best_path = left_child.path
                    priority_queue.append(left_child)
            if right_child.prediction+right_child.profit>best_profit:
                priority_queue.append(right_child)
    return best_profit, best_path, expanded_nodes

def greedy_best_first(json):
    budget = json["budget"]
    ranks = json["item_ranks"]
    item_costs = json["item_costs"]
    indeks = [i+1 for i in range(len(ranks))]
    pro_to_weig = [ranks[i]/item_costs[i] for i in range(len(item_costs))]
    lista_obiektow = list(zip(pro_to_weig, item_costs, indeks, ranks))
    sorted_items = sorted(lista_obiektow, key=lambda element: element[0], reverse=True)

    start_node = Node()
    start_node.bound(sorted_items, budget)

    current_node = start_node
    best_profit = 0
    best_path = []
    expanded_nodes = 0

    while True:

        next_floor = current_node.floor + 1

        if len(item_costs) <= next_floor:
            break

        expanded_nodes += 1

        left_child = Node(
            next_floor,
            current_node.cost + sorted_items[next_floor][1],
            current_node.profit + sorted_items[next_floor][3],
            current_node.path + [sorted_items[next_floor][2]]
        )

        right_child = Node(
            next_floor,
            current_node.cost,
            current_node.profit,
            current_node.path
        )

        left_child.bound(sorted_items, budget)
        right_child.bound(sorted_items, budget)

        candidates = []

        if left_child.cost <= budget:
            if left_child.profit > best_profit:
                best_profit = left_child.profit
                best_path = left_child.path
            candidates.append(left_child)

        candidates.append(right_child)

        if not candidates:
            break

        best = candidates[0]
        for x in candidates:
            if x.prediction + x.profit > best.prediction + best.profit:
                best = x

        current_node = best

    return best_profit, best_path, expanded_nodes