import numpy as np
import h5py
import os

#c4.pwru160c00.out  c4.pwru240w12.out  c4.pwru310w12.out
#c4.pwru240c00.out  c4.pwru310c00.out


geometry = 'pwru310w12'
os.system('rm ' + geometry + '-materials.hdf5')

#numgroups = 2 #make user input
filename = 'c4.' + geometry + '.out'
directory = "Cross-Section-Output/2-group/" #%(numgroups)
f = open(directory + filename, "r")
#f.read()
lines = []
counter = 0
for line in f: #finds line with "KRMXSN" and parses the next one
    if "KRMXSN" in line:
        lines.append(line) #for debugging; we don't actually need this line right now
        counter += 1
        continue #returns back to line 9 and reads code from there
    if counter == 1:
        words = line.split()
        print line
        numgroups = int(words[3])
        break
print lines
f.close()

f = open(directory + filename, "r")
lines = []
counter = 0
for line in f: #finds line with "full assembly" and parses the next one
    if "full assembly" in line:
        lines.append(line) #for debugging; we don't actually need this line right now
        counter += 1
        continue 
    if counter == 1:
        words = line.split()
        print line
        numregions = int(words[4])
        break
#print numgroups
#print numregions
#print lines
f.close()

siga = np.zeros((numregions, numgroups))
sigd = np.zeros((numregions, numgroups))
sigt = np.zeros((numregions, numgroups))
sigf = np.zeros((numregions, numgroups))
signf = np.zeros((numregions, numgroups))
sigs = np.zeros((numregions, numgroups, numgroups))

def parseXS(name, array):
    f = open(directory + filename, "r")
    lines = []
    counter = 0
    for line in f: 
        if name in line:
            words = line.split()
            print line
            array[counter, :] = [float(xs) for xs in words[2:2+numgroups]] 
            counter += 1
        if counter == numregions:
            break
    f.close()

def parseXS_scatter(name, array):
    f = open(directory + filename, "r")
    lines = []
    cur_region = 0
    cur_group = 0
    for line in f: 
        # splits line into tokens, adds values to numpy array
        if name in line:
            words = line.split()
            array[cur_region, cur_group, :] = [float(xs) for xs in words[2:2+numgroups]] #fills the array row by row, microregion by microregion
            cur_group += 1 #adds one to the cur_group after each group
        if cur_group == numgroups: #
            cur_region += 1
            cur_group = 0

        if cur_region == numregions:
            break
    f.close()

parseXS("SIGA", siga)
parseXS("SIGD", sigd)
parseXS('SIGT', sigt)
parseXS("SIGF", sigf)
parseXS("SIGNF", signf)
parseXS_scatter("SIGS", sigs)


f = h5py.File(geometry + '-materials.hdf5')

f.attrs['Energy Groups'] = numgroups

for region in range(numregions):
    material = f.create_group('microregion-' + str((region + 1)))
    material.create_dataset('Total XS', data=sigt[region, :])
    material.create_dataset('Absorption XS', data=siga[region, :])
    material.create_dataset('Fission XS', data=sigf[region, :])
    material.create_dataset('Nu Fission XS', data=signf[region, :])
    material.create_dataset('Scattering XS', data=np.ravel(sigs[region, :, :]))
    material.create_dataset('Dif Coefficient', data=sigd[region, :])
    #material.create_dataset('Chi', data=chi)
f.close()

print "THIS IS SIG A"
print siga
print "\n\n\n"

print "THIS IS SIG D"
print sigd
print "\n\n\n"

print "THIS IS SIG F"
print sigf
print "\n\n\n"

print "THIS IS SIG NF"
print signf
print "\n\n\n"

print "THIS IS SIG s"
print sigs
print "\n\n\n"

