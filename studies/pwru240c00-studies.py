from openmoc.options import Options
from tester import *
from casmo import *
import copy

options = Options()


#parses Casmo data
pwru240c00 = importxsFromCasmo('pwru240c00')
pwru240c00.setAssemblyName('pwru240c00')

#sets the number of energy groups
numgroups = pwru240c00.getEnergyGroups()

#sets assembly variable to the file name used
assembly_name = 'pwru240c00'
directory = 'casmo-data/'
geoDirectory = "../geo-data/%s-group/" % (numgroups)
pin_directory = 'casmo-reference/%s-group/' % (numgroups)

rings = 3
sectors = 8
note = 'rings = %d, sectors= %d' % (rings, sectors)

cellTypeArray = pwru240c00.getCellTypeArray()

pinCellArray = copy.deepcopy(cellTypeArray)

num_threads, track_spacing, num_azim, tolerance, max_iters = defineParameters(assembly_name)
materials = createMaterials(directory, assembly_name)
dummy, dummy_id, circles, planes = createSurfaces(numgroups, bp=False)
cells = createCells(rings, sectors, dummy_id, circles, planes)
lattice = createLattice(pwru240c00)
geometry = createGeometry(geoDirectory, assembly_name, dummy, materials, cells, pinCellArray, lattice)

#plot.plot_flat_source_regions(geometry, gridsize = 250)
#plot.plot_fluxes(geometry, solver, energy_groups=[2], gridsize=250)
#num_azim test values
num_azims = [i for i in range(4, 128, 4)]

os.system('rm ' + 'results/' + assembly_name + '-errors.h5')
if not os.path.exists('results'):
    os.makedirs('results')

f = h5py.File('results/' + assembly_name + '-errors.h5')
f.attrs['Energy Groups'] = numgroups
current_test = f.create_group('Azimuthal Angles Tests')


#simulation
for num_azim in num_azims:

    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
    max_error, mean_error, calculatedPinPowers = computePinPowerError(solver, pin_directory, assembly_name)
    kinf_error = computeKinfError(solver, pin_directory, assembly_name)
    azim_test = current_test.create_group('Num Azim = %d' % (num_azim))
    azim_test.create_dataset('Pin Powers', data = calculatedPinPowers)
    azim_test.create_dataset('Max Error', data = max_error)
    azim_test.create_dataset('Min Error', data = mean_error)
    azim_test.create_dataset('Kinf_Error', data = kinf_error)


#reset
num_azim = 32

#track_spacing test values
track_spacings = [0.1, 0.05, 0.01, 0.005]

current_test = f.create_group('Track Spacing Tests')

#simulation
for track_spacing in track_spacings:
    
    track_generator = createTrackGen(num_azim, geometry, track_spacing)
    solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
    max_error, mean_error, calculatedPinPowers= computePinPowerError(solver, pin_directory, assembly_name)
    kinf_error = computeKinfError(solver, pin_directory, assembly_name)
    track_test = current_test.create_group('Track Spacing = %d' % (track_spacing))
    track_test.create_dataset('Pin Powers', data = calculatedPinPowers)
    track_test.create_dataset('Max Error', data = max_error)
    track_test.create_dataset('Min Error', data = mean_error)
    track_test.create_dataset('Kinf_Error', data = kinf_error)

#reset
track_spacing = 0.05

#rings and sectors test values
rings_list = [1,2,3,4]
sectors_list = [4, 8, 12, 16]

current_test = f.create_group('Flat Source Region Tests')

#simulation
for rings in rings_list:
    ring_test = current_test.create_group('Rings = %d' % (rings))
    for sectors in sectors_list:
        pinCellArray = copy.deepcopy(cellTypeArray)
        cells = createCells(rings, sectors, dummy_id, circles, planes)
        lattice = createLattice(pwru240c00)
        geometry = createGeometry(geoDirectory, assembly_name, dummy, materials, cells, pinCellArray, lattice)
        track_generator = createTrackGen(num_azim, geometry, track_spacing)
        solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
        max_error, mean_error, calculatedPinPowers = computePinPowerError(solver, pin_directory, assembly_name)
        kinf_error = computeKinfError(solver, pin_directory, assembly_name)
        sector_test = ring_test.create_group('Sectors = %d' % (sectors))
        sector_test.create_dataset('Pin Powers', data = calculatedPinPowers)
        sector_test.create_dataset('Max Error', data = max_error)
        sector_test.create_dataset('Min Error', data = mean_error)
        sector_test.create_dataset('Kinf_Error', data = kinf_error)


f.close()
