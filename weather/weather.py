from ultralytics import YOLO
import yaml
import os

# Define your dataset directory and classes
dataset_dir = os.path.join(os.path.dirname(__file__), 'data')
classes = ['misty', 'clear']

# Define the paths to save configuration files
data_yaml_path = os.path.join(dataset_dir, 'data.yaml')
model_yaml_path = os.path.join(dataset_dir, 'model.yaml')

# Prepare the data.yaml file
data_yaml_content = {
    'train': os.path.join(dataset_dir, 'train/images'),
    'val': os.path.join(dataset_dir, 'val/images'),
    'nc': len(classes),
    'names': classes
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
model = YOLO(model_yaml_path)

# Start training
model.train(data_yaml_path)
