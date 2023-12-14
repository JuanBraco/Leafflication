import sys # to access the system
import os
from PIL import Image
import matplotlib.pyplot as plt

def load_images_from_directory(dir_path):
    images_list = []
    for image_filename in os.listdir(dir_path):
        image_path = os.path.join(dir_path, image_filename)
        try:
            with Image.open(image_path) as img:
                images_list.append(image_path)  # The file is an image
        except IOError:
            pass  # This file is not an image
    return images_list

def main():
    if len(sys.argv) != 2:
        raise AssertionError("Incorrect number of arguments")
    
    dir_path = sys.argv[1]

    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"The directory {dir_path} does not exist.")

    directory_images = {}
    total_images = 0

    for sub_dir_name in os.listdir(dir_path):
        sub_dir_path = os.path.join(dir_path, sub_dir_name)
        if os.path.isdir(sub_dir_path):  # Check if it's a directory
            images = load_images_from_directory(sub_dir_path)
        if images:
            directory_images[sub_dir_name] = images
            total_images += len(images)


    print(total_images)

    labels = list(directory_images.keys())
    sizes = [len(images) for images in directory_images.values()]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.show()
    


if __name__ == "__main__":
    main()
