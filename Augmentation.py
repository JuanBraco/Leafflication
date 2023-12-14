import sys
import os
import Augmentor


def main():
    if len(sys.argv) != 2:
        raise AssertionError("Incorrect number of arguments")

    dir_path = sys.argv[1]

    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"The directory {dir_path} does not exist.")

    for sub_dir_name in os.listdir(dir_path):
        sub_dir_path = os.path.join(dir_path, sub_dir_name)
        output_dir_path = os.path.join("../../../" + dir_path + "_augmented",
                                       sub_dir_name)

        p = Augmentor.Pipeline(source_directory=sub_dir_path,
                               output_directory=output_dir_path)
        p.rotate_without_crop(
            probability=.5,
            max_left_rotation=90,
            max_right_rotation=90,
            expand=True)
        p.zoom(
            probability=.3,
            min_factor=.5,
            max_factor=1.5)
        p.skew(
            probability=.3,
            magnitude=.35)
        p.random_brightness(
            probability=.5,
            min_factor=.2,
            max_factor=2)
        p.flip_random(probability=.5)
        p.crop_random(probability=.4, percentage_area=0.5)
        p.sample(1600)


if __name__ == "__main__":
    main()
