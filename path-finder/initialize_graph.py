import networkx as nx
from graph_utils import add_slope, add_lift

def create_ski_resort(weights):
    ski_resort = nx.DiGraph()

    add_slope(ski_resort, 'Peak', 'Intermediate Station', weather=0.7, difficulty=0.6, average_time=15, weights=weights)
    add_slope(ski_resort, 'Intermediate Station', 'Base', weather=0.8, difficulty=0.3, average_time=10, weights=weights)
    add_slope(ski_resort, 'Peak', 'Base', weather=0.5, difficulty=0.8, average_time=20, weights=weights)
    add_slope(ski_resort, 'Intermediate Station', 'Lodge', weather=0.9, difficulty=0.2, average_time=8, weights=weights)
    add_slope(ski_resort, 'Lodge', 'Base', weather=1.0, difficulty=0.1, average_time=5, weights=weights)
    add_slope(ski_resort, 'Lodge', 'Peak', weather=0.6, difficulty=0.5, average_time=12, weights=weights)
    add_slope(ski_resort, 'Peak', 'Viewpoint', weather=0.4, difficulty=0.9, average_time=18, weights=weights)
    add_slope(ski_resort, 'Viewpoint', 'Base', weather=0.7, difficulty=0.4, average_time=14, weights=weights)
    add_slope(ski_resort, 'Viewpoint', 'Lodge', weather=0.8, difficulty=0.3, average_time=9, weights=weights)
    add_slope(ski_resort, 'Top Ridge', 'Peak', weather=0.5, difficulty=0.7, average_time=16, weights=weights)
    add_slope(ski_resort, 'Top Ridge', 'Viewpoint', weather=0.6, difficulty=0.8, average_time=20, weights=weights)

    # Adding many more lifts
    add_lift(ski_resort, 'Base', 'Peak', waiting_time=10, average_time=15, weights=weights)
    add_lift(ski_resort, 'Base', 'Intermediate Station', waiting_time=5, average_time=10, weights=weights)
    add_lift(ski_resort, 'Lodge', 'Peak', waiting_time=7, average_time=12, weights=weights)
    add_lift(ski_resort, 'Base', 'Top Ridge', waiting_time=8, average_time=18, weights=weights)
    add_lift(ski_resort, 'Lodge', 'Viewpoint', waiting_time=6, average_time=11, weights=weights)
    add_lift(ski_resort, 'Intermediate Station', 'Top Ridge', waiting_time=9, average_time=14, weights=weights)


    return ski_resort
