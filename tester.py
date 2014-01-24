from openmoc import *
import openmoc.plotter as plotter
import openmoc.log as log
import openmoc.process as process
import subprocess
import tester_options
import h5py
import numpy

#Instantiates "options" object from "options" module and assigns it to options
options = tester_options.options()

#Gave the user multiple options to modify attributes for the simulation
options.parseArguments()

filename = options.filename
trackstest = options.trackstest
tracksvalues = options.tracksvalues
azimtest = options.azimtest
azimvalues = options.azimvalues
ringstest = options.ringstest
ringsvalues = options.ringsvalues
sectorstest = options.sectorstest
sectorsvalues = options.sectorsvalues
energygroups = options.energygroups

#turns strings that look like lists into actual lists
if tracksvalues != [0.1]:
    tracksvalues = [float(i) for i in tracksvalues.split(',')]
if azimvalues != [4]:
    azimvalues = [int(i) for i in azimvalues.split(',')]
if ringsvalues != [3]:
    ringsvalues = [int(i) for i in ringsvalues.split(',')]
if sectorsvalues != [16]:
    sectorsvalues = [int(i) for i in sectorsvalues.split(',')]

def tracks_tester(filename, tracksvalues, energygroups):
    print 'Varying Tracks...'
    for spacing in tracksvalues:
        f = open(filename, 'r+')
        for line in f:
            if 'numgroups = ' in line:
                print line
                old = str(line)
                line = line.replace(old, 'numgroups = %d' % (energygroups))
                print line
        f.close()
        subprocess.call(['python' , filename, '-s', str(spacing)])
        f = open(filename, 'r+')
        for line in f:
            if 'numgroups = ' in line:
                print line
                new = str(line)
                line = line.replace(new, old)
                print line
        f.close()
        print 'hi'



                     #### convergence test functions ####
def createCells(rings, sectors, dummy_id, circles, planes):

    #creates cells corresponding to the fuel pin
    cells = []
    #corresponds to fuel
    cells.append(CellBasic(universe=1, material=dummy_id, rings = rings, sectors = sectors))
    #corresponds to Helium
    cells.append(CellBasic(universe=1, material=dummy_id, sectors = sectors))
    #corresponds to cladding
    cells.append(CellBasic(universe=1, material=dummy_id, sectors = sectors))
    #corresponds to water
    cells.append(CellBasic(universe=1, material=dummy_id, sectors = sectors))

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
    cells.append(CellBasic(universe=2, material=dummy_id, rings = rings, sectors = sectors))
    #region with cladding
    cells.append(CellBasic(universe=2, material=dummy_id, sectors = sectors))
    #outside region with water
    cells.append(CellBasic(universe=2, material=dummy_id, sectors = sectors))

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

    return cells


def createLattice(geoDirectory, assembly):
    log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')
    lattice = Lattice(id=100, width_x=0.62992*2, width_y=0.62992*2)

    f = h5py.File(geoDirectory + assembly + '-minmax.hdf5', "r")
    cellData = f['cell_types']
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

    f.close()

    return pinCellArray, lattice

def createGeometry(geoDirectory, assembly, dummy, materials, cells, pinCellArray, lattice):

    log.py_printf('NORMAL', 'Creating geometry...')
    geometry = Geometry() 
    geometry.addMaterial(dummy)

    for material in materials.values(): geometry.addMaterial(material)
    for cell in cells: geometry.addCell(cell)
    
    #extracts microregion ranges
    f = h5py.File(geoDirectory + assembly + '-minmax.hdf5', "r")
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
            num_cells = cloned_universe.getNumCells()
            current_cell_ids = current_universe.getCellIds(num_cells)
            cell_ids = cloned_universe.getCellIds(num_cells)
            current_material_ids = []
            for k in range(len(current_min_max)):
                if 'microregion-%d' % (current_min_max[k]) in materials.keys():
                    current_material_ids.append(materials['microregion-%d' % (current_min_max[k])].getId())
            for k, cell_id in enumerate(cell_ids):
                cloned_cell = cloned_universe.getCellBasic(int(cell_id))
                cloned_cell.setMaterial(current_material_ids[k])
                geometry.addCell(cloned_cell)

    #lattice.printString()
    print pinCellArray
    lattice.setLatticeCells(pinCellArray)
    geometry.addLattice(lattice)

    geometry.initializeFlatSourceRegions()

    #plotter.plotCells(geometry, gridsize = 200 )
    #plotter.plotMaterials(geometry, gridsize = 200)

    return geometry


def createTrackGen(num_azim, geometry, track_spacing):

    log.py_printf('NORMAL', 'Initializing the track generator...')
    track_generator = TrackGenerator(geometry, num_azim, track_spacing)
    track_generator.generateTracks()
    return track_generator

def createSolver(geometry, track_generator, num_threads, tolerance, max_iters):   

    solver = ThreadPrivateSolver(geometry, track_generator)
    solver.setNumThreads(num_threads)
    solver.setSourceConvergenceThreshold(tolerance)
    solver.convergeSource(max_iters)
    solver.printTimerReport()

    process.storeSimulationState(solver, use_hdf5 = True)

def plot_things(geometry, solver, egs, gs):
    
    plotter.plotCells(geometry, gridsize = gs ) #gs --> gridsize
    plotter.plotMaterials(geometry, gridsize = gs)
    plotter.plotFluxes(geometry, solver, energy_groups=egs) #egs --> energy_groups
