from openmoc.compatible.casmo import Casmo

creating_class = 'PASS'
set_assembly_name = 'PASS'
get_assembly_name = 'PASS'
set_file_name = 'PASS'
get_file_name = 'PASS'
set_directory = 'PASS'
get_directory = 'PASS'
parse_energy_groups = 'PASS'
import_energy_groups = 'PASS'
get_energy_groups = 'PASS'
parse_num_regions = 'PASS'
import_num_regions = 'PASS'
get_num_regions = 'PASS'
parse_fuel_pin_radii = 'PASS'
import_fuel_pin_radii = 'PASS'
get_fuel_pin_radii = 'PASS'
parse_lattice_pitch = 'PASS'
import_lattice_pitch = 'PASS'
get_lattice_pitch = 'PASS'
parse_scattering_cross_sections = 'PASS'
import_all_xs = 'PASS'
xs_errors = {}
parse_width = 'PASS'
import_width = 'PASS'
get_width = 'PASS'
parse_microregions = 'PASS'
import_microregions = 'PASS'
get_microregions = 'PASS'
parse_kinf = 'PASS'
import_kinf = 'PASS'
get_kinf = 'PASS'
parse_pin_powers = 'PASS'
import_pin_powers = 'PASS'
get_pin_powers = 'PASS'
set_cell_type = 'PASS'
get_cell_types = 'PASS'
parse_cell_type_array = 'PASS'
import_cell_type_array = 'PASS'
get_cell_type_array = 'PASS'
string_cell_type_array = 'PASS'
set_string_cell_type_array = 'PASS'
get_string_cell_type_array = 'PASS'
import_from_casmo = 'PASS'
export = 'PASS'
import_from_hdf5 = 'PASS'
xs_to_hdf5 = 'PASS'


#Creating class
try:
    test = Casmo()
except:
    creating_class = 'FAIL'

#set Assembly Name
try:
    test.setAssemblyName('pwru240w12')
except:
    set_assembly_name = 'FAIL'

#get Assembly name
try:
    print 'Assembly Name: ', test.getAssemblyName()
except:
    get_assembly_name = 'FAIL'

#set file name
try:
    test.setFileName('c4.pwru240w12.out')
except:
    set_file_name = 'FAIL'

#get Assembly name
try:
    print 'File Name: ', test.getFileName()
except:
    get_file_name = 'FAIL'

#set directory
try:
    test.setDirectory('Cross-Section-Output/2-group/')
except:
    set_directory = 'FAIL'

#get directory
try:
    print 'Directory: ', test.getDirectory()
except:
    get_directory = 'FAIL'

#parse energy groups
try:
    print 'Energy Groups (parser): ', test.parseEnergyGroups()
except:
    parse_energy_groups = 'FAIL'

#import energy groups
try:
    test.importEnergyGroups()
except:
    import_energy_groups = 'FAIL'

#get energy groups
try:
    print 'Energy Groups (getter): ', test.getEnergyGroups()
except:
    get_energy_groups = 'FAIL'

#parse number microregions
try:
    print 'Number Microregions (parser): ', test.parseNumRegions()
except:
    parse_num_regions = 'FAIL'

#import number microregions
try:
    test.importNumRegions()
except:
    import_num_regions = 'FAIL'

#get number microregions
try:
    print 'Number Microregions (getter): ', test.getNumRegions()
except:
    get_num_regions = 'FAIL'

#parse fuel pin radii
try:
    print 'Fuel Pin Radii (parser): ', test.parseFuelPinRadii()
except:
    parse_fuel_pin_radii = 'FAIL'

#import fuel pin radii
try:
    test.importFuelPinRadii()
except:
    import_fuel_pin_radii = 'FAIL'

#get fuel pin radii
try:
    print 'Fuel Pin Radii (getter): ', test.getFuelPinRadii()
except:
    get_fuel_pin_radii = 'FAIL'

#parse lattice pitch
try:
    print 'Lattice Pitch (parser): ', test.parseLatticePitch()
except:
    parse_lattice_pitch = 'FAIL'

#import lattice pitch
try:
    test.importLatticePitch()
except:
    import_lattice_pitch = 'FAIL'

#get lattice pitch
try:
    print 'Lattice Pitch (getter): ', test.getLatticePitch()
except:
    get_lattice_pitch = 'FAIL'

#parse scattering cross sections
try:
    print
    print 'Scattering Cross section matrix (parser)'
    print test.parseXS('SIGS')
    print
except:
    parse_scattering_cross_sections = 'FAIL'

#import all cross sections
try:
    test.importAllXS()
except:
    import_all_xs = 'FAIL'

#get all cross sections
for xs_name in ['SIGA', 'SIGD', 'SIGT', 'SIGF', 'SIGNF', 'CHI']:
    try:
        print
        print xs_name, '(getter)' 
        print test.getXS(xs_name)
        print
    except:
        errors[xs_name] = 'FAIL'

#parse width
try:
    print 'Width (parser): ', test.parseWidth()
except:
    parse_width = 'FAIL'

#import width
try:
    test.importWidth()
except:
    import_width = 'FAIL'

#get width
try:
    print 'Width (getter): ', test.getWidth()
except:
    get_width = 'FAIL'

#parse min and max microregion arrays
try:
    print
    print 'Min Microregions (parser)'
    print test.parseMicroregions()[0]
    print
    print 'Max Microregions (parser)'
    print test.parseMicroregions()[1]
    print
except:
    parse_microregions = 'FAIL'

