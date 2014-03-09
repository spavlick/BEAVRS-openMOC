from openmoc import * 
import openmoc.log as log
import openmoc.plotter as plot
import openmoc.materialize as materialize
import numpy
import h5py
import copy
from openmoc.options import Options
from tester import *
import matplotlib

options = Options()

#sets the number of energy groups
numgroups = 2

#sets assembly variable to the file name used
assembly = "pwru160c00"
directory = "../materials/%s-group/" % (numgroups)
geoDirectory = "../geo-data/%s-group/" % (numgroups)
pin_directory = 'casmo-reference/%s-group/' % (numgroups)

rings = 3
sectors = 8
note = 'rings = %d, sectors= %d' % (rings, sectors)

num_threads, track_spacing, num_azim, tolerance, max_iters = defineParameters()
materials = createMaterials(directory, assembly)
dummy, dummy_id, circles, planes = createSurfaces(numgroups, bp=False)
cells = createCells(rings, sectors, dummy_id, circles, planes)
pinCellArray, lattice = createLattice(geoDirectory, assembly)
geometry = createGeometry(geoDirectory, assembly, dummy, materials, cells, pinCellArray, lattice)

#plot.plot_flat_source_regions(geometry, gridsize = 250)
#plot.plot_fluxes(geometry, solver, energy_groups=[2], gridsize=250)
#num_azim test values
num_azims = [i for i in range(4, 128, 4)]

f = h5py.File('results/' + assembly + '-errors.h5')
f.attrs['Energy Groups'] = 2
current_test = f.create_group('Azimuthal Angles Tests')


#simulation
for num_azim in num_azims:

    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
    max_error, mean_error, calculatedPinPowers = computePinPowerError(solver, pin_directory, assembly)
    kinf_error = computeKinfError(solver, pin_directory, assembly)
    azim_test = current_test.create_group('Num Azim = %d' % (num_azim))
    azim_test.create_dataset('Pin Powers', data = calculatedPinPowers)
    azim_test.create_dataset('Max Error', data = max_error)
    azim_test.create_dataset('Min Error', data = mean_error)
    azim_test.create_dataset('Kinf_Error', data = kinf_error)


#reset
num_azim = 32

#track_spacing test values
track_spacings = [0.5, 0.25, 0.1, 0.05, 0.01, 0.005]

current_test = f.create_group('Track Spacing Tests')

#simulation
for track_spacing in track_spacings:
    
    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
    max_error, mean_error, calculatedPinPowers= computePinPowerError(solver, pin_directory, assembly)
    kinf_error = computeKinfError(solver, pin_directory, assembly)
    track_test = current_test.create_group('Track Spacing = %d' % (track_spacing))
    track_test.create_dataset('Pin Powers', data = calculatedPinPowers)
    track_test.create_dataset('Max Error', data = max_error)
    track_test.create_dataset('Min Error', data = mean_error)
    track_test.create_dataset('Kinf_Error', data = kinf_error)

#reset
track_spacing = 0.1

#rings and sectors test values
rings_list = [1,2,3,4]
sectors_list = [4, 8, 12, 16]


#simulation
for rings in rings_list:
    for sectors in sectors_list:
        cells = createCells(rings, sectors, dummy_id, circles, planes)
        pinCellArray, lattice = createLattice(geoDirectory, assembly)
        geometry = createGeometry(geoDirectory, assembly, dummy, materials, cells, pinCellArray, lattice)
        track_generator = createTrackGen(num_azim, geometry, track_spacing)
        createSolver(geometry, track_generator, num_threads, tolerance, max_iters, note = ('rings = %d, sectors = %d' % (rings, sectors)), data = True)


f.close()