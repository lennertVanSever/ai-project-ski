import networkx as nx

# Adjusted functions to include time
def add_slope(graph, start, end, weather, difficulty, average_time):
    weight = weather_weight * weather + difficulty_weight * (1 - difficulty)
    graph.add_edge(start, end, weight=weight, type='slope', weather=weather, difficulty=difficulty, time=average_time)

def add_lift(graph, start, end, waiting_time, average_time):
    weight = waiting_time_weight * waiting_time
    graph.add_edge(start, end, weight=weight, type='lift', waiting_time=waiting_time, time=average_time)

# New function to find path
def find_path_with_time_constraint(graph, start, end, desired_time_minutes):
    all_paths = list(nx.all_simple_paths(graph, start, end))
    closest_path = None
    closest_time_diff = float('inf')

    for path in all_paths:
        total_time = sum(graph[path[i]][path[i+1]]['time'] for i in range(len(path)-1))
        time_diff = abs(total_time - desired_time_minutes)

        if time_diff < closest_time_diff:
            closest_path = path
            closest_time_diff = time_diff

    return closest_path

# Example setup with times included
weather_weight = 2.0
difficulty_weight = 1.5
waiting_time_weight = 1.0

ski_resort = nx.DiGraph()

# Adding slopes with average times (minutes)
add_slope(ski_resort, 'Peak', 'Intermediate Station', weather=0.7, difficulty=0.6, average_time=15)
add_slope(ski_resort, 'Intermediate Station', 'Base', weather=0.8, difficulty=0.3, average_time=10)
add_slope(ski_resort, 'Peak', 'Base', weather=0.5, difficulty=0.8, average_time=20)
add_slope(ski_resort, 'Intermediate Station', 'Lodge', weather=0.9, difficulty=0.2, average_time=8)
add_slope(ski_resort, 'Lodge', 'Base', weather=1.0, difficulty=0.1, average_time=5)

# Adding lifts with average times (minutes)
add_lift(ski_resort, 'Base', 'Peak', waiting_time=10, average_time=15)
add_lift(ski_resort, 'Base', 'Intermediate Station', waiting_time=5, average_time=10)
add_lift(ski_resort, 'Lodge', 'Peak', waiting_time=7, average_time=12)

# Finding a path with a time constraint
desired_time_hours = 0.6
desired_time_minutes = desired_time_hours * 60
path_with_time_constraint = find_path_with_time_constraint(ski_resort, 'Peak', 'Base', desired_time_minutes)

print("Path approximating desired time:", path_with_time_constraint)
