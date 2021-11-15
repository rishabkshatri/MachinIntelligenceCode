"""

You can create any other helper funtions.

Do not modify the given functions

"""

import queue

import copy


def A_star_Traversal(cost, heuristic, start_point, goals):
    """

    Perform A* Traversal and find the optimal path 

    Args:

        cost: cost matrix (list of floats/int)

        heuristic: heuristics for A* (list of floats/int)

        start_point: Staring node (int)

        goals: Goal states (list of ints)

    Returns:

        path: path to goal state obtained from A*(list of ints)

    """


n = len(cost)

visited = [0 for i in range(n)]

frontier_priority_queue = queue.PriorityQueue()

frontier_priority_queue.put((heuristic[start_point], ([start_point], start_point, 0)))

while (frontier_priority_queue.qsize() != 0):

    total_estimated_cost, nodes_tuple = frontier_priority_queue.get()

    A_star_path_till_node = nodes_tuple[0]

    node = nodes_tuple[1]

    node_cost = nodes_tuple[2]

    if visited[node] == 0:

        visited[node] = 1

        if node in goals:
            return A_star_path_till_node

        for neighbour_node in range(1, n):

            if cost[node][neighbour_node] > 0 and visited[neighbour_node] == 0:
                total_cost_till_node = node_cost + cost[node][neighbour_node]

                estimated_total_cost = total_cost_till_node + heuristic[neighbour_node]

                A_star_path_till_neighbour_node = copy.deepcopy(A_star_path_till_node)

                A_star_path_till_neighbour_node.append(neighbour_node)

                frontier_priority_queue.put(
                    (estimated_total_cost, (A_star_path_till_neighbour_node, neighbour_node, total_cost_till_node)))

return list()


def DFS_Traversal(cost, start_point, goals):
    """

    Perform DFS Traversal and find the optimal path 

        cost: cost matrix (list of floats/int)

        start_point: Staring node (int)

        goals: Goal states (list of ints)

    Returns:

        path: path to goal state obtained from DFS(list of ints)

    """

    n = len(cost)

    visited = [0 for i in range(n)]

    frontier_stack = queue.LifoQueue()

    frontier_stack.put((start_point, [start_point]))

    while (frontier_stack.qsize() != 0):

        node, dfs_path_till_node = frontier_stack.get()

        if visited[node] == 0:

            visited[node] = 1

            if node in goals:
                return dfs_path_till_node

            for neighbour_node in range(n - 1, 0, -1):

                if cost[node][neighbour_node] > 0:

                    if visited[neighbour_node] == 0:
                        dfs_path_till_neighbour_node = copy.deepcopy(dfs_path_till_node)

                        dfs_path_till_neighbour_node.append(neighbour_node)

                        frontier_stack.put((neighbour_node, dfs_path_till_neighbour_node))

    return list()