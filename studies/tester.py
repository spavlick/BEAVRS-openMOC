from openmoc import *
from openmoc import options
import openmoc.plotter as plotter
import openmoc.log as log
import openmoc.process as process
import openmoc.materialize as materialize
import h5py
import numpy
import matplotlib.pyplot as plt
from casmo import *
options = options.Options()


def defineParameters(assembly_name, test_name):

    num_threads = options.getNumThreads()
    track_spacing = options.getTrackSpacing()
    num_azim = options.getNumAzimAngles()
    tolerance = options.getTolerance()
    max_iters = options.getMaxIterations()

    log.set_log_level('NORMAL')
    set_log_filename(assembly_name + test_name + '-log')

    return num_threads, track_spacing, num_azim, tolerance, max_iters

def importxsFromCasmo(assembly_name):

    assembly = Casmo()
    assembly.setCellTypes(1, 'fuel')
    assembly.setCellTypes(2, 'gt')

    assembly.importFromCASMO('c4.' + assembly_name + '.out', '../Cross-Section-Output/2-group/')
    f_temp = assembly.getXS('SIGF')
    chi_temp = assembly.getXS('CHI')
    fission_counter = 0
    for region in range(assembly._num_micro_regions):
        for group in range(assembly._energy_groups):
            fission_counter+=f_temp[region, group]
        if abs(fission_counter) > 0:
            if assembly._energy_groups == 2:
                chi_temp[region:] = numpy.array([1,0])
            if assembly._energy_groups == 8:
                chi_temp[region:] = numpy.array([7.560E-01, 2.438E-01, 1.808E-04, 0.000E+00, 0.000E+00, 0.000E+00,
0.000E+00, 0.000E+00])
        fission_counter = 0
    assembly.setXS('CHI', chi_temp)
    assembly.xsToHDF5(assembly_name)

    return assembly


def createMaterials(directory, assembly_name):

    log.py_printf('NORMAL', 'Importing materials data from HDF5...')

    materials = materialize.materialize(directory + assembly_name + '-materials.hdf5')
    
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
        cells.append(CellFill(universe=0, universe_fill=100))

        #giant cell
        cells[16].addSurface(halfspace=+1, surface=planes[0])
        cells[16].addSurface(halfspace=-1, surface=planes[1])
        cells[16].addSurface(halfspace=+1, surface=planes[2])
        cells[16].addSurface(halfspace=-1, surface=planes[3])

        return cells


def createLattice(assembly):
    log.py_printf('NORMAL', 'Creating simple 4x4 lattice...')
    lattice = Lattice(id=100, width_x=0.62992*2, width_y=0.62992*2)

    return lattice

def createGeometry(geoDirectory, assembly_name, dummy, materials, cells, pinCellArray, lattice):

    log.py_printf('NORMAL', 'Creating geometry...')
    geometry = Geometry() 
    geometry.addMaterial(dummy)

    for material in materials.values(): geometry.addMaterial(material)
    for cell in cells: geometry.addCell(cell)
    
    #extracts microregion ranges
    f = h5py.File(geoDirectory + assembly_name + '-minmax.hdf5', "r")
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
    lattice.setLatticeCells(pinCellArray)
    geometry.addLattice(lattice)

    geometry.initializeFlatSourceRegions()

    return geometry


def createTrackGen(num_azim, geometry, track_spacing):

    log.py_printf('NORMAL', 'Initializing the track generator...')
    track_generator = TrackGenerator(geometry, num_azim, track_spacing)
    track_generator.generateTracks()
    return track_generator

def createSolver(geometry, track_generator, num_threads, tolerance, max_iters, note = "", data=False):   

    solver = ThreadPrivateSolver(geometry, track_generator)
    solver.setNumThreads(num_threads)
    solver.setSourceConvergenceThreshold(tolerance)
    solver.convergeSource(max_iters)
    solver.printTimerReport()
    
    if data == True:    
        process.store_simulation_state(solver, use_hdf5 = True, note = note, pin_powers = True, fluxes = True)

    return solver

def plot_things(geometry, solver, egs, gs):
    
    plotter.plotCells(geometry, gridsize = gs ) #gs->gridsize
    plotter.plotMaterials(geometry, gridsize = gs)
    plotter.plotFluxes(geometry, solver, energy_groups=egs) #egs->energy_groups

