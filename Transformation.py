from plantcv import plantcv as pcv
from plantcv.parallel import WorkflowInputs


def main():
    args = WorkflowInputs(
        images=["/mnt/nfs/homes/jde-la-f/E42/python/Leafflication/images/Apple/Apple_healthy/image (2).JPG"],
        names="image",
        result="example_results_oneimage_file.csv",
        outdir="./output",
        writeimg=False,
        debug="plot"
    )
    pcv.params.debug = args.debug
    pcv.params.dpi = 100
    pcv.params.text_size = 20
    pcv.params.text_thickness = 20

    img, path, filename = pcv.readimage(filename=args.image)

    gray_img = pcv.rgb2gray_hsv(rgb_img=img, channel="s")

    # Adaptive threshold with different parameters
    bin_gauss1 = pcv.threshold.gaussian(gray_img=gray_img, ksize=250, offset=15,
                                        object_type='dark')

    bin_gauss1 = pcv.threshold.gaussian(gray_img=gray_img, ksize=25, offset=5,
                                        object_type='dark')

    bin_gauss1 = pcv.threshold.gaussian(gray_img=gray_img, ksize=2000, offset=15,
                                        object_type='dark')

    gaussian_img = pcv.gaussian_blur(img=bin_gauss1, ksize=(11, 11), sigma_x=0, sigma_y=None)


if __name__ == "__main__":
    main()
