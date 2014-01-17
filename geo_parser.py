import numpy
import h5py
import os
import matplotlib.pyplot as plt
from os import walk

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups? '))

#sets directory to the directory location of the file
directory = "Cross-Section-Output/%s-group/" % (numgroups)
directory1 = "geo-data/%s-group/" % (numgroups)

#splits casmo files into tokens
def casmo_lister(files):
    casmo_list = files.split()
    return casmo_list

'''#multiple file parser
def multi_file_lister(path):
    answer = raw_input('Run for all files? (y/n) ')
    if answer == y:
        casmo_files = []
        for (dirpath, dirnames, filenames) in walk(path):
            casmo_files.extend(filenames)
            break
        for index, casmo_file in enumerate(casmo_files):
            if 'c4.' in casmo_file:
                casmo_file = casmo_file[3:13]
                casmo_files[index] = casmo_file
        return casmo_files
    elif answer == n:
        print 'Please enter file name manually'
        break
    else:
        print "Invalid response, please enter file name manually."'''



#sets cell_data variable to the file name used
cell_data = raw_input('What is/are the file names? (Enter each one separated by a space without \'c4.\' or the file extension.) ')
#puts tokens into list
cell_data_list = casmo_lister(cell_data)

#loops through casmo files
for cell_data in cell_data_list:

    #sets directory to the directory location of the file
    directory = "Cross-Section-Output/%s-group/" % (numgroups)
    directory1 = "geo-data/%s-group/" % (numgroups)

    #removes previously created hdf5 file for the results file
    os.system('rm ' + directory1 + cell_data + '-minmax.hdf5')
    
    #sets name of casmo file as filename
    filename = 'c4.' + cell_data + '.out'
    
    #parses geo-structure from CASMO output file
    f = open(directory + filename, "r")
    x=-1
    for line in f:
        if "Layout" in line:
            x += 1
            continue
        if x>=0 and line == '\n':
            break
        if x>=0:
            x += 1
    square4 = numpy.zeros((x,x))
    f.close()
    
    #parses cell_types from CASMO output file
    counter = 0
    f = open(directory + filename, 'r')
    for line in f:
        if counter >=1 and line == '\n':
            break
        if 'Layout' in line:
            counter += 1
            continue
        if counter >= 1:
            cell_types = line.split()
            for index, cell_type in enumerate(cell_types):
                cell_type = cell_type.strip('*')
                square4[counter-1, index] = int(cell_type)
            counter += 1
    f.close()
    
    #creates an array of all the cell types
    d = (2*x-1)
    bigsquare = numpy.zeros((d,d), dtype=numpy.int32)
    bigsquare[(x-1):,(x-1):] = square4
    bigsquare[(x-1):, 0:(x)] = numpy.fliplr(square4)
    bigsquare[0:(x), (x-1):] = numpy.flipud(square4)
    bigsquare[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(square4))

    '''fig = plt.figure()
    plt.title(cell_data + ' Pin Powers')
    plt.imshow(bigsquare, interpolation = "nearest")
    plt.show()'''

    f = open(directory + filename, 'r')
    
    #initializes small square of min and max values each
    squaremin = numpy.zeros((x,x), dtype=numpy.int32)
    squaremax = numpy.zeros((x,x), dtype=numpy.int32) 

    #parses min and max values and enters them into squaremin and squaremax   
    counter = 0
    for line in f:
        if counter >= 1 and "1_________" in line:
            break
        if "Micro-region" in line:
            counter += 1
            continue
        if counter >= 1:
            powers = line.split()
            for index, power in enumerate(powers):
                power = power.strip("*")
                power = power.strip("-")
                if index%2 ==0:
                    squaremin[counter-1, index/2] = float(power)
                    squaremin[index/2, counter-1] = float(power)
                else:
                    squaremax[counter-1, (index-1)/2] = float(power)
                    squaremax[(index-1)/2, counter-1] = float(power)
            counter += 1
    f.close()
    
    #creates a big array of minimum values of microregion ranges
    d = (2*x-1)
    bigsquaremin = numpy.zeros ((d,d), dtype=numpy.int32)
    bigsquaremin[(x-1):,(x-1):] = squaremin
    bigsquaremin[(x-1):, 0:(x)] = numpy.fliplr(squaremin)
    bigsquaremin[0:(x), (x-1):] = numpy.flipud(squaremin)
    bigsquaremin[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(squaremin))
    
    #creates a big array of maximum values of microregion ranges
    bigsquaremax = numpy.zeros ((d,d), dtype=numpy.int32)
    bigsquaremax[(x-1):,(x-1):] = squaremax
    bigsquaremax[(x-1):, 0:(x)] = numpy.fliplr(squaremax)
    bigsquaremax[0:(x), (x-1):] = numpy.flipud(squaremax)
    bigsquaremax[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(squaremax))

    #stores all data in -minmax file
    f = h5py.File(directory1 + cell_data + '-minmax.hdf5')
    f.attrs['Energy Groups'] = numgroups
    f.create_dataset('minregions', data = bigsquaremin)
    f.create_dataset('maxregions', data = bigsquaremax)
    f.create_dataset('cell_types', data = bigsquare)

    f.close()
