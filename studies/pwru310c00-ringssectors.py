from openmoc.options import Options
from tester import *
from casmo import *
import copy

options = Options()


#parses Casmo data
pwru310c00 = importxsFromCasmo('pwru310c00')
pwru310c00.setAssemblyName('pwru310c00')

#sets the number of energy groups
numgroups = pwru310c00.getEnergyGroups()

#sets assembly variable to the file name used
assembly_name = "pwru310c00"
directory = "casmo-data/"
geoDirectory = "../geo-data/%s-group/" % (numgroups)
pin_directory = 'casmo-reference/%s-group/' % (numgroups)

rings = 3
sectors = 8
note = 'rings = %d, sectors= %d' % (rings, sectors)

cellTypeArray = pwru310c00.getCellTypeArray()

pinCellArray = copy.deepcopy(cellTypeArray)

num_threads, track_spacing, num_azim, tolerance, max_iters = defineParameters(assembly_name, '-ringssectors')
materials = createMaterials(directory, assembly_name)
dummy, dummy_id, circles, planes = createSurfaces(numgroups, bp=False)

os.system('rm ' + 'results/' + assembly_name + '-ringssectors-errors.h5')
if not os.path.exists('results'):
    os.makedirs('results')

f = h5py.File('results/' + assembly_name + '-ringssectors-errors.h5')
f.attrs['Energy Groups'] = numgroups
current_test = f.create_group('Flat Source Region Tests')

track_spacing = 0.05

#rings and sectors test values
rings_list = [1,2,3,4]
sectors_list = [4, 8, 12, 16]

#simulation
for rings in rings_list:
    ring_test = current_test.create_group('Rings = %d' % (rings))
    for sectors in sectors_list:
        pinCellArray = copy.deepcopy(cellTypeArray)
        cells = createCells(rings, sectors, dummy_id, circles, planes)
        lattice = createLattice(pwru310c00)
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
