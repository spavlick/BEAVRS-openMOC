import h5py
import numpy
import matplotlib as plt
from tester import *
import os.path

test = 'Track Spacing Tests'
strip = 'Track Spacing = '

x_axis = []

assembly_list = ['pwru160c00','pwru240c00','pwru240w12','pwru310c00','pwru310w12']

f = h5py.File('results/' + assembly_list[4] + '-trackspacing-errors.h5', 'r')
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

legend = ['1.6% w/o BP','2.4% w/o BP', '2.4% w/ BP', '3.1% w/o BP', '3.1% w/ BP']
fig = plt.figure()
colors = ['b', 'g', 'r', 'k', 'm']
for i, assembly in enumerate(assembly_list):
    kinf_list = []
    filename = assembly + '-trackspacing-errors.h5'
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for j, x in enumerate(x_axis):
        value_keys = f[test][sorted_keys[j]].keys()
        for key in value_keys:
            if 'Kinf_Error' in key:
                kinf_list.append(f[test][sorted_keys[j]][key][...]*10**5)
    plt.plot(x_axis,kinf_list, colors[i] + 'o-', ms = 10, lw = 2)
    f.close()

plt.axis([max(x_axis), 0, 0, 400])
plt.title('Error in K-Infinity')
plt.xlabel('Track Spacing [cm]')
plt.ylabel('K-Infinity Error [pcm]')
plt.grid()
plt.legend(legend)
plt.show()
fig.savefig('K-Infinity-Error-TS.png')

fig = plt.figure()
for i, assembly in enumerate(assembly_list):
    mean_list = []
    filename = assembly + '-trackspacing-errors.h5'
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for j, x in enumerate(x_axis):
        value_keys = f[test][sorted_keys[j]].keys()
        for key in value_keys:
            if 'Min' in key:
                mean_list.append(f[test][sorted_keys[j]][key][...]*10**2)
    plt.plot(x_axis,mean_list, colors[i] + 'o-', ms = 10, lw = 2)
    f.close()

plt.axis([max(x_axis), 0, 0, .4])
plt.title('Mean Pin Power Error')
plt.xlabel('Track Spacing [cm]')
plt.ylabel('Relative Percent Mean Pin Power Error')
plt.grid()
plt.legend(legend)
plt.show()
fig.savefig('Mean-Error-TS.png')

fig = plt.figure()
for i, assembly in enumerate(assembly_list):
    max_list = []
    filename = assembly + '-trackspacing-errors.h5'
    if os.path.isfile('results/' + filename):
        f = h5py.File('results/' + filename, 'r')
    else:
        f = h5py.File('results/' + assembly + '-errors.h5', 'r')
    for j, x in enumerate(x_axis):
        value_keys = f[test][sorted_keys[j]].keys()
        for key in value_keys:
            if 'Max' in key:
                max_list.append(f[test][sorted_keys[j]][key][...]*10**2)
    plt.plot(x_axis,max_list, colors[i] + 'o-', ms = 10, lw = 2)
    f.close()

plt.axis([max(x_axis), 0, 0, 4])
plt.title('Max Pin Power Error')
plt.xlabel('Track Spacing [cm]')
plt.ylabel('Relative Percent Max Pin Power Error')
plt.grid()
plt.legend(legend)
plt.show()
fig.savefig('Max-Error-TS.png')
