import h5py
import os
import numpy
import matplotlib.pyplot as plt

  



#sets directory to the directory location of the file
directory = "Cross-Section-Output/2-group/" #%(numgroups)
directory1 = "casmo-reference/2-group/" #%(numgroups)

#sets geometry variable to the file name used
geometry = 'pwru310c00'
#removes previously created hdf5 file for the geometry file
os.system('rm ' + directory1 + geometry + '-results.hdf5')

#creates filename variable
filename = 'c4.' + geometry + '.out'

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
plt.imshow(bigsquare, interpolation = "nearest")
plt.show()




#creates hdf5 file for data
f = h5py.File(directory1 + geometry + '-results.hdf5')
f.attrs['K-Infinity'] = kinf
f.create_dataset("Pin Powers", data = bigsquare)


f.close()
