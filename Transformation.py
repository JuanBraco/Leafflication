import matplotlib.pyplot as plt
from plantcv import plantcv as pcv
from plantcv.parallel import WorkflowInputs
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import glob
import cv2
import numpy as np

def crop_coords(img):
    """
    Crop ROI from image.
    """
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    _, breast_mask = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    cnts, _ = cv2.findContours(breast_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = max(cnts, key = cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    return (x, y, w, h)


def main():

    # train_images = glob.glob("./images/Apple/Apple_healthy/*")

    args = WorkflowInputs(
        images=["./images/Apple/Apple_scab/image (1).JPG"],
        names="image",
        result="example_results_oneimage_file.csv",
        outdir="./output",
        writeimg=False,
        debug="plot"
    )
    pcv.params.debug = args.debug
    pcv.params.text_size = 20
    pcv.params.text_thickness = 20

    img, path, filename = pcv.readimage(filename=args.image)

    cs = pcv.visualize.colorspaces(rgb_img=img, original_img=False)


    gray_img = pcv.rgb2gray_lab(rgb_img=img, channel="a")

    # Instead of setting a manual threshold, try an automatic threshold method such as Otsu
    mask_a = pcv.threshold.otsu(gray_img=gray_img, object_type="dark")
    mask_b = pcv.threshold.mean(gray_img=gray_img, ksize=100, offset=3, object_type="dark")

    cleaner_mask = pcv.fill(bin_img=mask_a, size=50)

    win = 24
    thresh = 90

    homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = pcv.homology.acute(img=img, 
                                                                               mask=mask_a, win=win, 
                                                                               threshold=thresh)



    gray_img_flat = gray_img.flatten()

    plt.hist(gray_img_flat, bins=30, color='gray', edgecolor='black')

    # Add titles and labels (optional)
    plt.title('Grayscale Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')

    # Show the plot
    plt.show()

    # Visualize a histogram of the grayscale values to identify signal related to the plant and the background
    hist = pcv.visualize.histogram(img=gray_img, bins=30)

    # fig, axs = plt.subplots(1, 3)

    
    # axs[0].imshow(img, cmap='gray')

    # bin_gauss1 = pcv.threshold.gaussian(gray_img=gray_img, ksize=2000, offset=15,
    #                                     object_type='dark')

    # gaussian_img = pcv.gaussian_blur(img=bin_gauss1, ksize=(11, 11), sigma_x=0, sigma_y=None)

    # axs[1].imshow(bin_gauss1, cmap='gray')
    # axs[2].imshow(gaussian_img, cmap='gray')
    # plt.show()

    # _, axs = plt.subplots(2, 5, figsize=(16, 8))
    # axs = axs.flatten()
    # images = []
    # for img_path, ax in zip(train_images[:10], axs):
    #     img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    #     (x, y, w, h) = crop_coords(img)
    #     # Create a Rectangle patch
    #     rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
    #     # Add the patch to the Axes
    #     ax.add_patch(rect)
    #     img_cropped = img[y:y+h, x:x+w]
    #     images.append(img_cropped)
    #     ax.imshow(img, cmap="bone")

    # plt.savefig("rectangles.png")
    # plt.show()

if __name__ == "__main__":
    main()
