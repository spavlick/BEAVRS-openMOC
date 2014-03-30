import h5py
import numpy
import matplotlib.pyplot as plt
import casmo
import os

assembly_name = 'pwru310w12'
assembly = casmo.Casmo()

# create a directory for plots
directory = 'pin-error-gridplots/'
if not os.path.exists(directory):
  os.makedirs(directory)

# extract and normalize simulation pin powers
f = h5py.File('pin-powers/%s-fission-rates.h5' % (assembly_name), 'r')
powers = numpy.zeros((17,17))
powers[:] = f['universe0']['fission-rates'][...]
avg_power = numpy.average(powers[numpy.nonzero(powers)])
powers = powers/avg_power
f.close()

# extract and normalize reference pin powers
assembly._filename = ('c4.' + assembly_name + '.out')
assembly._directory = '../Cross-Section-Output/2-group/'
assembly.importWidth()
ref_powers = assembly.parsePinPowers()
ref_powers = ref_powers/(numpy.average(ref_powers[numpy.nonzero(ref_powers)]))

# Compute percent relative error w/ respect to reference c5g7 errors
rel_err = (powers-ref_powers)/ref_powers * 100 # in percentages 
rel_err[numpy.isinf(rel_err)] = 0.0
rel_err[numpy.isnan(rel_err)] = 0.0
rel_err = abs(rel_err)

# plot error
plt.figure()
plt.pcolor(numpy.linspace(0, 18,18), numpy.linspace(0,18,18), \
       numpy.flipud(rel_err[:,:]), edgecolors='k', linewidths=1, 
           vmin=rel_err[:,:].min(), vmax=rel_err[:,:].max())
plt.colorbar()
plt.title(assembly_name + ' Pin Power Percent Relative Error\n', fontsize=18)
plt.axis([0,18,0,18])
plt.gca().axes.get_xaxis().set_ticks([])
plt.gca().axes.get_yaxis().set_ticks([])
plt.savefig(directory+assembly_name+'-pin-errors.png')
