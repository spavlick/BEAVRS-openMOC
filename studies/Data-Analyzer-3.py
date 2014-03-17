import h5py
import numpy
import matplotlib as plt
from tester import *
import os.path

test = 'Azimuthal Angles Tests'
strip = 'Num Azim = '

assembly_list = ['pwru160c00','pwru240c00','pwru240w12','pwru310c00','pwru310w12']

x_axis = []

f = h5py.File('results/' + assembly_list[0] + 'num-azim-errors.h5', 'r')
keys = f[test].keys()
for key in keys:
    current_value = float(key.strip(strip))
    x_axis.append(current_value)
f.close()
x_axis.sort()

sorted_keys = [None]*len(x_axis)
for key in keys:
    for i, x in enumerate(x_axis):
        if x == float(key.strip(strip)):
            sorted_keys[i] = key

legend = ['1.6% w/ BP','2.4% w/o BP', '2.4% w/ BP', '3.1% w/o BP', '3.1% w/ BP']
fig = plt.figure()
colors = ['b', 'g', 'r', 'k', 'm']
for i, assembly in enumerate(assembly_list):
    kinf_list = []
    filename = assembly + 'num-azim-errors.h5'
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for j, x in enumerate(x_values):
        value_keys = f[test][sorted_keys[j]].keys()
        for key in value_keys:
            if 'Kinf' in key:
                kinf_list.append(f[test][sorted_keys[j]][key][...])
    plt.plot(x_axis,kinf_list, colors[i] + 'o-', ms = 10, lw = 2)
    f.close()

plt.axis([0, x_scale, 0, y_scale])
plt.title('K-Infinity Error')
plt.xlabel(test)
plt.ylabel('K-Infinity Error [pcm]')
plt.grid()
plt.legend(legend)
plt.show()
fig.savefig('K-Infinity-Error.png')

fig = plt.figure()
colors = ['b', 'g', 'r', 'k', 'm']
for i, assembly in enumerate(assembly_list):
    mean_list = []
    f = h5py.File('results/' + assembly + testname, 'r')
    for j, x in enumerate(x_values):
        value_keys = f[test][sorted_keys[j]].keys()
        for key in value_keys:
            if 'Mean' in key:
                mean_list.append(f[test][sorted_keys[j]][key][...])
    plt.plot(x_axis,kinf_list, colors[i] + 'o-', ms = 10, lw = 2)
    f.close()

plt.axis([0, x_scale, 0, y_scale])
plt.title('Mean Pin Power Error')
plt.xlabel(test)
plt.ylabel('Mean Pin Power Error')
plt.grid()
plt.legend(legend)
plt.show()
fig.savefig('Mean-Error.png')

fig = plt.figure()
colors = ['b', 'g', 'r', 'k', 'm']
for i, assembly in enumerate(assembly_list):
    max_list = []
    f = h5py.File('results/' + assembly + testname, 'r')
    for j, x in enumerate(x_values):
        value_keys = f[test][sorted_keys[j]].keys()
        for key in value_keys:
            if 'Max' in key:
                max_list.append(f[test][sorted_keys[j]][key][...])
    plt.plot(x_axis,kinf_list, colors[i] + 'o-', ms = 10, lw = 2)
    f.close()

plt.axis([0, x_scale, 0, y_scale])
plt.title('Max Pin Power Error')
plt.xlabel(test)
plt.ylabel('Max Pin Power Error')
plt.grid()
plt.legend(legend)
plt.show()
fig.savefig('Max-Error.png')
