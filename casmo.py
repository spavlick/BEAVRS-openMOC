import numpy
import h5py
import os

class Casmo(object):
    def __init__(self, filename, directory, energy_groups):
        self._filename = filename
        self._directory = directory
        self._energy_groups = energy_groups
        self._num_regions = None
        self._siga = None
        self._sigd = None
        self._sigt = None
        self._sigf = None
        self._signf = None
        self._sigs = None
        self._chi = None

    def parseNumRegions(self):
        # write documentation for this
        f = open(directory + filename, 'r')
        counter = 0
        for line in f:
            if "Micro-region" in line:
                counter += 1
                continue
            if counter == 1:
                tokens = line.split()
                num_regions = int(tokens[1])
                break
        f.close()
        return num_regions

    def setNumRegions(self):
        # write doc for this
        self._num_regions = parseNumRegions()

    def parseXS(self, xs_name):
        '''Takes name of cross-section to be parsed, returns numpy array of
        cross\ sections.'''

        # Specify in documentation that xs should be ALLCAPSONEWORD

        f = open(directory + filename, 'r')
        counter = 0
        xs_array =
        for line in f:
            if xs_name in line:
                tokens = line.split()
                xs_array[counter, :] = [float(xs) for xs in tokens[2:2+numgroups]]
                counter += 1
            if counter == numregions:
                break #stops loop after array has been filled
        f.close()
        return xs_array
