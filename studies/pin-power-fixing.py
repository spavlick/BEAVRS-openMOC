from openmoc import *
import openmoc.log as log # this module stores data printed during simulation
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import numpy
import h5py
from openmoc.options import Options
import openmoc.plotter as plotter
from tester import *

options = Options()

#sets the number of energy groups
numgroups = 2

#sets geometry variable to the file name used
assembly = 'pwru240w12'

directory = "../materials/%s-group/" % (numgroups)
geoDirectory = "../geo-data/%s-group/" % (numgroups)
pin_directory = 'casmo-reference/%s-group/' % (numgroups)

rings = 3
sectors = 8


num_threads, track_spacing, num_azim, tolerance, max_iters = defineParameters()
materials = createMaterials(directory, assembly)
dummy, dummy_id, circles, planes = createSurfaces(numgroups, bp=True)
cells = createCells(rings, sectors, dummy_id, circles, planes, bp=True)
pinCellArray, lattice = createLattice(geoDirectory, assembly)
geometry = createGeometry(geoDirectory, assembly, dummy, materials, cells, pinCellArray, lattice)

#num_azim test values
num_azim = 52

track_generator = createTrackGen(num_azim, geometry, track_spacing)
solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters, data = True)
max_error, mean_error = computePinPowerError(solver, pin_directory, assembly)
kinf_error = computeKinfError(solver, pin_directory, assembly)
print max_error, mean_error, kinf_error

#reset
num_azim = 32

#track_spacing test values
track_spacing = 0.05
   
track_generator = createTrackGen(num_azim, geometry, track_spacing)
solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters, data = True)
max_error, mean_error = computePinPowerError(solver, pin_directory, assembly)
kinf_error = computeKinfError(solver, pin_directory, assembly)
print max_error,mean_error,kinf_error
