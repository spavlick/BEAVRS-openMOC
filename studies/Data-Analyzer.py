import h5py
import numpy
from tester import *

f = h5py.File('results/pwru160c00-errors.h5', 'r')
keys = f['az'].keys()

angles = numpy.zeros(len(keys) / 3)
max_errors = numpy.zeros(len(keys) / 3)
mean_errors = numpy.zeros(len(keys) / 3)
kinf_errors = numpy.zeros(len(keys) / 3)
for key in keys:
    if "kinf" in key:
        num_azim = int(key.strip("az_kinf_num_azim = "))
        angles[num_azim / 4 - 1] = num_azim
        kinf_errors[num_azim / 4 - 1] = f['az'][key][...] * 10**5

for key in keys:
    if "max" in key:
        num_azim = int(key.strip("az_max_num_azim = "))
        max_errors[num_azim / 4 - 1] = f['az'][key][...] * 10**2

for key in keys:
    if "mean" in key:
        num_azim = int(key.strip("az_mean_num_azim = "))
        mean_errors[num_azim / 4 - 1] = f['az'][key][...] * 10**2

plotter([angles], [kinf_errors], "Azimuthal Angle Convergence Study", \
"Azimuthal Angles", "Error in K-effective [pcm]", 5, "pwru160c00-angles.png", 1)

plotter([angles, angles], [max_errors, mean_errors], "Relative Percent Pin Power Error", \
"Azimuthal Angles", "Pin Power Errors", 1, "pwru160c00-powers.png", 2, ['Max', 'Min'])
