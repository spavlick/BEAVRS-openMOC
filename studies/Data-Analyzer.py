import h5py
import numpy
from tester import *

assembly = raw_input("Assembly?")

f = h5py.File('results/' + assembly + '-errors.h5', 'r')
keys_az = f['az'].keys()

angles = numpy.zeros(len(keys_az) / 3)
az_max_errors = numpy.zeros(len(keys_az) / 3)
az_mean_errors = numpy.zeros(len(keys_az) / 3)
az_kinf_errors = numpy.zeros(len(keys_az) / 3)
for key in keys_az:
    if "kinf" in key:
        num_azim = int(key.strip("az_kinf_num_azim = "))
        angles[num_azim / 4 - 1] = num_azim
        az_kinf_errors[num_azim / 4 - 1] = f['az'][key][...] * 10**5

for key in keys_az:
    if "max" in key:
        num_azim = int(key.strip("az_max_num_azim = "))
        az_max_errors[num_azim / 4 - 1] = f['az'][key][...] * 10**2

for key in keys_az:
    if "mean" in key:
        num_azim = int(key.strip("az_mean_num_azim = "))
        az_mean_errors[num_azim / 4 - 1] = f['az'][key][...] * 10**2

plotter([angles], [az_kinf_errors], "Azimuthal Angle Convergence Study (" + assembly + " assembly)", \
"Azimuthal Angles", "Error in K-effective [pcm]", max(angles), max(az_kinf_errors) + 10, assembly + "-kinf-angles.png", 1)

plotter([angles, angles], [az_max_errors, az_mean_errors], "Relative Percent Pin Power Error (" + assembly + " assembly)", \
"Azimuthal Angles", "Pin Power Errors", max(angles), max(az_max_errors) + .2, assembly + "-powers-angles.png", 2, ['Max', 'Mean'])

keys_ts = f['ts'].keys()

tracks = numpy.zeros(len(keys_ts) / 3)
ts_max_errors = numpy.zeros(len(keys_ts) / 3)
ts_mean_errors = numpy.zeros(len(keys_ts) / 3)
ts_kinf_errors = numpy.zeros(len(keys_ts) / 3)
counter = 0
for key in keys_ts:
    if "kinf" in key:
        track_spacing = float(key.strip("ts_kinf_track_spacing = "))
        tracks[counter] = track_spacing
        ts_kinf_errors[counter] = f['ts'][key][...] * 10**5
        counter += 1

counter = 0
for key in keys_ts:
    if "max" in key:
        track_spacing = float(key.strip("ts_max_track_spacing = "))
        ts_max_errors[counter] = f['ts'][key][...] * 10**2
        counter += 1

counter = 0
for key in keys_ts:
    if "mean" in key:
        track_spacing = float(key.strip("ts_mean_track_spacing = "))
        ts_mean_errors[counter] = f['ts'][key][...] * 10**2
        counter += 1

plotter([tracks], [ts_kinf_errors], "Track Spacing Convergence Study (" + assembly + " assembly)", \
"Track Spacing", "Error in K-effective [pcm]", max(tracks), max(ts_kinf_errors) + 10, assembly + "-kinf-tracks.png", 1)

plotter([tracks, tracks], [ts_max_errors, ts_mean_errors], "Relative Percent Pin Power Error (" + assembly + " assembly)", \
"Track Spacing", "Pin Power Errors", max(tracks), max(ts_max_errors) + .2, assembly + "-powers-tracks.png", 2, ['Max', 'Mean'])
