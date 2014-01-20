from openmoc import *
import subprocess
import tester_options
import h5py
import openmoc.log as log

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

def createTrackGen(angle, geometry, track_spacing):
    ###########################################################################
    #######################   Creating the TrackGenerator   ###################
    ###########################################################################

    #The following runs the simulation for changes in FSR

    log.py_printf('NORMAL', 'Initializing the track generator...')

    #Creates an instance of the TrackGenerator class, takes three parameters
    track_generator = TrackGenerator(geometry, int(angle), track_spacing)
    #Runs the generateTracks() method of the TrackGenerator class
    track_generator.generateTracks()
    return track_generator

def createSolver(geometry, track_generator, num_threads, tolerance, max_iters):   
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

    process.storeSimulationState(solver, use_hdf5 = True)

def createGeometry(num_rings, num_sectors, geoDirectory, assembly, dummy, materials, cells, pinCellArray):
    ############################################################################
    ##########################   Creating the Geometry   #######################
    ############################################################################
    lattice = Lattice(id=100, width_x=0.62992*2, width_y=0.62992*2)
    #lattice.printString()
    f = h5py.File(geoDirectory + assembly + '-minmax.hdf5', "r")
    log.py_printf('NORMAL', 'Creating geometry...')

    geometry = Geometry() 

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
                cloned_cell.setNumSectors(num_sectors)
                #if k == 0:
                    #cloned_cell.setNumRings(num_rings)        
                
    lattice.setLatticeCells(pinCellArray)
    #lattice.printString()
    geometry.addLattice(lattice)

    geometry.initializeFlatSourceRegions()
    return geometry, lattice
