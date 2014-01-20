import getopt, sys


class options:

    #default filename
    filename = ''    

    #whether or not we're running trackstest
    trackstest = 'n'
    
    #whether or not we're running sectors test
    tracksvalues = [0.1]

    #whether or not we're running azimuthyl angles test
    azimtest = 'n'

    #whether or not we're running sectors test
    azimvalues = [4]

    #whether or not we're running rings test
    ringstest = 'n'

    #whether or not we're running sectors test
    ringsvalues = [3]
    
    #whether or not we're running sectors test
    sectorstest = 'n'   
            
    #whether or not we're running sectors test
    sectorsvalues = [16]

    #energy group value default
    energygroups = 2

    def parseArguments(self):    #defining the method parseArguments

        try:
            opts, args = getopt.getopt(sys.argv[1:], 
                                       'hf:t:w:a:x:r:y:s:z:e:', #each letter represents
                                       ['help',         #optional user
                                        'filename=',        #command line inputs
                                        'trackstest=',
                                        'tracksvalues=',
                                        'azimtest=',
                                        'azimvalues=',
                                        'ringstest=',
                                        'ringsvalues=',
                                        'sectorstest=',
                                        'sectorsvalues=',
                                        'energygroups='])

        except getopt.GetoptError as err:   #if user enters invalid command,
            print ('WARNING'+ str(err))     #error message is printed and 'pass'
            pass                            #allows the program to run on defaults

        # Parse the command line arguments
        for opt, arg in opts:

            # Print a report of all supported runtime options and exit
            if opt in ('-h', '--help'):

                print '{:-^80}'.format('')
                print '{: ^80}'.format('Tester runtime options')
                print '{:-^80}'.format('')
                print

                categories = '  {: <16}'.format('[command]')
                categories += '\t{: <18}'.format('[default]')
                categories += '[description]'
                print categories
                print

                help = '  {: <40}'.format('-h, --help')
                help += 'Report Game of Life runtime options\n'
                print help              
 
                filename = '  {: <14}'.format('-f, --filename')
                filename += '\t{: <18}'.format('')
                filename += 'Name of file to be tested\n'
                print filename

                trackstest = '  {: <14}'.format('-t, --trackstest')
                trackstest += '\t{: <18}'.format('n')
                trackstest += 'Option to run test varying track space\n'
                print trackstest

                azimtest = '  {: <10}'.format('-a, --azimtest')
                azimtest += '\t{: <18}'.format('n')
                azimtest += 'Option to test varying angles\n'
                print azimtest

                ringstest = '  {: <10}'.format('-r, --ringstest')
                ringstest += '\t{: <18}'.format('n')
                ringstest += 'Option to test varying rings\n'
                print ringstest

                sectorstest = '  {: <10}'.format('-s, --sectorstest')
                sectorstest += '\t{: <18}'.format('n')
                sectorstest += 'Option to test varying sectors\n'
                print sectorstest

                sys.exit()

            elif opt in ('-f', '--filename'):
                self.filename = str(arg)

            elif opt in ('-t', '--trackstest'):
                self.trackstest = str(arg)

            elif opt in ('-w', '--tracksvalues'):
                self.tracksvalues = arg

            elif opt in ('-a', '--azimtest'):
                self.azimtest = str(arg)

            elif opt in ('-x', '--azimvalues'):
                self.azimvalues = arg

            elif opt in ('-r', '--ringstest'):
                self.ringstest = str(arg)

            elif opt in ('-y', '--ringsvalues'):
                self.ringsvalues = arg

            elif opt in ('-s', '--sectorstest'):
                self.sectorstest = str(arg)

            elif opt in ('-z', '--sectorsvalues'):
                self.sectorsvalues = arg

            elif opt in ('-e', '--energygroups'):
                self.energygroups = int(arg)
