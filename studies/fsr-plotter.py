import h5py
import numpy
import matplotlib as plt
from tester import *
import os.path

test = 'Flat Source Region Test'
strip_rings = 'Rings = '
strip_sectors = 'Sectors = '

x_axis = []
y_axis = []

assembly_list = ['pwru160c00','pwru240c00','pwru240w12','pwru310c00','pwru310w12']

f = h5py.File('results/' + assembly_list[4] + '-trackspacing-errors.h5', 'r')
keys = f[test].keys()
for key in keys:
    current_value = float(key.strip(strip_rings))
    x_axis.append(current_value)
x_axis.sort()

keys = f[test].keys()
for key in keys:
    current_value = float(key.strip(strip_sectors))
    y_axis.append(current_value)
f.close()
y_axis.sort()


