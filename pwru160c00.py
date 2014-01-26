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
assembly = "pwru160c00"
directory = "materials/%s-group/" % (numgroups)
geoDirectory = "geo-data/%s-group/" % (numgroups)


rings = 3
sectors = 8


num_threads, track_spacing, num_azim, tolerance, max_iters = defineParameters()
materials = createMaterials(directory, assembly)
dummy, dummy_id, circles, planes = createSurfaces(numgroups, bp=False)
cells = createCells(rings, sectors, dummy_id, circles, planes)
pinCellArray, lattice = createLattice(geoDirectory, assembly)
geometry = createGeometry(geoDirectory, assembly, dummy, materials, cells, pinCellArray, lattice)
track_generator = createTrackGen(num_azim, geometry, track_spacing)
createSolver(geometry, track_generator, num_threads, tolerance, max_iters)


gs = 200
egs = [1,2]
#plot_things(geometry, solver, egs, gs)

###For Paper###

#plot with 3 rings, 8 sectors, and 32 angles

#storeSimulationState (SSS) parameter info:
    #instead of appending, we can make SSS override the data before each simulation by adding the argument:
        #append = False (default is True)
    #to add a note, argument is:
        #note = '(insert stuff here)'
            #useful for rings and sectors and whatever else we need for each run