def computePinPowerError(solver, pin_directory, assembly_name):

    #finds pin powers from simulation
    process.compute_pin_powers(solver, use_hdf5=True)      
    f = h5py.File('pin-powers/fission-rates.h5', 'r') 
    calculatedPinPowers = f['universe0']['fission-rates'][...]
    normalizedPinPowers = calculatedPinPowers/numpy.sum(calculatedPinPowers)
    f.close()

    #finds pin powers from casmo
    f = h5py.File(pin_directory + assembly_name + '-results.hdf5')
    actualPinPowers = f['Pin Powers'][...]
    f.close()
    normalized_actualPinPowers = actualPinPowers/numpy.sum(actualPinPowers)


    #finds pinError
    pinError = numpy.zeros(normalized_actualPinPowers.shape)
    for i in range(normalized_actualPinPowers.shape[0]):
        for j in range(normalized_actualPinPowers.shape[1]):
            if normalized_actualPinPowers[i][j] != 0:
                pinError[i][j] = (normalizedPinPowers[i][j] - normalized_actualPinPowers[i][j]) / normalized_actualPinPowers[i][j]
            elif normalized_actualPinPowers[i][j] == 0:
                pinError[i][j] = 0
    max_error = numpy.max(abs(pinError))
    pinError_sum = 0
    numErrors = 0
    for i in range(pinError.shape[0]):
        for j in range(pinError.shape[1]):
            pinError_sum += pinError[i][j]
            if pinError[i][j] != 0:
                numErrors += 1
    mean_error = pinError_sum / numErrors
    
    return max_error, mean_error, calculatedPinPowers


def computeKinfError(solver, pin_directory, assembly_name):

    #finds kinf from simulation
    calculated_kinf = solver.getKeff()
    #finds kinf from casmo
    f = h5py.File(pin_directory + assembly_name + '-results.hdf5')
    actual_kinf = f.attrs['K-Infinity']
    f.close()

    kinf_error = abs((calculated_kinf - actual_kinf)/(actual_kinf))

    return kinf_error

def storeError(assembly_name, study_name, max_errors, mean_errors, kinf_errors):
    
    f = h5py.File('results/' + assembly_name + '-errors.h5')
    f.attrs['Energy Groups'] = 2
    current_test = f.require_group(study_name)
    keys = max_errors.keys()
    for key in keys:
        current_test.require_dataset('%s_max_%s' % (study_name, key), (), '=f8', exact=False, data=max_errors[key])
        current_test.require_dataset('%s_mean_%s' % (study_name, key), (), '=f8', exact=False, data=mean_errors[key])
        current_test.require_dataset('%s_kinf_%s' % (study_name, key), (), '=f8', exact=False, data=kinf_errors[key])
    f.close()

def plotter(X, Y, title, x_name, y_name, x_scale, y_scale, filename, num_datasets, legend = []):
    fig = plt.figure()
    colors = ['b', 'g', 'r', 'k', 'm']
    for i in range(num_datasets):
        plt.plot(X[i], Y[i], colors[i] + 'o-', ms = 10, lw = 2)
    if x_name == 'Track Spacing':
        plt.axis([x_scale, 0, 0, y_scale])
    else:
        plt.axis([0, x_scale, 0, y_scale])
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.grid()
    if num_datasets > 1:
        plt.legend(legend)
    plt.show()
    fig.savefig(filename)

def pinPowerPlotter(pin_directory):

    f = h5py.File('pin-powers/fission-rates.h5', 'r')
    calculatedPinPowers = f['universe0']['fission-rates'][...]
    normalizedPinPowers = calculatedPinPowers/numpy.sum(calculatedPinPowers)
    f.close()

    plt.figure()
    plt.pcolor(numpy.linspace(0, 17, 17), numpy.linspace(0, 17, 17), normalizedPinPowers, edgecolors = 'k', linewidths = 1, vmin = normalizedPinPowers[:,:].min(), vmax = normalizedPinPowers[:,:].max())
    plt.colorbar()
    plt.axis([0,17,0,17])
    plt.title('Normalized Pin Powers')
    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.show()
