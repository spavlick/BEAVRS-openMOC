import numpy as np
import h5py
import os

#sets the number of energy groups
numgroups = str(raw_input('How many energy groups? '))

#sets casmo_files variable to the file name used
casmo_files = raw_input('What is/are the file names? (Enter each one separated by a space without \'c4.\' or the file extension.) ')

#separates list of casmo files into tokens
def casmo_lister(files):
    casmo_list = files.split()
    return casmo_list

#returns list of casmo_files
casmo_list = casmo_lister(casmo_files)

#loops through files
for casmo_files in casmo_list:

    #creates filename variable
    filename = 'c4.' + casmo_files + '.out'
    
    #sets directory to the directory location of the CASMO file
    directory = "Cross-Section-Output/%s-group/" % (numgroups)
    directory1 = 'materials/%s-group/' % (numgroups)

    #removes previously created hdf5 file for the casmo_files file
    os.system('rm ' + directory1 + casmo_files + '-materials.hdf5')

    #opens file
    f = open(directory + filename, "r")
    
    #f.read()
    lines = []
    counter = 0
    for line in f: #finds line with "KRMXSN" and parses the next one
        if "KRMXSN" in line:
            counter += 1
            continue #returns back to beginning of for loop
        if counter == 1: #allows for line after KRMXSN to be read
            words = line.split() #parses line into separate words
            numgroups = int(words[3]) #finds number of groups from line
            break #stops look after finding numgroups
    f.close()

    #begins reading file again from beginning of file
    f = open(directory + filename, "r")
    lines = []
    counter = 0
    for line in f: #finds line with "full assembly" and parses the next one
        if "full assembly" in line:
            counter += 1
            continue 
        if counter == 1:
            words = line.split()
            numregions = int(words[4])
            break
    f.close()

    #creates empty arrays for XS data using variables read from file
    siga = np.zeros((numregions, numgroups))
    sigd = np.zeros((numregions, numgroups))
    sigt = np.zeros((numregions, numgroups))
    sigf = np.zeros((numregions, numgroups))
    signf = np.zeros((numregions, numgroups))
    sigs = np.zeros((numregions, numgroups, numgroups))

    #function to read XS data from file
    def parseXS(name, array):
        f = open(directory + filename, "r")
        lines = []
        counter = 0
        for line in f: 
            if name in line: #finds lines with the XS name
                words = line.split()
                #inputs line data to array
                array[counter, :] = [float(xs) for xs in words[2:2+numgroups]] 
                counter += 1
            if counter == numregions:
                break #stops loop after array has been filled
        f.close()

    #function to read data for the scattering XS
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
            if cur_group == numgroups:
                cur_region += 1
                cur_group = 0

            if cur_region == numregions:
                break
        f.close()

    #calls function for each XS type
    parseXS("SIGA", siga)
    parseXS("SIGD", sigd)
    parseXS('SIGT', sigt)
    parseXS("SIGF", sigf)
    parseXS("SIGNF", signf)
    parseXS_scatter("SIGS", sigs)

    #creates hdf5 file for data
    f = h5py.File(directory1 + casmo_files + '-materials.hdf5')

    f.attrs['Energy Groups'] = numgroups

    #loop to input data for each microregion
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

    #prints data
    '''
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
    '''

