import h5py
import numpy
from tester import *

assembly1 = 'pwru160c00'
assembly2 = 'pwru240w12'

f = h5py.File('results/' + assembly1 + '-errors.h5', 'r')
keys_az = f['az'].keys()

angles = numpy.zeros(len(keys_az) / 3)
az_max_errors1 = numpy.zeros(len(keys_az) / 3)
az_mean_errors1 = numpy.zeros(len(keys_az) / 3)
az_kinf_errors1 = numpy.zeros(len(keys_az) / 3)

for key in keys_az:
    if "kinf" in key:
        num_azim = int(key.strip("az_kinf_num_azim = "))
        angles[num_azim / 4 - 1] = num_azim
        az_kinf_errors1[num_azim / 4 - 1] = f['az'][key][...] * 10**5

for key in keys_az:
    if "max" in key:
        num_azim = int(key.strip("az_max_num_azim = "))
        az_max_errors1[num_azim / 4 - 1] = f['az'][key][...] * 10**2

for key in keys_az:
    if "mean" in key:
        num_azim = int(key.strip("az_mean_num_azim = "))
        az_mean_errors1[num_azim / 4 - 1] = f['az'][key][...] * 10**2


keys_ts = f['ts'].keys()

tracks = numpy.zeros(len(keys_ts) / 3)
ts_max_errors1 = numpy.zeros(len(keys_ts) / 3)
ts_mean_errors1 = numpy.zeros(len(keys_ts) / 3)
ts_kinf_errors1 = numpy.zeros(len(keys_ts) / 3)
counter = 0
for key in keys_ts:
    if "kinf" in key:
        track_spacing = float(key.strip("ts_kinf_track_spacing = "))
        tracks[counter] = track_spacing
        ts_kinf_errors1[counter] = f['ts'][key][...] * 10**5
        counter += 1

counter = 0
for key in keys_ts:
    if "max" in key:
        track_spacing = float(key.strip("ts_max_track_spacing = "))
        ts_max_errors1[counter] = f['ts'][key][...] * 10**2
        counter += 1

counter = 0
for key in keys_ts:
    if "mean" in key:
        track_spacing = float(key.strip("ts_mean_track_spacing = "))
        ts_mean_errors1[counter] = f['ts'][key][...] * 10**2
        counter += 1

f.close()

f = h5py.File('results/' + assembly2 + '-errors.h5', 'r')
keys_az = f['az'].keys()

az_max_errors2 = numpy.zeros(len(keys_az) / 3)
az_mean_errors2 = numpy.zeros(len(keys_az) / 3)
az_kinf_errors2 = numpy.zeros(len(keys_az) / 3)

for key in keys_az:
    if "kinf" in key:
        num_azim = int(key.strip("az_kinf_num_azim = "))
        az_kinf_errors2[num_azim / 4 - 1] = f['az'][key][...] * 10**5

for key in keys_az:
    if "max" in key:
        num_azim = int(key.strip("az_max_num_azim = "))
        az_max_errors2[num_azim / 4 - 1] = f['az'][key][...] * 10**2

for key in keys_az:
    if "mean" in key:
        num_azim = int(key.strip("az_mean_num_azim = "))
        az_mean_errors2[num_azim / 4 - 1] = f['az'][key][...] * 10**2


keys_ts = f['ts'].keys()

ts_max_errors2 = numpy.zeros(len(keys_ts) / 3)
ts_mean_errors2 = numpy.zeros(len(keys_ts) / 3)
ts_kinf_errors2 = numpy.zeros(len(keys_ts) / 3)
counter = 0
for key in keys_ts:
    if "kinf" in key:
        track_spacing = float(key.strip("ts_kinf_track_spacing = "))
        ts_kinf_errors2[counter] = f['ts'][key][...] * 10**5
        counter += 1

counter = 0
for key in keys_ts:
    if "max" in key:
        track_spacing = float(key.strip("ts_max_track_spacing = "))
        ts_max_errors2[counter] = f['ts'][key][...] * 10**2
        counter += 1

counter = 0
for key in keys_ts:
    if "mean" in key:
        track_spacing = float(key.strip("ts_mean_track_spacing = "))
        ts_mean_errors2[counter] = f['ts'][key][...] * 10**2
        counter += 1

f.close()



plotter([angles, angles], [az_kinf_errors1, az_kinf_errors2], "Azimuthal Angle Convergence Study", \
"Azimuthal Angles", "Error in K-effective [pcm]", max(angles), max(az_kinf_errors1) + 10, "kinf-angles.png", 2, legend = ['Without BP', 'With BP'])

plotter([angles, angles], [az_max_errors1, az_mean_errors1], "Relative Percent Pin Power Error Without BP", \
"Azimuthal Angles", "Pin Power Errors", max(angles), max(az_max_errors1) + .2, assembly1 + "-powers-angles.png", 2, legend = ['Max', 'Mean'])

plotter([angles, angles], [az_max_errors2, az_mean_errors2], "Relative Percent Pin Power Error With BP", \
"Azimuthal Angles", "Pin Power Errors", max(angles), max(az_max_errors2) + .2, assembly2 + "-powers-angles.png", 2, legend = ['Max', 'Mean'])

plotter([tracks,tracks], [ts_kinf_errors1, ts_kinf_errors2], "Track Spacing Convergence Study", \
"Track Spacing", "Error in K-effective [pcm]", max(tracks), max(ts_kinf_errors1) + 10, "kinf-tracks.png", 2, legend = ['Without BP', 'With BP'])

plotter([tracks, tracks], [ts_max_errors1, ts_mean_errors1], "Relative Percent Pin Power Error Without BP", \
"Track Spacing", "Pin Power Errors", max(tracks), max(ts_max_errors1) + .2, assembly1 + "-powers-tracks.png", 2, legend = ['Max', 'Mean'])

plotter([tracks, tracks], [ts_max_errors2, ts_mean_errors2], "Relative Percent Pin Power Error With BP", \
"Track Spacing", "Pin Power Errors", max(tracks), max(ts_max_errors2) + .2, assembly2 + "-powers-tracks.png", 2, legend = ['Max', 'Mean'])
