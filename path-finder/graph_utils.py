import networkx as nx


def add_slope(graph, start, end, weather, difficulty, average_time, weights):
    weight = weights['weather_weight'] * weather + \
        weights['difficulty_weight'] * (1 - difficulty)
    graph.add_edge(start, end, weight=weight, type='slope',
                   weather=weather, difficulty=difficulty, time=average_time)


def add_lift(graph, start, end, waiting_time, average_time, weights):
    weight = weights['waiting_time_weight'] * waiting_time
    graph.add_edge(start, end, weight=weight, type='lift',
                   waiting_time=waiting_time, time=average_time)


def find_initial_path_with_time_constraint(graph, start, end, desired_time_minutes):
    all_paths = list(nx.all_simple_paths(graph, start, end))
    closest_path = None
    closest_weighted_time_diff = float('inf')

    for path in all_paths:
        total_time = sum(graph[path[i]][path[i+1]]['time']
                         for i in range(len(path)-1))
        total_weight = sum(graph[path[i]][path[i+1]]['weight']
                           for i in range(len(path)-1))
        weighted_time = total_time * total_weight
        weighted_time_diff = abs(weighted_time - desired_time_minutes)

        if weighted_time_diff < closest_weighted_time_diff:
            closest_path = path
            closest_weighted_time_diff = weighted_time_diff

    return closest_path, closest_weighted_time_diff


def extend_path_if_needed(graph, path, desired_time_minutes):
    total_time = sum(graph[path[i]][path[i+1]]['time']
                     for i in range(len(path)-1))
    extended_path = list(path)

    for i in range(1, len(path)-2):
        for neighbor in graph.neighbors(path[i]):
            if neighbor not in path and graph.has_edge(neighbor, path[i+1]):
                detour_time = graph[path[i]][neighbor]['time'] + \
                    graph[neighbor][path[i+1]]['time']
                if total_time + detour_time <= desired_time_minutes:
                    extended_path.insert(i+1, neighbor)
                    total_time += detour_time
                if total_time >= desired_time_minutes:
                    break
        if total_time >= desired_time_minutes:
            break

    return extended_path
