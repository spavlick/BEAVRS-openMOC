import matplotlib.pyplot as plt
import numpy
import h5py

f = h5py.File('pin-powers/fission-rates.h5', 'r')
calculatedPinPowers = f['universe0']['fission-rates'][...]
normalizedPinPowers = calculatedPinPowers/numpy.sum(calculatedPinPowers)
f.close()

plt.figure()
plt.pcolor(numpy.linspace(0, 17, 17), numpy.linspace(0, 17, 17), normalizedPinPowers, edgecolors = 'k', linewidths = 1, vmin = normalizedPinPowers[:,:].min(), vmax = normalizedPinPowers[:,:].max())
plt.colorbar()
plt.axis([0,17,0,17])
plt.title('Normalized Pin Powers')
plt.show()