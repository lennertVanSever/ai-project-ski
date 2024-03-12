from ultralytics import YOLO
import numpy as np

model = YOLO("yolov8s.pt")

PEOPLE_PER_GROUP = 4
CYCLE_TIME = 1

def calculate_wait_time(num_people, people_per_group, cycle_time):
    # Calculate the number of groups in the line
    num_groups = np.ceil(num_people / people_per_group)

    # Calculate wait time based on the number of groups and cycle time
    wait_time_minutes = num_groups * cycle_time
    return wait_time_minutes

# Detect objects from classes 0 and 1 only
classes = [0, 1]

# Set the confidence threshold
conf_thresh = 0.5

# Set the source of the input data (e.g., image file, video file, or folder containing images)
source = "./data"

# Call the predict function with the specified parameters
results = model.predict(source=source, save=False, classes=classes, conf=conf_thresh)


for result in results:
    num_people = len(result.boxes)
    wait_time = calculate_wait_time(num_people, PEOPLE_PER_GROUP, CYCLE_TIME)
    print(f'Estimated wait time for image: {wait_time} minutes. Number of people: {num_people}')

