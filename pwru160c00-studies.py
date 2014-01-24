"""Imports all modules from OpenMOC, as well as the individual functions log, 
plotter, and materialize, all of which are part of submodules within OpenMoc"""

from openmoc import * 
import openmoc.log as log # this module stores data printed during simulation
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import numpy
import h5py
from openmoc.options import Options
import openmoc.plotter as plotter
import openmoc.process as process
from tester import *
import copy

options = Options()

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups?'))

#sets assembly variable to the file name used
assembly = "pwru160c00"

directory = "materials/%s-group/" % (numgroups)
geoDirectory = "geo-data/%s-group/" % (numgroups)

###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

"""This imports a variety of variables from the options file. This should be 
located within the OpenMOC folder.This could potentially also accept user input,
but there should also be a default value."""

num_threads = options.num_omp_threads
track_spacing = options.track_spacing
num_azim = options.num_azim
tolerance = options.tolerance
max_iters = options.max_iters

log.setLogLevel('NORMAL')

###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

#The following assigns the dictionary returned by the materialize function in 
#the materialize python file to the variable materials
materials = materialize.materialize(directory + assembly + '-materials.hdf5')

#empty list to insert all material ids
material_ids = []

#jasmeet rox
for material in materials:
    material_ids.append(materials[str(material)].getId())



###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating Surfaces...')

#creates list of circle and plane surfaces
circles = [] 
planes = []

#creates empty Material object as a dummy to fill the fuel cells
dummy_id = material_id()
dummy = Material(dummy_id)

#gives dummy material stupid cross sections
dummy.setNumEnergyGroups(int(numgroups))
dummyxs = numpy.zeros(int(numgroups))
dummyscatter = numpy.zeros((int(numgroups))**2)
dummy.setSigmaT(dummyxs)
dummy.setSigmaS(dummyscatter)
dummy.setSigmaF(dummyxs)
dummy.setSigmaA(dummyxs)
dummy.setNuSigmaF(dummyxs)
dummy.setChi(dummyxs)

#appends surfaces to lists
planes.append(XPlane(x=-0.62992*17))
planes.append(XPlane(x=0.62992*17))
planes.append(YPlane(y=-0.62992*17))
planes.append(YPlane(y=0.62992*17))
#Radii for fuel cells
circles.append(Circle(x=0.0, y=0.0, radius=0.39218))
circles.append(Circle(x=0.0, y=0.0, radius=0.40005))
circles.append(Circle(x=0.0, y=0.0, radius=0.45720))
#Radii for guide tubes (also use for instrument tube)
circles.append(Circle(x=0.0, y=0.0, radius=0.56134))
circles.append(Circle(x=0.0, y=0.0, radius=0.60198))

#sets the boundary type for the planes to be reflective (neutrons bounce back)
for plane in planes:plane.setBoundaryType(REFLECTIVE)


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

num_sectors = 8
num_rings = 3

#creates cells corresponding to the fuel pin
cells = []
#corresponds to fuel
cells.append(CellBasic(universe=1, material=dummy_id, rings = num_rings, sectors = num_sectors))
#corresponds to Helium
cells.append(CellBasic(universe=1, material=dummy_id, sectors = num_sectors))
#corresponds to cladding
cells.append(CellBasic(universe=1, material=dummy_id, sectors = num_sectors))
#corresponds to water
cells.append(CellBasic(universe=1, material=dummy_id, sectors = num_sectors))

#first cell, region with fuel
cells[0].addSurface(halfspace=-1, surface=circles[0])

#second cell, region with helium
cells[1].addSurface(halfspace=-1, surface=circles[1])
cells[1].addSurface(halfspace=+1, surface=circles[0])

#third cell, region with cladding
cells[2].addSurface(halfspace=-1, surface=circles[2])
cells[2].addSurface(halfspace=+1, surface=circles[1])

#region with water
cells[3].addSurface(halfspace=+1, surface=circles[2])

#creates cells corresponding to the guide tube
#inner region with water
cells.append(CellBasic(universe=2, material=dummy_id, sectors = num_sectors, rings = num_rings))
#region with cladding
cells.append(CellBasic(universe=2, material=dummy_id, sectors = num_sectors))
#outside region with water
cells.append(CellBasic(universe=2, material=dummy_id, sectors = num_sectors))

#first cell, inner water region
cells[4].addSurface(halfspace=-1, surface=circles[3])

#next cell with cladding
cells[5].addSurface(halfspace=-1, surface=circles[4])
cells[5].addSurface(halfspace=+1, surface=circles[3])

#outer cell with water
cells[6].addSurface(halfspace=+1, surface=circles[4])

#creates cells that are filled by the lattice universe
cells.append(CellFill(universe=0, universe_fill=100))

#giant cell
cells[7].addSurface(halfspace=+1, surface=planes[0])
cells[7].addSurface(halfspace=-1, surface=planes[1])
cells[7].addSurface(halfspace=+1, surface=planes[2])
cells[7].addSurface(halfspace=-1, surface=planes[3])



###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')

"""A universe is a space containing a fuel pin within our 4x4 lattice. Further 
comments below on how the lattice was created."""

#reads data from hdf5 file
f = h5py.File(geoDirectory + assembly + '-minmax.hdf5', "r")

#extracts cell_types data set from file and assigns it to cellData
cellData = f['cell_types']

#creates an array of zeros in the same shape as cellData
pinCellArray = numpy.zeros(cellData.shape, dtype=numpy.int32)

burnablePoisons = False

#checks to see if there are burnable poisons in cellData
if 4 in cellData[:,:]:
    burnablePoisons = True

