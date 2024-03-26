import networkx as nx

def add_slope(graph, start, end, weather, difficulty):
    weight = weather_weight * weather + difficulty_weight * (1 - difficulty)
    graph.add_edge(start, end, weight=weight, type='slope', weather=weather, difficulty=difficulty)

def add_lift(graph, start, end, waiting_time):
    weight = waiting_time_weight * waiting_time
    graph.add_edge(start, end, weight=weight, type='lift', waiting_time=waiting_time)

def find_path(graph, start, end):
    path = nx.dijkstra_path(graph, start, end, weight='weight')
    return path

# Preference weights
weather_weight = 2.0
difficulty_weight = 1.5
waiting_time_weight = 1.0

# Create a directed graph for our ski resort
ski_resort = nx.DiGraph()

# Adding slopes - (graph, start, end, weather, difficulty)
add_slope(ski_resort, 'Peak', 'Intermediate Station', weather=0.7, difficulty=0.6)
add_slope(ski_resort, 'Intermediate Station', 'Base', weather=0.8, difficulty=0.3)
add_slope(ski_resort, 'Peak', 'Base', weather=0.5, difficulty=0.8)
add_slope(ski_resort, 'Intermediate Station', 'Lodge', weather=0.9, difficulty=0.2)
add_slope(ski_resort, 'Lodge', 'Base', weather=1.0, difficulty=0.1)

# Adding lifts - (graph, start, end, waiting_time)
add_lift(ski_resort, 'Base', 'Peak', waiting_time=10)
add_lift(ski_resort, 'Base', 'Intermediate Station', waiting_time=5)
add_lift(ski_resort, 'Lodge', 'Peak', waiting_time=7)

# Let's find a desirable path from the Peak to the Base
path = find_path(ski_resort, 'Peak', 'Base')
print("Recommended Path from Peak to Base:", path)

# Example to find a path from the Base back to the Peak, considering lift wait times
return_path = find_path(ski_resort, 'Base', 'Peak')
print("Recommended Path from Base back to Peak:", return_path)
