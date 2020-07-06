from PIL import Image as pil
import numpy as np

PATH = "rarity.png"
CONTRAST_THRESHOLD = 96  # range (0 - 255)
GAMMA = 2

def get_grey_value(pixel, gamma=2):
    """converts colored pixel into grey scale\n1, 3 and 4 length tuples supported"""
    
    return pixel[0] if len(pixel) == 1 else ((pixel[0]**gamma + pixel[1]**gamma + pixel[2]**gamma)/3)**(1/gamma) if len(pixel) == 3 else ((pixel[0]**gamma + pixel[1]**gamma + pixel[2]**gamma)/3)**(1/gamma) * pixel[3] / 255

def convert_to_binary(image, threshold, gamma):
    """returns 2D array of 0's and 1's\n0 if pixel < threshold 1 otherwise"""

    return np.array([0 if get_grey_value(image.getpixel((i, j)), gamma) < threshold else 1 for j in range(image.size[1]) for i in range(image.size[0])]).reshape(image.size[1], image.size[0])

def split_array(array, w, h):
    """returns w x h blocks of array\nArray is resized if not divisible"""
    
    # if width is not divisible extend by adding 0's
    array = np.concatenate((array, np.array([0 for i in range(array.shape[1] * (w - array.shape[0] % w))]).reshape(w - array.shape[0] % w, array.shape[1])), 0) if array.shape[0] % w != 0 else array
    
    # if height is not divisible extend by adding 0's
    array = np.concatenate((array, np.array([0 for i in range(array.shape[0] * (h - array.shape[1] % h))]).reshape(array.shape[0], h - array.shape[1] % h)), 1) if array.shape[1] % h != 0 else array
    
    # convert 2D array into 4D with given block dimensions
    return np.array([array[i*h: (i+1)*h, j*w:(j+1)*w] for (i, j) in np.ndindex(int(array.shape[0] / h), int(array.shape[1] / w))]).reshape(int(array.shape[0] / h), int(array.shape[1] / w), h, w)

# convert image to 2D array of (2x4) blocks
s = split_array(convert_to_binary(pil.open(PATH), CONTRAST_THRESHOLD, GAMMA), 2, 4)

# convert into characters and write to file
open("output.txt", 'w', encoding="utf-8").write(''.join(k for k in ['\n' if j == s.shape[1] else chr(int("2800", 16) + s[i][j][0][0]*1 + s[i][j][1][0]*2 + s[i][j][2][0]*4 + s[i][j][0][1]*8 + s[i][j][1][1]*16 + s[i][j][2][1]*32 + s[i][j][3][0]*64 + s[i][j][3][1]*128) if s[i][j][0][0]|s[i][j][1][0]|s[i][j][2][0]|s[i][j][0][1]|s[i][j][1][1]|s[i][j][2][1]|s[i][j][3][0]|s[i][j][3][1] != 0 else chr(int("2005", 16))*3 for i in range(s.shape[0]) for j in range(s.shape[1] + 1)]))
