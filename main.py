# Load images from directory TestImages and save to folder TestImagesPNG (also convert to PNG)

# Imported libraries and such
import os
import cv2 as cv
import openslide
import PIL
from PIL import Image
import glob
from tqdm import tqdm

# Calc_scale
def calc_scale(full_image):
    import math

    dim_before = full_image.dimensions
    num_pix = dim_before[0] * dim_before[1]
    max_pix = 21708 * 11059
    scale = math.sqrt(max_pix / num_pix)
    return scale

# Slide_thumbnail
def get_slide_thumbnail(slide, size):
    downsample = max(*[dim / thumb for dim, thumb in zip(slide.dimensions, size)])
    level = slide.get_best_level_for_downsample(downsample)
    if level < 3:
        level = 3
    tile = slide.read_region((0,0), level, slide.level_dimensions[level])
    bg_color = '#' + slide.properties.get(u'openslide.background-color', 'ffffff')
    thumb = Image.new('RGB', tile.size, bg_color)
    thumb.paste(tile, None, tile)
    thumb.thumbnail(size, Image.ANTIALIAS)
    return thumb

# Save images as png - save_dir="/home/andrewaever/Desktop/TestImagePng/"
def downscaleImageToDisc(dir="/home/andrewaever/Desktop/TestImages/*.ndpi", save_dir="/home/andrewaever/Desktop/TestImagesPng/", offset=0, save_format="png"):
    imageNames = glob.glob(dir)
    numImages = len(imageNames)
    print("Detected :", numImages, " images in the folder.")

    # Set count number to the next number in line based on how many images already processed -
    # Possibly implementing lines that reads the max number in the folder and set count = max
    count = 0

    for name in tqdm(imageNames[offset:]):
        slide = openslide.OpenSlide(name)
        scale = calc_scale(slide)
        img = get_slide_thumbnail(slide=slide, size=(int(slide.dimensions[0] * scale), int(slide.dimensions[1] * scale)))
        img.save(save_dir + str(count), "png")
        count += 1

downscaleImageToDisc()