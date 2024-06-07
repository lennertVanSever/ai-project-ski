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
