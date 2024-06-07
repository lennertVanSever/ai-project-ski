# AI Ski Map

The goal of this project is to generate the ideal pathway on a ski map for skiers based on their preferences. For example if you want to have a ski day without difficult slopes, good weather conditions and low waiting time, this app is for you

## How it works?

[Webcam data](https://www.skylinewebcams.com/en/webcam/italia/lombardia/brescia/passo-del-tonale/timelapse.html) and an AI algorithm is used to determine the waiting time for a lift. We use the same technology to determine the weather on a given slope. Further there is some static data like slope dificulty and lift duration taken from the website of ski resorts.

All of this data is transformed into a directional graph. Then the user can give some weights on how important the weather, difficulty and waiting time is. Then an ideal path is generated through a custom path finding algorithm.


## Determining waiting time slope

Through the YoloV8 library the amount of people are counted on a given webcam image of a ski lift. Then some simple math is applied to determine how long the waiting time is. There is some manual labour required to correctly crop 1 webcam image and also to determine the average cycling time of a given lift

```python
from ultralytics import YOLO
import numpy as np
from PIL import Image
import os
import tempfile

model = YOLO("yolov8s.pt")

PEOPLE_PER_GROUP = 4
CYCLE_TIME = 1


def calculate_wait_time(num_people, people_per_group, cycle_time):
    num_groups = np.ceil(num_people / people_per_group)
    wait_time_minutes = num_groups * cycle_time
    return wait_time_minutes


classes = [0, 1]
conf_thresh = 0.5
source = "./data"
temp_dir = tempfile.mkdtemp()


crop_start_x = 988
crop_start_y = 939


for file_name in os.listdir(source):
    if file_name.endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(source, file_name)
        img = Image.open(img_path)
        width, height = img.size

        if crop_start_x < width and crop_start_y < height:
            cropped_img = img.crop((crop_start_x, crop_start_y, width, height))
            cropped_img_path = os.path.join(temp_dir, file_name)
            cropped_img.save(cropped_img_path)


results = model.predict(source=temp_dir, save=True,
                        classes=classes, conf=conf_thresh)


for file_name, result in zip(os.listdir(temp_dir), results):
    num_people = len(result.boxes)
    wait_time = calculate_wait_time(num_people, PEOPLE_PER_GROUP, CYCLE_TIME)
    print(
        f'Estimated wait time for image {file_name}: {wait_time} minutes. Number of people: {num_people}')

```

Some examples of how people are counted

## Determining weather conditions

Throught the same library I tried to determine the weather but now by first training the model via manually labelling webcam photos. This didn't had the results that I was looking for, after doing some online research I also found that this is complex problem to solve

Weather.py
```python
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
```

## Pathfinding algorithm

Now that we have all the data generated or taken from a ski resort. It's time to bring it all together. First of all I used networkx as my graph library. It would go a bit to much into detail if I discuss the code in detail, if you want a more detailed look, go to the `./path-finder` folder. 

First of all a graph is created with the slopes and lifts as edges and the stations as nodes. For each there are some normalized data points like weather, waiting time and difficulty. Then there are some function to give the best path based on the preferences of waiting time, difficulty and waiting time. I spent a day trying to get some decent result with cyclical graphs so that you could say, desired ski time 3 hours but it went a bit above my knowledge of math.

## Interactive interface

As a final step, I made a small web app where you can try the ski map! It works by putting the python networkx logic on a flask backend and then making a frontend by using cytoscape. It's still very rough but it does work.

[DEMO](http://127.0.0.1:5500/graph/index.html)