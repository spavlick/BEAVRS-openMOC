from openmoc import * 
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import numpy
import h5py
import copy
from openmoc.options import Options
import openmoc.plotter as plotter
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

#num_azim test values
num_azims = [i for i in range(4, 128, 4)]


#dictionaries that will contain pin errors and k-inf errors
az_pinmax = {}
az_pinmean = {}
az_kinf = {}

#simulation
for num_azim in num_azims:

    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters, note, data = True)
    max_error, mean_error = computePinPowerError(solver, pin_directory, assembly)
    kinf_error = computeKinfError(solver, pin_directory, assembly)
    az_pinmax['num_azim = %d' % (num_azim)] = max_error
    az_pinmean['num_azim = %d' % (num_azim)] = mean_error
    az_kinf['num_azim = %d' % (num_azim)] = kinf_error

#plotting
#plotter(num_azims, az_kinf, "Effect of Angle Variation on K-effective", "Azimuthal angles", "pwru160c00-angles.png")
    

#reset
num_azim = 32

#track_spacing test values
track_spacings = [0.5, 0.25, 0.1, 0.05, 0.01, 0.005]

#dictionaries that will contain pin errors and k-inf errors
ts_pinmax = {}
ts_pinmean = {}
ts_kinf = {}

#simulation
for track_spacing in track_spacings:
    
    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    createSolver(geometry, track_generator, num_threads, tolerance, max_iters, note, data = True)
    max_error, mean_error = computePinPowerError(solver, pin_directory, assembly)
    kinf_error = computeKinfError(solver, pin_directory, assembly)
    ts_pinmax['track_spacing = %f' % (track_spacing)] = max_error
    ts_pinmean['track_spacing = %f' % (track_spacing)] = mean_error
    ts_kinf['track_spacing = %f' % (track_spacing)] = kinf_error

#plotter(track_spacings, ts_kinf, "Effect of Track Spacing Variation on K-effective", "Track spacing", "pwru160c00-tracks.png")

#reset
track_spacing = 0.1

#rings and sectors test values
rings_list = [1]#[1,2,3,4]
sectors_list = [4,8]#[4, 8, 12, 16]

#dictionaries that will contain pin errors and k-inf errors
fsr_pinmax = {}
fsr_pinmean = {}
fsr_kinf = {}

storeError(assembly, 'az', az_pinmax, az_pinmean, az_kinf)
storeError(assembly, 'ts', ts_pinmax, ts_pinmean, ts_kinf)

'''
#simulation
for rings in rings_list:
    for sectors in sectors_list:
        note = 'rings = %d, sectors= %d' % (rings, sectors)
        cells = createCells(rings, sectors, dummy_id, circles, planes)
        pinCellArray, lattice = createLattice(geoDirectory, assembly)
        geometry = createGeometry(geoDirectory, assembly, dummy, materials, cells, pinCellArray, lattice)
        track_generator = createTrackGen(num_azim, geometry, track_spacing)
        createSolver(geometry, track_generator, num_threads, tolerance, max_iters, note, data = True)
        max_error, mean_error = computePinPowerError(solver, pin_directory, assembly)
        kinf_error = computeKinfError(solver, pin_directory, assembly)
        fsr_pinmax['rings = %d, sectors = %d' % (rings, sectors)] = max_error
        fsr_pinmean['rings = %d, sectors = %d' % (rings, sectors)] = mean_error
        fsr_kinf['rings = %d, sectors = %d' % (rings, sectors)] = kinf_error
'''