#import min and max microregion arrays
try:
    test.importMicroregions()
except:
    import_microregions = 'FAIL'

#get min microregion array
try:
    print
    print 'Min Microregions (getter)'
    print test.getMinMicroregions()
    print
    print 'Max Microregions (getter)'
    print test.getMaxMicroregions()
    print
except:
    get_microregions = 'FAIL'

#parse kinf
try:
    print 'Kinf (parser): ', test.parseKinf()
except:
    parse_kinf = 'FAIL'

#import kinf
try:
    test.importKinf()
except:
    import_kinf = 'FAIL'

#get kinf
try:
    print 'Kinf (getter): ', test.getKinf()
except:
    get_kinf = 'FAIL'

#parse pin powers
try:
    print
    print 'Reference Pin Powers (parser): '
    print test.parsePinPowers()
    print
except:
    parse_pin_powers = 'FAIL'

#import pin powers
try:
    test.importPinPowers()
except:
    import_pin_powers = 'FAIL'

#get pin powers
try:
    print
    print 'Reference Pin Powers (getter): '
    print test.getPinPowers()
    print
except:
    get_pin_powers = 'FAIL'

#set cell types
try:
    test.setCellType(1, 'Fuel Pin')
    test.setCellType(2, 'Guide Tube')
    test.setCellType(3, 'Burnable Poison')
except:
    set_cell_type = 'FAIL'

#get cell types
try:
    print
    print 'Cell Types'
    print test.getCellTypes()
    print
except:
    get_cell_types = 'FAIL'

#parse cell type array
try:
    print
    print 'Cell Type Array (parser): '
    print test.parseCellTypeArray()
    print
except:
    parse_cell_type_array = 'FAIL'

#import cell type array
try:
    test.importCellTypeArray()
except:
    import_cell_type_array = 'FAIL'

#get cell type array
try:
    print
    print 'Cell Type Array (getter)'
    print test.getCellTypeArray()
    print
except:
    get_cell_type_array = 'FAIL'

#convert to string cell type array
try:
    print
    print 'String Cell Type Array (converter)'
    print test.stringCellTypeArray()
    print
except:
    string_cell_type_array = 'FAIL'

#set string cell type array
try:
    test.setStringCellTypeArray('This is an array. Believe me.')
except:
    set_string_cell_type_array = 'FAIL'

#get string cell type array
try:
    print
    print 'String Cell Type Array (converter)'
    print test.getStringCellTypeArray()
    print
except:
    get_string_cell_type_array = 'FAIL'

#import from casmo
try:
    test.importFromCASMO('c4.pwru240w12.out', 'Cross-Section-Output/2-group/')
except:
    import_from_casmo = 'FAIL'

# export all data
try:
    test.export()
except:
    export = 'FAIL'

#import from hdf5
try:
    test.importFromHDF5()
except:
    import_from_hdf5 = 'FAIL'

#xs to HDF5
try:
    test.xsToHDF5('pwru240w12')
except:
    xs_to_hdf5 = 'FAIL'

print 'Creating Class: ', creating_class
print 'Set Assembly Name: ', set_assembly_name
print 'Get Assembly Name: ', get_assembly_name
print 'Set File Name: ', set_file_name
print 'Get File Name: ', get_file_name
print 'Set Directory: ', set_directory
print 'Get Directory: ', get_directory
print 'Parse Energy Groups: ', parse_energy_groups
print 'Import Energy Groups: ', import_energy_groups
print 'Get Energy Groups: ', get_energy_groups
print 'Parse Num Regions: ', parse_num_regions
print 'Import Num Regions: ', import_num_regions
print 'Get Num Regions: ', get_num_regions
print 'Parse Fuel Pin Radii: ', parse_fuel_pin_radii
print 'Import Fuel Pin Radii: ', import_fuel_pin_radii
print 'Get Fuel Pin Radii: ', get_fuel_pin_radii
print 'Parse Lattice Pitch: ', parse_lattice_pitch
print 'Import Lattice Pitch: ', import_lattice_pitch
print 'Get Lattice Pitch: ', get_lattice_pitch
print 'Parse Scattering Cross Sections', parse_scattering_cross_sections
print 'Import All xs: ', import_all_xs
print 'Cross Section Errors: ', xs_errors
print 'Parse Width: ', parse_width
print 'Import Width: ', import_width
print 'Get Width: ', get_width
print 'Parse Microregions: ', parse_microregions
print 'Import Microregions: ', import_microregions
print 'Get Microregions: ', get_microregions
print 'Parse Kinf: ', parse_kinf
print 'Import Kinf: ', import_kinf
print 'Get Kinf: ', get_kinf
print 'Parse Pin Powers: ', parse_pin_powers
print 'Import Pin Powers: ', import_pin_powers
print 'Get Pin Powers: ', get_pin_powers
print 'Set Cell Type: ', set_cell_type
print 'Get Cell Types: ', get_cell_types
print 'Parse Cell Type Array: ', parse_cell_type_array
print 'Import Cell Type Array: ', import_cell_type_array
print 'Get Cell Type Array: ', get_cell_type_array
print 'String Cell Type Array: ', string_cell_type_array
print 'Set String Cell Type Array: ', set_string_cell_type_array
print 'Get String Cell Type Array: ', get_string_cell_type_array
print 'Import From Casmo: ', import_from_casmo
print 'Export: ', export
print 'Import From HDF5: ', import_from_hdf5
print 'XS to HDF5: ', xs_to_hdf5
