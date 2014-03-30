from openmoc.options import Options
from openmoc import plotter
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
geoDirectory = "../../geo-data/%s-group/" % (numgroups)
pin_directory = '../casmo-reference/%s-group/' % (numgroups)

rings = 3
sectors = 8
num_azim = 60
track_spacing = 0.1

cellTypeArray = pwru310c00.getCellTypeArray()

pinCellArray = copy.deepcopy(cellTypeArray)

num_threads, track_spacing, num_azim, tolerance, max_iters = defineParameters(assembly_name, '')
materials = createMaterials(directory, assembly_name)
dummy, dummy_id, circles, planes = createSurfaces(numgroups, bp=False)
cells = createCells(rings, sectors, dummy_id, circles, planes)
lattice = createLattice(pwru310c00)
geometry = createGeometry(geoDirectory, assembly_name, dummy, materials, cells, pinCellArray, lattice)
track_generator = createTrackGen(num_azim, geometry, track_spacing)
solver = createSolver(geometry, track_generator, num_threads, tolerance, max_iters)
kinf = solver.getKeff()

# writes kinf to file
f = h5py.File('../best-case-kinf-values.hdf5')
f.attrs['Energy Groups'] = numgroups
kinf_group = f.create_group('pwru310c00')
kinf_group.create_dataset('kinf', data=kinf)
f.close()

#plotter.plot_fluxes(geometry, solver, energy_groups=[1,2], gridsize = 1200)

