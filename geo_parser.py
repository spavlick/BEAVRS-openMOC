import numpy
import h5py
import os
import matplotlib.pyplot as plt

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups? '))

#sets cell_data variable to the file name used
cell_data = raw_input('What is/are the file names? (Enter each one separated by a space without \'c4.\' or the file extension.) ')

def casmo_lister(files):
    casmo_list = files.split()
    return casmo_list

cell_data_list = casmo_lister(cell_data)

for cell_data in cell_data_list:

    #sets directory to the directory location of the file
    directory = "Cross-Section-Output/%s-group/" % (numgroups)
    directory1 = "geo-data/%s-group/" % (numgroups)

    #removes previously created hdf5 file for the results file
    os.system('rm ' + directory1 + cell_data + '-cell_data.hdf5')

    filename = 'c4.' + cell_data + '.out'

    f = open(directory + filename, "r")

    #parses geo-structure from CASMO output file

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

    d = (2*x-1)
    bigsquare = numpy.zeros((d,d), dtype=numpy.int64)
    bigsquare[(x-1):,(x-1):] = square4
    bigsquare[(x-1):, 0:(x)] = numpy.fliplr(square4)
    bigsquare[0:(x), (x-1):] = numpy.flipud(square4)
    bigsquare[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(square4))

    '''fig = plt.figure()
    plt.title(cell_data + ' Pin Powers')
    plt.imshow(bigsquare, interpolation = "nearest")
    plt.show()'''

    f = open(directory + filename, 'r')

    squaremin = numpy.zeros((x,x))
    squaremax = numpy.zeros((x,x))    
    counter = 0
    for line in f:
        if counter >= 1 and "1_________" in line:
            break
        if "Micro-region" in line:
            counter += 1
            print line
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
    
    d = (2*x-1)
    bigsquare = numpy.zeros ((d,d))
    bigsquare[(x-1):,(x-1):] = squaremin
    bigsquare[(x-1):, 0:(x)] = numpy.fliplr(squaremin)
    bigsquare[0:(x), (x-1):] = numpy.flipud(squaremin)
    bigsquare[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(squaremin))

    bigsquaremax = numpy.zeros ((d,d))
    bigsquaremax[(x-1):,(x-1):] = squaremax
    bigsquaremax[(x-1):, 0:(x)] = numpy.fliplr(squaremax)
    bigsquaremax[0:(x), (x-1):] = numpy.flipud(squaremax)
    bigsquaremax[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(squaremax))

    print squaremin
    print squaremax

    f = h5py.File(directory1 + cell_data + '-minmax.hdf5')
    f.attrs['Energy Groups'] = numgroups
    f.create_dataset('minregions', data = bigsquare)
    f.create_dataset('maxregions', data = bigsquaremax)

    f.close()

#pwru240w12