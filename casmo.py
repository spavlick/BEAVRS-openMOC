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
    self._min_microregions = None
    self._max_microregions = None

  def parseNumRegions(self):
    '''Parses CASMO for total number of microregions in assembly.'''
    f = open(self._directory + self._filename, 'r')
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

  def setNumRegions(self): self._num_regions = self.parseNumRegions()

  def parseXS(self, xs_name):
    '''Takes name of cross-section to be parsed, returns numpy array of
    cross\ sections.'''

    # Specify in documentation that xs should be ALLCAPSONEWORD

    if xs_name != 'SIGS':
      xs_array = numpy.zeros(self._num_regions, self._energy_groups)
      f = open(self._directory + self._filename, 'r')
      counter = 0
      for line in f:
        if xs_name in line:
          tokens = line.split()
          xs_array[counter, :] = [float(xs) for xs in tokens[2:2+self._energy_groups]]
          counter += 1
        if counter == self._num_regions:
          break
      f.close()
      return xs_array

    if xs_name == 'SIGS':
      xs_array = numpy.zeros(self._num_regions, self._energy_groups, self._energy_groups)
      f = open(self._directory + self._filename, "r")
      cur_region = 0
      cur_group = 0
      for line in f:
        if xs_name in line:
          words = line.split()
          xs_array[cur_region, cur_group, :] = [float(xs) for xs in words[2:2+self._energy_groups]]
          cur_group += 1
        if cur_group == self._energy_groups:
          cur_region += 1
          cur_group = 0
        if cur_region == self._num_regions:
          break

    f.close()

  def setXS(self, xs_name, xs_array):
    '''Takes name of cross-section and numpy array with cross-section values,
    sets cross-section attribute.'''

    if xs_name == 'SIGA':
      self._siga = xs_array
    if xs_name == 'SIGD':
      self._sigd = xs_array
    if xs_name == 'SIGT':
      self._sigt = xs_array
    if xs_name == 'SIGF':
      self._sigf = xs_array
    if xs_name == 'SIGNF':
      self._signf = xs_array
    if xs_name == 'SIGS':
      self._sigs = xs_array
    if xs_name == 'CHI':
      self._chi = xs_array

  def getXS(self, xs_name):
    '''Retrieves cross-section attribute.'''

    if xs_name == 'SIGA':
      return self._siga
    if xs_name == 'SIGD':
      return self._sigd
    if xs_name == 'SIGT':
      return self._sigt
    if xs_name == 'SIGF':
      return self._sigf
    if xs_name == 'SIGNF':
      return self._signf
    if xs_name == 'SIGS':
      return self._sigs
    if xs_name == 'CHI':
      return self._chi

  def importXS(self, xs_name): self.setXS(xs_name, self.parseXS(xs_name))

  def importAllXS(self):
    xs_list = ['SIGA', 'SIGD', 'SIGT', 'SIGF', 'SIGNF', 'SIGS', 'CHI']
    for xs_name in xs_list:
      self.importXS(self, xs_name)

  def parseDimensions(self):
    '''Parses dimensions of one fourth the full array from CASMO.'''

    dimension = -1
    f = open(self._directory + self._filename, "r")
    for line in f:
      if "Layout" in line:
        dimension += 1
        continue
      if dimension>=0 and line == '\n':
        break
      if dimension>=0:
        dimension += 1
    f.close()
    return dimension

  def fullDimensions(self): return (self.parseDimensions()*2-1)

  def parseMinMicroregions(self):
    '''Parses minimum microregions for each assembly component.'''

    dimension = self.parseDimensions()
    full_dimension = self.fullDimensions()
    min_array = numpy.zeros((full_dimension,full_dimension), dtype=numpy.int32)
    small_array = numpy.zeros((dimension,dimension), dtype=numpy.int32)

    f = open(self._directory + self._filename, 'r')
    counter = 0
    for line in f:
      if counter >= 1 and "1_________" in line:
        break
      if "Micro-region" in line:
        counter += 1
        continue
      if counter >= 1:
        tokens = line.split()
        for index, token in enumerate(tokens):
          token = token.strip("*")
          token = token.strip("-")
          if index%2 ==0:
            small_array[counter-1, index/2] = float(token)
            small_array[index/2, counter-1] = float(token)
        counter += 1
    f.close()

    min_array[(dimension-1):,(dimension-1):] = small_array
    min_array[(dimension-1):, 0:(dimension)] = numpy.fliplr(small_array)
    min_array[0:(dimension), (dimension-1):] = numpy.flipud(small_array)
    min_array[0:(dimension), 0:(dimension)] = numpy.flipud(numpy.fliplr(small_array))

    return min_array

  def parseMaxMicroRegions(self):
    '''Parses maximum microregions for each assembly component.'''

    dimension = self.parseDimensions()
    full_dimension = self.fullDimensions()
    max_array = numpy.zeros((full_dimension,full_dimension), dtype=numpy.int32)
    small_array = numpy.zeros((dimension,dimension), dtype=numpy.int32)

    f = open(self._directory + self._filename, 'r')
    counter = 0
    for line in f:
      if counter >= 1 and "1_________" in line:
        break
      if "Micro-region" in line:
        counter += 1
        continue
      if counter >= 1:
        tokens = line.split()
        for index, token in enumerate(tokens):
          token = token.strip("*")
          token = token.strip("-")
          if index%2 !=0:
            max_array[counter-1, (index-1)/2] = float(token)
            max_array[(index-1)/2, counter-1] = float(token)
        counter += 1
    f.close()

    max_array[(dimension-1):,(dimension-1):] = small_array
    max_array[(dimension-1):, 0:(dimension)] = numpy.fliplr(small_array)
    max_array[0:(dimension), (dimension-1):] = numpy.flipud(small_array)
    max_array[0:(dimension), 0:(dimension)] = numpy.flipud(numpy.fliplr(small_array))

    return max_array

  def getMinMicroregions(self): return self._min_microregions
  def setMinMicroregions(self, min_array): self._min_microregions = min_array
  def importMinMicroregions(self): self.setMinMicroregions(self.parseMinMicroregions())
  def getMaxMicroregions(self): return self._max_microregions
  def setMaxMicroregions(self, max_array): self._max_microregions = max_array
  def importMaxMicroregions(self): self.setMaxMicroregions(self.parseMaxMicroRegions())
  def importMicroregions(self): self.importMinMicroregions(), self.setMaxMicroregions()
