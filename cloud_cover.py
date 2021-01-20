from PIL import Image
import numpy as np
from numpy import asarray
from skimage.filters.rank import median
from skimage.morphology import disk
from skimage import draw, io

# Next steps: Adjust threshold for haze index (guess and check). Also take a look at software to locate sun + remove brightest points in image.
# In addition, begin compiling dataset.

def main():

    sky_trimmed = load_and_trim('C:\\Users\\David\\Documents\\Research\\sky_camera_images\\2020-02-13-14-30-0.jpg')
    #sky_trimmed = load_and_trim('C:\\Users\\David\\Documents\\Research\\sky_camera_images\\2019-05-21-09-55-0.jpg')
    haze_index_im = process_image_haze_index(sky_trimmed)
    rb_ratio_im = process_image_rb_ratio(sky_trimmed)
    print(calculate_cloud_cover(rb_ratio_im))

    io.imsave("sky_trimmed.jpg", sky_trimmed)
    io.imsave("rb_ratio_no_haze.jpg", rb_ratio_im)
    io.imsave("haze.jpg", haze_index_im)

def load_and_trim(filename):
    sky = io.imread(filename)
    sky_trimmed = trim_outer_circle(sky)
    return sky_trimmed

def trim_outer_circle(sky):
    x1_trim = 300
    x2_trim = 2280

    width = sky.shape[0]
    height = sky.shape[1]
    center_on_width = int(width / 2)
    center_on_height = int(height / 2)
    circle_radius = 971

    sky_circle = np.zeros((width, height), dtype=np.uint8)
    rr, cc = draw.circle(center_on_width, center_on_height, circle_radius)
    sky_circle[rr, cc] = 1
    sky_trimmed = sky.copy()
    sky_trimmed[sky_circle == 0] = 0
    return sky_trimmed[:, x1_trim: x2_trim]

def process_image_rb_ratio(image):
    rb_ratio = image[..., 0] / image[..., 2]
    threshold = 0.9
    rb_ratio[rb_ratio > threshold] = 255
    rb_ratio[rb_ratio <= threshold] = 0
    return median(rb_ratio, disk(10))

def process_image_haze_index(image):
    b = image[..., 0]
    g = image[..., 1]
    r = image[..., 2]
    haze_index = (((r + b) / 2) - g) / (((r + b) / 2) + g)
    haze_index[haze_index > 0] = 255
    haze_index[haze_index <= 0] = 0
    #return haze_index
    return median(haze_index, disk(10))

def calculate_cloud_cover(image):
    circle_radius = 971
    pixels_in_circle = int(np.pi * (circle_radius ** 2))
    white = 255
    flattened_image = image.flatten()
    white_pixels = np.sum(flattened_image == white)
    cloud_percentage = white_pixels / pixels_in_circle * 100
    return cloud_percentage



if __name__ == "__main__":
    main()