import matplotlib.pyplot as plt
import h5py
import numpy

f = h5py.File('results/pwru310w12-fission-rates.h5', 'r')
calculatedPinPowers = f['universe0']['fission-rates'][...]
normalizedPinPowers = calculatedPinPowers/numpy.sum(calculatedPinPowers)
f.close()

fig = plt.figure()
plt.figure()
plt.pcolor(numpy.linspace(0, 17, 17), numpy.linspace(0, 17, 17), normalizedPinPowers, edgecolors = 'k', linewidths = 1, vmin = normalizedPinPowers[:,:].min(), vmax = normalizedPinPowers[:,:].max())
plt.colorbar()
plt.axis([0,17,0,17])
plt.title('Normalized Pin Powers')
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_yaxis().set_ticks([])
plt.show()
fig.savefig('Pin Powers pwru310w12.png')
