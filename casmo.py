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
    self._kinf = None
    self._pin_powers = None
    self._cell_type_array = None #this will be stored as an array of strings

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

  def parseKinf(self):
    f = open(self._directory + self._filename, 'r')

    '''parses k-infinity from CASMO output file'''
    for line in f:
        if "k-infinity" in line:
            tokens = line.split()
            kinf = float(tokens[2])
            break
    f.close()
    return kinf

  def getKinf(self): return self._kinf
  def setKinf(self,kinf): self._kinf = kinf
  def importKinf(self): self.setKinf(self.parseKinf())

  def parsePinPowers(self):
    f = open(self._directory + self._filename, 'r')

    dimension = self.parseDimensions()
    full_dimension = self.fullDimensions()
    pin_power_array = numpy.zeros((full_dimension,full_dimension), dtype=numpy.int32)
    small_array = numpy.zeros((dimension,dimension), dtype=numpy.int32)

    counter = 0
    '''parses pin powers from the CASMO output file'''
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
                small_array[counter-1, index] = float(power)
                small_array[index, counter-1] = float(power)
            counter += 1
    f.close()
    
    '''creates a 17x17 array and systematically fills with small_array'''
    pin_power_array[(dimension-1):,(dimension-1):] = small_array
    pin_power_array[(dimension-1):, 0:(dimension)] = numpy.fliplr(small_array)
    pin_power_array[0:(dimension), (dimension-1):] = numpy.flipud(small_array)
    pin_power_array[0:(dimension), 0:(dimension)] = numpy.flipud(numpy.fliplr(small_array))

    return pin_power_array

  def setPinPowers(self,pin_power_array): self._pin_powers = pin_power_array
  def getPinPowers(self): return self._pin_powers
  def importPinPowers(self): self.setPinPowers(self.parsePinPowers())

  def stringCellTypeArray(self):
    dimension = self.parseDimensions()
    full_dimension = self.fullDimensions()
    cell_type_array = numpy.zeros((full_dimension,full_dimension), dtype=numpy.int32)
    small_array = numpy.zeros((dimension,dimension), dtype=numpy.int32)

    '''parses cell types from CASMO output file'''
    counter = 0
    f = open(self._directory + self._filename, 'r')
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
                small_array[counter-1, index] = int(cell_type)
            counter += 1
    f.close()
    
    '''creates an array of all the cell types represented by whole numbers'''
    cell_type_array[(dimension-1):,(dimension-1):] = small_array
    cell_type_array[(dimension-1):, 0:(dimension)] = numpy.fliplr(small_array)
    cell_type_array[0:(dimension), (dimension-1):] = numpy.flipud(small_array)
    cell_type_array[0:(dimension), 0:(dimension)] = numpy.flipud(numpy.fliplr(small_array))
    
    '''converts numerical array to strings'''
    #id of 1 corresponds to fuel (string of fuel)
    #id of 2 corresponds to guide tube (string of gt)
    #id of 3 corresponds to burnable poison (string of bp)
    string_cell_type_array = numpy.zeros((full_dimension,full_dimension), dtype=numpy.int32)
    for i, row in enumerate(cell_type_array):
      for j, cell in enumerate(row):
        if cell_type_array[i,j] == 1:
          string_cell_type_array[i,j] = 'fuel'
        elif cell_type_array[i,j] == 2:
          string_cell_type_array[i,j] = 'gt'
        elif cell_type_array[i,j] == 3:
          string_cell_type_array[i,j] = 'bp'

    #center cell treated as a guide tube
    string_cell_type_array[dimension-1,dimension-1] = 'gt'
    
    return string_cell_type_array

  def getCellTypes(self): return self._cell_types
  def setCellTypes(self,cell_type_array): self._cell_types = cell_type_array
  def importCellTypes(self): self.setCellTypes(self.stringCellTypeArray())
