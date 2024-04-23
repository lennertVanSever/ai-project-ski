from ultralytics import YOLO
import yaml
import os

# Define your dataset directory and classes
dataset_dir = os.path.join(os.path.dirname(__file__), 'data')
classes = ['misty', 'clear']

# Define the paths to save configuration files
data_yaml_path = os.path.join(dataset_dir, 'data.yaml')
model_yaml_path = os.path.join(dataset_dir, 'model.yaml')
data_yaml_content = os.path.join(dataset_dir, 'content.yaml')

nc = len(classes)


# Prepare the data.yaml file
model_yaml_content = {
    'nc': nc,
    'depth_multiple': 0.33,  # model depth multiple
    'width_multiple': 0.50,  # layer channel multiple
    # Example backbone - You need to replace this with actual YOLOv8 structure
    'backbone': [
        # [from, number, module, args]
        [-1, 1, 'Conv', [32, 3, 1]],
        [-1, 1, 'C3', [64, 3, 2]],
        # ... more layers ...
    ],
    # Example head - You need to replace this with actual YOLOv8 structure
    'head': [
        # [from, number, module, args]
        [-1, 3, 'Conv', [128, 3, 1]],
        [-1, 1, 'Detect', [nc, 'anchors']],
        # ... more layers ...
    ],
}

# Write data configuration to yaml file
with open(data_yaml_path, 'w') as file:
    yaml.dump(data_yaml_content, file, sort_keys=False)

# Prepare the model.yaml content for your custom dataset
model_yaml_content = {
    # ... Model configuration goes here, e.g., number of classes, anchors, etc. ...
    'nc': len(classes),
    'depth_multiple': 0.33,  # model depth multiple
    'width_multiple': 0.50,  # layer channel multiple
}

# Write model configuration to yaml file
with open(model_yaml_path, 'w') as file:
    yaml.dump(model_yaml_content, file, sort_keys=False)

# Initialize YOLO model for training
model = YOLO(model_yaml_path, task='detect')

# Start training
model.train(data_yaml_path)
