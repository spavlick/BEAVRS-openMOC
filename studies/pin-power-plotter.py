import matplotlib.pyplot as plt
import h5py
import numpy


assembly_list = ['pwru160c00','pwru240c00','pwru240w12','pwru310c00','pwru310w12']

for assembly in assembly_list:

    f = h5py.File('pin-powers/'+ assembly +'-fission-rates.h5', 'r')
    calculatedPinPowers = f['universe0']['fission-rates'][...]
    normalizedPinPowers = calculatedPinPowers/numpy.sum(calculatedPinPowers)
    f.close()

    fig = plt.figure()
    plt.figure()
    plt.pcolor(numpy.linspace(0, 18, 18), numpy.linspace(0, 18, 18), normalizedPinPowers, edgecolors = 'k', linewidths = 1, vmin = normalizedPinPowers[:,:].min(), vmax = normalizedPinPowers[:,:].max())
    plt.colorbar()
    plt.axis([0,18,0,18])
    plt.title('Normalized Pin Powers')
    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.show()
    fig.savefig('Pin_Powers_' + assembly + '.png')
