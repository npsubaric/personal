from PIL import Image
import numpy as np

def remove_background(image):
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    
    # Apply thresholding to segment the foreground from the background
    threshold = 200  # Adjust the threshold value as needed
    binary_image = grayscale_image.point(lambda x: 0 if x < threshold else 255, '1')
    
    # Invert the binary image to get the background as white and foreground as black
    inverted_binary_image = Image.eval(binary_image, lambda x: 255 - x)
    
    # Use the inverted binary image as a mask to remove the background
    transparent_image = image.copy()
    transparent_image.putalpha(inverted_binary_image)
    
    return transparent_image

def ordered_dither(im, D4):
    if im.max() != 0:
        im = (15 * (im / im.max())).astype(np.uint8)
    else:
        im = np.zeros_like(im)
    h, w = im.shape
    im_out = np.zeros((4 * h, 4 * w), dtype=np.uint8)
    x, y = 0, 0
    for i in range(h):
        for j in range(w):
            im_out[x:x + 4, y:y + 4] = 255 * (D4 < im[i, j])
            y = (y + 4) % (4 * w)
        x = (x + 4) % (4 * h)
    return im_out

def convert_to_bitmap(input_image_path, output_image_path):
    # Open the input image
    image = Image.open(input_image_path)
    
    # Remove the background
    transparent_image = remove_background(image)
    
    # Convert the transparent image to grayscale
    grayscale_image = transparent_image.convert('L')
    
    # Define the Bayer matrix
    D4 = np.array([[ 0,  8,  2, 10],
                   [12,  4, 14,  6],
                   [ 3, 11,  1,  9],
                   [15,  7, 13,  5]], dtype=np.uint8)
    
    # Apply ordered dithering
    halftoned_image = ordered_dither(np.asarray(grayscale_image), D4)
    
    # Convert numpy array to PIL Image
    output_image = Image.fromarray(halftoned_image)
    
    # Save the output image as a bitmap
    output_image.save(output_image_path)

# Example usage:
input_image_path = 'stick_figure_coco.jpg'
output_image_path = 'stick_figure_coco.bmp'
convert_to_bitmap(input_image_path, output_image_path)