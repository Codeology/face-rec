import PIL
from PIL import Image, ImageChops
import numpy as np
import os

def diffcalc(a, b):
    img1 = Image.open(a).convert('RGB')
    img2 = Image.open(b).convert('RGB')
    diff = ImageChops.difference(img1, img2)
    newdiff = ImageChops.difference(diff, img1)
    return newdiff
