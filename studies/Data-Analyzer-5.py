import h5py
import numpy
import matplotlib as plt
from tester import *
import os.path

test = 'Flat Source Region Tests'
strip1 = 'Rings = '
strip2 = 'Sectors = '

assembly_list = ['pwru160c00','pwru240c00','pwru240w12','pwru310c00','pwru310w12']

f = h5py.File('results/' + assembly_list[4] + '-ringssectors-errors.h5', 'r')

keys = f[test].keys()
rings = []
sectors = []
for key in keys:
    current_value = float(key.strip(strip1))
    rings.append(current_value)
rings.sort()

sorted_rings_keys = [None]*len(rings)
for key in keys:
    for i, x in enumerate(rings):
        if x == float(key.strip(strip1)):
            sorted_rings_keys[i] = key


keys = f[test][sorted_rings_keys[0]].keys()
for key in keys:
    current_value = float(key.strip(strip2))
    sectors.append(current_value)
f.close()
sectors.sort()

sorted_sectors_keys = [None]*len(sectors)
for key in keys:
    for i, x in enumerate(sectors):
        if x == float(key.strip(strip2)):
            sorted_sectors_keys[i] = key

fsr_kinf_error = []
for assembly in assembly_list:
    filename = assembly + '-ringssectors-errors.h5'
    kinf_array = []
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for ring_key in sorted_rings_keys:
        kinf_row = []
        for sector_key in sorted_sectors_keys:
            value_keys = f[test][ring_key][sector_key].keys()
            for key in value_keys:
                if 'Kinf' in key:
                    kinf_row.append(f[test][ring_key][sector_key][key][...]*10**5)
        kinf_array.append(kinf_row)
    fsr_kinf_error.append(kinf_array)
    f.close()

fsr_mean_error = []
for assembly in assembly_list:
    filename = assembly + '-ringssectors-errors.h5'
    mean_array = []
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for ring_key in sorted_rings_keys:
        mean_row = []
        for sector_key in sorted_sectors_keys:
            value_keys = f[test][ring_key][sector_key].keys()
            for key in value_keys:
                if 'Min' in key:
                    mean_row.append(f[test][ring_key][sector_key][key][...]*10**2)
        mean_array.append(mean_row)
    fsr_mean_error.append(mean_array)
    f.close()

fsr_max_error = []
for assembly in assembly_list:
    filename = assembly + '-ringssectors-errors.h5'
    max_array = []
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for ring_key in sorted_rings_keys:
        max_row = []
        for sector_key in sorted_sectors_keys:
            value_keys = f[test][ring_key][sector_key].keys()
            for key in value_keys:
                if 'Max' in key:
                    max_row.append(f[test][ring_key][sector_key][key][...]*10**2)
        max_array.append(max_row)
    fsr_max_error.append(max_array)
    f.close()

for array in fsr_kinf_error:
    nparray = numpy.array(array)
    fig = plt.figure()
    plt.pcolor(numpy.linspace(0,5,5),numpy.linspace(0,5,5), nparray, edgecolors = 'k', linewidths = 1, vmin = nparray[:,:].min(), vmax = nparray[:,:].max())
    plt.colorbar()
    plt.axis([0,4,0,4])
    plt.title('FSR K-infinity')
    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.show()
    fig.savefig('fsr.jpeg')
