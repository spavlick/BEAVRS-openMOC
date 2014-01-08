"""Imports all modules from OpenMOC, as well as the individual functions log,
plotter, and materialize, all of which are part of submodules within OpenMoc"""

from openmoc import *
import openmoc.log as log # this module stores data printed during simulation
import openmoc.plotter as plotter
import openmoc.materialize as materialize

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups? '))

#sets geometry variable to the file name used
geometry = pwru240c00 # raw_input('What is/are the file names? (Enter each one separated by a space without \'c4.\' or the file extension.) ')

directory = "materials/%s-group/" % (numgroups)

###############################################################################
####################### Main Simulation Parameters ########################
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
########################### Creating Materials ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

#The following assigns the dictionary returned by the materialize function in
#the materialize python file to the variable materials
materials = materialize.materialize(directory + geometry + '-materials.hdf5')

material_ids = []

#jasmeet rox
for material in materials:
    material_ids.append(materials[str(material)].getId())


###############################################################################
########################### Creating Surfaces #############################
###############################################################################

log.py_printf('NORMAL', 'Creating Surfaces...')

#creates list of circle and plane surfaces
circles = []
planes = []

#creates empty Material object as a dummy to fill the fuel cells
dummy_id = material_id()
dummy = Material(dummy_id)

#appends surfaces to listsg
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
############################# Creating Cells ##############################
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
