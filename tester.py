from openmoc import *
from openmoc import options
import openmoc.plotter as plotter
import openmoc.log as log
import openmoc.process as process
import subprocess
import h5py
import numpy

options = options.Options()


def defineParameters():

    num_threads = options.num_omp_threads
    track_spacing = options.track_spacing
    num_azim = options.num_azim
    tolerance = options.tolerance
    max_iters = options.max_iters

    log.setLogLevel('NORMAL')

    return num_threads, track_spacing, num_azim, tolerance, max_iters


def createMaterials(directory, assembly):

    log.py_printf('NORMAL', 'Importing materials data from HDF5...')

    materials = materialize.materialize(directory + assembly + '-materials.hdf5')
    
    return materials


def createSurfaces(numgroups, bp=False):
    
    if bp == False:
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

        for plane in planes:plane.setBoundaryType(REFLECTIVE)

        return dummy, dummy_id, circles, planes
    
    elif bp == True:

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
        #Radii for burnable poisons
        circles.append(Circle(x=0.0, y=0.0, radius=0.21400))
        circles.append(Circle(x=0.0, y=0.0, radius=0.23051))
        circles.append(Circle(x=0.0, y=0.0, radius=0.24130))
        circles.append(Circle(x=0.0, y=0.0, radius=0.42672))
        circles.append(Circle(x=0.0, y=0.0, radius=0.43688))
        circles.append(Circle(x=0.0, y=0.0, radius=0.48387))
        circles.append(Circle(x=0.0, y=0.0, radius=0.56134))
        circles.append(Circle(x=0.0, y=0.0, radius=0.60198))

        for plane in planes:plane.setBoundaryType(REFLECTIVE)

        return dummy, dummy_id, circles, planes


def createCells(rings, sectors, dummy_id, circles, planes, bp=False):

    if bp == False:

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

    elif bp == True:

        cells = []
        #corresponds to fuel
        cells.append(CellBasic(universe=1, material=dummy_id))
        #corresponds to Helium
        cells.append(CellBasic(universe=1, material=dummy_id))
        #corresponds to cladding
        cells.append(CellBasic(universe=1, material=dummy_id))
        #corresponds to water
        cells.append(CellBasic(universe=1, material=dummy_id))

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
        cells.append(CellBasic(universe=2, material=dummy_id))
        #region with cladding
        cells.append(CellBasic(universe=2, material=dummy_id))
        #outside region with water
        cells.append(CellBasic(universe=2, material=dummy_id))

        #first cell, inner water region
        cells[4].addSurface(halfspace=-1, surface=circles[3])

        #next cell with cladding
        cells[5].addSurface(halfspace=-1, surface=circles[4])
        cells[5].addSurface(halfspace=+1, surface=circles[3])

        #outer cell with water
        cells[6].addSurface(halfspace=+1, surface=circles[4])


        #creates cells corresponding to the burnable poison

        #inner region with air
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with SS304
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with air
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with burnable poison
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with air
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with SS304
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with water
        cells.append(CellBasic(universe=3, material=dummy_id))
        #region with Zircaloy
        cells.append(CellBasic(universe=3, material=dummy_id))
        #outside region with water
        cells.append(CellBasic(universe=3, material=dummy_id))

        #first cell, region with air
        cells[7].addSurface(halfspace=-1, surface=circles[5])

        #second cell, region with SS304
        cells[8].addSurface(halfspace=-1, surface=circles[6])
        cells[8].addSurface(halfspace=+1, surface=circles[5])

        #third cell, region with air
        cells[9].addSurface(halfspace=-1, surface=circles[7])
        cells[9].addSurface(halfspace=+1, surface=circles[6])

        #region with burnable poison
        cells[10].addSurface(halfspace=-1, surface=circles[8])
        cells[10].addSurface(halfspace=+1, surface=circles[7])

        #region with air
        cells[11].addSurface(halfspace=-1, surface=circles[9])
        cells[11].addSurface(halfspace=+1, surface=circles[8])

        #region with SS304
        cells[12].addSurface(halfspace=-1, surface=circles[10])
        cells[12].addSurface(halfspace=+1, surface=circles[9])

        #region with water
        cells[13].addSurface(halfspace=-1, surface=circles[11])
        cells[13].addSurface(halfspace=+1, surface=circles[10])

        #region with Zircaloy
        cells[14].addSurface(halfspace=-1, surface=circles[12])
        cells[14].addSurface(halfspace=+1, surface=circles[11])

        #region with water
        cells[15].addSurface(halfspace=+1, surface=circles[12])

        #creates cells that are filled by the lattice universe
        cells.append(CellFill(universe=0, universe_fill=3))

        #giant cell
        cells[16].addSurface(halfspace=+1, surface=planes[0])
        cells[16].addSurface(halfspace=-1, surface=planes[1])
        cells[16].addSurface(halfspace=+1, surface=planes[2])
        cells[16].addSurface(halfspace=-1, surface=planes[3])

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

def createSolver(geometry, track_generator, num_threads, tolerance, max_iters, data=False):   

    solver = ThreadPrivateSolver(geometry, track_generator)
    solver.setNumThreads(num_threads)
    solver.setSourceConvergenceThreshold(tolerance)
    solver.convergeSource(max_iters)
    solver.printTimerReport()
    
    if data == True:    
        process.storeSimulationState(solver, use_hdf5 = True)

def plot_things(geometry, solver, egs, gs):
    
    plotter.plotCells(geometry, gridsize = gs ) #gs --> gridsize
    plotter.plotMaterials(geometry, gridsize = gs)
    plotter.plotFluxes(geometry, solver, energy_groups=egs) #egs --> energy_groups
