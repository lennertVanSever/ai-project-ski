from ultralytics import YOLO
import yaml
import os


dataset_dir = os.path.join(os.path.dirname(__file__), 'data')
classes = ['misty', 'clear']


data_yaml_path = os.path.join(dataset_dir, 'data.yaml')
model_yaml_path = os.path.join(dataset_dir, 'model.yaml')
data_yaml_content = os.path.join(dataset_dir, 'content.yaml')

nc = len(classes)


model_yaml_content = {
    'nc': nc,
    'depth_multiple': 0.33,
    'width_multiple': 0.50,

    'backbone': [

        [-1, 1, 'Conv', [32, 3, 1]],
        [-1, 1, 'C3', [64, 3, 2]],

    ],

    'head': [

        [-1, 3, 'Conv', [128, 3, 1]],
        [-1, 1, 'Detect', [nc, 'anchors']],

    ],
}


with open(data_yaml_path, 'w') as file:
    yaml.dump(data_yaml_content, file, sort_keys=False)


model_yaml_content = {

    'nc': len(classes),
    'depth_multiple': 0.33,
    'width_multiple': 0.50,
}


with open(model_yaml_path, 'w') as file:
    yaml.dump(model_yaml_content, file, sort_keys=False)


model = YOLO(model_yaml_path, task='detect')


model.train(data_yaml_path)
