import numpy as np
import sys
from matplotlib.image import imread

def img2feat(filename):
	img = imread(filename)
	vals = []
	for row in range(0, len(img[:, 1, 0])):
		for col in range(0, len(img[0, :, 0])):
			val = ("0x%02x%02x%02x" 
			% (int(img[row, col, 0]*255),
			   int(img[row, col, 1]*255),
			   int(img[row, col, 2]*255)))
			vals.append(val)

	vals_string = ', '.join(vals)
	return vals_string

if __name__ == '__main__':
	img2feat('imagename.png')