#changes values in pinCellArray to be consistent in this code
for i, row in enumerate(cellData):
    for j, col in enumerate(row):
        if cellData[i,j] == 1:
            pinCellArray[i,j] = 1
        elif cellData[i,j] == 2:
            pinCellArray[i,j] = 2
        elif burnablePoisons == False and cellData[i,j] == 3:
            pinCellArray[i,j] = 2
        elif burnablePoisons == True and cellData[i,j] == 3:
            pinCellArray[i,j] = 3
        else:
            pinCellArray[i,j] = 2


############################################################################
##########################   Creating the Geometry   #######################
############################################################################
lattice = Lattice(id=100, width_x=0.62992*2, width_y=0.62992*2)
#lattice.printString()
f = h5py.File(geoDirectory + assembly + '-minmax.hdf5', "r")
log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry() 
num_sector = 8

#adds dummy material to geometry
geometry.addMaterial(dummy)

for material in materials.values(): geometry.addMaterial(material)

for cell in cells: geometry.addCell(cell)

#extracts the range of microregions for each unit in the array
min_values = f['minregions'][...]
max_values = f['maxregions'][...]
f.close()

#finds microregions, clones universe, adds materials to cells in universes
for i, row in enumerate(pinCellArray):
    for j, col in enumerate(row):
        current_UID = pinCellArray[i,j]
        current_min_max = [y for y in range(min_values[i,j], max_values[i,j]+1)]
        current_universe = geometry.getUniverse(int(current_UID))
        cloned_universe = current_universe.clone()
        pinCellArray [i,j] = cloned_universe.getId()
        print pinCellArray[i,j]
        num_cells = cloned_universe.getNumCells()
        current_cell_ids = current_universe.getCellIds(num_cells)
        cell_ids = cloned_universe.getCellIds(num_cells)
        current_material_ids = []
        for k in range(len(current_min_max)):
            if 'microregion-%d' % (current_min_max[k]) in materials.keys():
                current_material_ids.append(materials['microregion-%d' % (current_min_max[k])].getId())
        
        for k, cell_id in enumerate(cell_ids):
            cloned_cell = cloned_universe.getCellBasic(int(cell_id))
            #print cloned_cell
            cloned_cell.setMaterial(current_material_ids[k])
            geometry.addCell(cloned_cell)
            #cloned_cell.setNumSectors(num_sector)
            #if k == 0:
                #cloned_cell.setNumRings(num_rings)        
            
lattice.setLatticeCells(pinCellArray)
#lattice.printString()
geometry.addLattice(lattice)

geometry.initializeFlatSourceRegions()


#num_rings = 3
angle = 4
track_spacing = 0.1

'''for num_sector in num_sectors:
    new_pinCellArray = copy.deepcopy(pinCellArray)
    geometry, lattice = createGeometry(num_rings, num_sector, geoDirectory, assembly, dummy, materials, cells, new_pinCellArray)
    track_generator = createTrackGen(angle, geometry, track_spacing)
    solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
    del geometry'''


angles = numpy.arange(4, 260, 4, dtype = numpy.int32)



for angle in angles:
    ###########################################################################
    #######################   Creating the TrackGenerator   ###################
    ###########################################################################

    #The following runs the simulation for changes in FSR

    log.py_printf('NORMAL', 'Initializing the track generator...')

    #Creates an instance of the TrackGenerator class, takes three parameters
    track_generator = TrackGenerator(geometry, int(angle), track_spacing)
    #Runs the generateTracks() method of the TrackGenerator class
    track_generator.generateTracks()
    ############################################################################
    #########################   Running a Simulation ###########################
    ############################################################################

    #Creates an instance of the ThreadPrivateSolver class with two parameters
    solver = ThreadPrivateSolver(geometry, track_generator)
    #Sets the number of threads with the number imported from options
    solver.setNumThreads(num_threads)
    #sets the convergence threshold with tolerance imported from options
    solver.setSourceConvergenceThreshold(tolerance)
    #This is where the simulation is actually run. max_iters here is the 
    #number of iterations for the simulation.
    solver.convergeSource(max_iters)
    #Prints a report with time elapsed 
    solver.printTimerReport()
    process.storeSimulationState(solver, use_hdf5 = True, filename = "angles")


#num_rings = 3
angle = 4
track_spacing = 0.1

'''for num_sector in num_sectors:
    new_pinCellArray = copy.deepcopy(pinCellArray)
    geometry, lattice = createGeometry(num_rings, num_sector, geoDirectory, assembly, dummy, materials, cells, new_pinCellArray)
    track_generator = createTrackGen(angle, geometry, track_spacing)
    solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
    del geometry'''


tracks = [.1, .05, .01, .005, .001, .0005]


for track in tracks:
    ###########################################################################
    #######################   Creating the TrackGenerator   ###################
    ###########################################################################

    #The following runs the simulation for changes in FSR

    log.py_printf('NORMAL', 'Initializing the track generator...')

    #Creates an instance of the TrackGenerator class, takes three parameters
    track_generator = TrackGenerator(geometry, int(angle), track)
    #Runs the generateTracks() method of the TrackGenerator class
    track_generator.generateTracks()
    ############################################################################
    #########################   Running a Simulation ###########################
    ############################################################################

    #Creates an instance of the ThreadPrivateSolver class with two parameters
    solver = ThreadPrivateSolver(geometry, track_generator)
    #Sets the number of threads with the number imported from options
    solver.setNumThreads(num_threads)
    #sets the convergence threshold with tolerance imported from options
    solver.setSourceConvergenceThreshold(tolerance)
    #This is where the simulation is actually run. max_iters here is the 
    #number of iterations for the simulation.
    solver.convergeSource(max_iters)
    #Prints a report with time elapsed 
    solver.printTimerReport()
    process.storeSimulationState(solver, use_hdf5 = True, filename = "trackspacing")

