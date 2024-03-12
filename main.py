import cv2
import numpy as np
from matplotlib import pyplot as plt

# Parameters (Please adjust these parameters based on the lift's actual operation)
people_per_group = 4  # Average number of people per ski lift chair/group
cycle_time = 2  # Time it takes for one cycle of the lift in minutes
path_to_images = './data/'  # Path to the directory with images

def count_people(image_path):
    print(image_path)
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use a simple threshold to attempt to isolate people
    _, thresh_img = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours which might correspond to people
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours that are not likely to be people
    min_contour_area = 100  # This is an estimate; it needs to be calibrated for the image
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # For now, we assume each contour corresponds to one person
    num_people = len(large_contours)

    # Optionally display the threshold image with contours
    cv2.drawContours(img, large_contours, -1, (0, 255, 0), 3)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

    return num_people

def calculate_wait_time(num_people, people_per_group, cycle_time):
    # Calculate the number of groups in the line
    num_groups = np.ceil(num_people / people_per_group)

    # Calculate wait time based on the number of groups and cycle time
    wait_time_minutes = num_groups * cycle_time
    return wait_time_minutes

# Analyze each image and print estimated wait time
image_files = ['image1.png', 'image2.png', 'image3.png', 'image4.png', 'image5.png', 'image6.png']
for image_file in image_files:
    num_people = count_people(path_to_images + image_file)
    wait_time = calculate_wait_time(num_people, people_per_group, cycle_time)
    print(f'Estimated wait time for {image_file}: {wait_time} minutes. Number of people {num_people}')
