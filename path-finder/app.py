from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from initialize_graph import create_ski_resort
from graph_utils import find_initial_path_with_time_constraint
import networkx as nx

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# http://0.0.0.0:5001/graph?weather_weight=2.0&difficulty_weight=1.5&waiting_time_weight=1.0
@app.route('/graph')
def graph():
    # Get weights from URL parameters or use defaults
    weather_weight = float(request.args.get('weather_weight', 2.0))
    difficulty_weight = float(request.args.get('difficulty_weight', 1.5))
    waiting_time_weight = float(request.args.get('waiting_time_weight', 1.0))
    
    weights = {
        'weather_weight': weather_weight,
        'difficulty_weight': difficulty_weight,
        'waiting_time_weight': waiting_time_weight
    }
    
    # Create the ski resort graph with the given weights
    ski_resort = create_ski_resort(weights)
    pos = nx.spring_layout(ski_resort)  # Layout for the node positions

    elements = {'nodes': [], 'edges': []}
    for node in ski_resort.nodes():
        elements['nodes'].append({
            'data': {'id': node},
            'position': {'x': int(1000 * pos[node][0]), 'y': int(1000 * pos[node][1])}
        })

    for source, target, data in ski_resort.edges(data=True):
        label = f"{data['type']} {data['time']}min"
        elements['edges'].append({
            'data': {
                'source': source,
                'target': target,
                'label': label
            }
        })

    return jsonify(elements)

@app.route('/find_path')
def find_path():
    # Get weights from URL parameters or use defaults
    weather_weight = float(request.args.get('weather_weight', 2.0))
    difficulty_weight = float(request.args.get('difficulty_weight', 1.5))
    waiting_time_weight = float(request.args.get('waiting_time_weight', 1.0))
    
    weights = {
        'weather_weight': weather_weight,
        'difficulty_weight': difficulty_weight,
        'waiting_time_weight': waiting_time_weight
    }
    
    # Create the ski resort graph with the given weights each time a request is made
    ski_resort = create_ski_resort(weights)
    
    # Get the start and end nodes along with the desired time from URL parameters
    start = request.args.get('start')
    end = request.args.get('end')
    desired_time_minutes = int(request.args.get('time', 0))
    
    # Find path using the provided utility function
    path, _ = find_initial_path_with_time_constraint(ski_resort, start, end, desired_time_minutes)
    return jsonify({'path': path})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)