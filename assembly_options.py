import getopt, sys


class options:

    #default filename
    numgroups = 2    

    def parseArguments(self):    #defining the method parseArguments

        try:
            opts, args = getopt.getopt(sys.argv[1:], 
                                       'hn:', #each letter represents
                                       ['help',         #optional user
                                        'numgroups='])

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

            elif opt in ('-n', '--numgroups'):
                self.numgroups = int(arg)


