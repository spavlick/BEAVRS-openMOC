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

options = Options()

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups?'))

#sets assembly variable to the file name used
assembly = "pwru310c00"
directory = "../materials/%s-group/" % (numgroups)
geoDirectory = "../geo-data/%s-group/" % (numgroups)


rings = 3
sectors = 8


#num_azim test values
num_azims = [i for i in range(4, 260, 4)]
print num_azims

#simulation
for num_azim in num_azims:

    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    createSolver(geometry, track_generator, num_threads, tolerance, max_iters, data = True)

#reset
num_azim = 32

#track_spacing test values
track_spacings = [0.5, 0.25, 0.1, 0.05, 0.01, 0.005]

#simulation
for track_spacing in track_spacings:
    
    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    createSolver(geometry, track_generator, num_threads, tolerance, max_iters, data = True)

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
        createSolver(geometry, track_generator, num_threads, tolerance, max_iters, data = True)

