import h5py
import os
import numpy
import matplotlib.pyplot as plt

  
#sets the number of energy groups
numgroups = str(raw_input('How many energy groups? '))

#sets results variable to the file name used
results = raw_input('What is/are the file names? (Enter each one separated by a space without \'c4.\' or the file extension.) ')

def casmo_lister(files):
    casmo_list = files.split()
    return casmo_list

results_list = casmo_lister(results)

for results in results_list:

    #sets directory to the directory location of the file
    directory = "Cross-Section-Output/%s-group/" % (numgroups)
    directory1 = "casmo-reference/%s-group/" % (numgroups)

    #removes previously created hdf5 file for the results file
    os.system('rm ' + directory1 + results + '-results.hdf5')

    #creates filename variable
    filename = 'c4.' + results + '.out'

    #opens file
    f = open(directory + filename, "r")

    #parses k-infinity from CASMO output file
    for line in f:
        if "k-infinity" in line:
            words = line.split()
            kinf = float(words[2])
            break
    f.close()

    #opens file
    f = open(directory + filename, "r")

    counter = 0
    x = -1
    for line in f:
        if "Power Distribution" in line:
            x += 1
            continue
        if x >= 0 and line == "\n":
            break
        if x >= 0:
            x += 1
    square4 = numpy.zeros ((x,x))
    f.close()

    f = open(directory + filename, "r")
    #parses pin powers from the CASMO output file
    for line in f:
        if counter >= 1 and line == "\n":
            break
        if "Power Distribution" in line:
            counter += 1
            continue
        if counter >= 1:
            powers = line.split()
            for index, power in enumerate(powers):
                power = power.strip("*")
                square4[counter-1, index] = float(power)
                square4[index, counter-1] = float(power)
            counter += 1
    f.close()
       
    d = (2*x-1)
    bigsquare = numpy.zeros ((d,d))
    bigsquare[(x-1):,(x-1):] = square4
    bigsquare[(x-1):, 0:(x)] = numpy.fliplr(square4)
    bigsquare[0:(x), (x-1):] = numpy.flipud(square4)
    bigsquare[0:(x), 0:(x)] = numpy.flipud(numpy.fliplr(square4))

    fig = plt.figure()
    plt.title(results + ' Pin Powers')
    plt.imshow(bigsquare, interpolation = "nearest")
    plt.show()
    



    #creates hdf5 file for data
    f = h5py.File(directory1 + results + '-results.hdf5')
    f.attrs['K-Infinity'] = kinf
    f.create_dataset("Pin Powers", data = bigsquare)


    f.close()
