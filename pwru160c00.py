"""Imports all modules from OpenMOC, as well as the individual functions log, 
plotter, and materialize, all of which are part of submodules within OpenMoc"""

from openmoc import * 
import openmoc.log as log # this module stores data printed during simulation
import openmoc.plotter as plotter
import openmoc.materialize as materialize
import numpy
import h5py

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups? '))

#sets geometry variable to the file name used
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

#creates cells corresponding to the fuel pin
cells = []
#corresponds to fuel
cells.append(CellBasic(universe=1, material=dummy_id, rings=3, sectors=8))
#corresponds to Helium
cells.append(CellBasic(universe=1, material=dummy_id, sectors=8))
#corresponds to cladding
cells.append(CellBasic(universe=1, material=dummy_id, sectors=8))
#corresponds to water
cells.append(CellBasic(universe=1, material=dummy_id,sectors=8))

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
cells.append(CellBasic(universe=2, material=dummy_id, rings=3, sectors=8))
#region with cladding
cells.append(CellBasic(universe=2, material=dummy_id, sectors=8))
#outside region with water
cells.append(CellBasic(universe=2, material=dummy_id, sectors=8))

#first cell, inner water region
cells[4].addSurface(halfspace=-1, surface=circles[3])

#next cell with cladding
cells[5].addSurface(halfspace=-1, surface=circles[4])
cells[5].addSurface(halfspace=+1, surface=circles[3])

#outer cell with water
cells[6].addSurface(halfspace=+1, surface=circles[4])


#creates cells that are filled by the lattice universe
cells.append(CellFill(universe=0, universe_fill=3))

###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')

"""A universe is a space containing a fuel pin within our 4x4 lattice. Further 
comments below on how the lattice was created."""

lattice = Lattice(id=3, width_x=0.62992*2, width_y=0.62992*2)

#reads data from hdf5 file
f = h5py.File(geoDirectory + assembly + '-minmax.hdf5', "r")
cellData = f['cell_types']
pinCellArray = numpy.zeros(cellData.shape, dtype=numpy.int32)

burnablePoisons = False

if 4 in cellData[:,:]:
    burnablePoisons = True

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

lattice.setLatticeCells(pinCellArray)

###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry() 
"""Creates an instance of the Geometry class. This is a 
class in the openmoc file."""

geometry.addMaterial(dummy)

min_values = f['minregions']
max_values = f['maxregions']

f.close()

for i, row in enumerate(pinCellArray):
    for j, col in enumerate(row):
        current_UID = pinCellArray[i,j]
        current_universe = geometry.getUniverse(current_UID)
        cloned_universe = current_universe.clone()
        cell_ids = current_universe.cellIds()
        for region in range(min_values[i,j],max_values[i,j]+1):
            #for cell_id in cell_ids:
                #cell = cloned_universe.getCell(cell_id)
                #figure out what micro region to use
                #cell.setmaterial(our specific material)
                

for material in materials.values(): geometry.addMaterial(material)


for cell in cells: geometry.addCell(cell)


geometry.addLattice(lattice)

geometry.initializeFlatSourceRegions()



###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

#The following runs the simulation for changes in FSR

log.py_printf('NORMAL', 'Initializing the track generator...')

#Creates an instance of the TrackGenerator class, takes three parameters
track_generator = TrackGenerator(geometry, num_azim, track_spacing)
#Runs the generateTracks() method of the TrackGenerator class
track_generator.generateTracks()

###############################################################################
#########################   Running a Simulation ##############################
###############################################################################

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
