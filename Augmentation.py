import sys # to access the system
import os
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np


# def load_images_from_directory(dir_path):
#     images_list = []
#     for image_filename in os.listdir(dir_path):
#         image_path = os.path.join(dir_path, image_filename)
#         try:
#             with Image.open(image_path) as img:
#                 images_list.append(image_path)  # The file is an image
#         except IOError:
#             pass  # This file is not an image
#     return images_list

def main():
    if len(sys.argv) != 2:
        raise AssertionError("Incorrect number of arguments")
    
    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The directory {image_path} does not exist.")

    image =cv2.imread(image_path)
    height, width, channels = image.shape
    print(height, width, channels)
    rotation_matrix = cv2.getRotationMatrix2D((width/2,height/2),45,1)
    rotated_image = cv2.warpAffine(image,rotation_matrix,(width,height))
    bright = np.ones(image.shape , dtype="uint8") * 70
    brightdecrease = cv2.subtract(image,bright)
    brightincrease = cv2.add(image,bright)
    flip = cv2.flip(image,3)

    combined_image = np.hstack((image, rotated_image, brightdecrease, brightincrease, flip))
    cv2.imshow('first' , combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # print(total_images)

    # labels = list(directory_images.keys())
    # sizes = [len(images) for images in directory_images.values()]

    # fig, ax = plt.subplots()
    # ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    # plt.show()
    


if __name__ == "__main__":
    main()
