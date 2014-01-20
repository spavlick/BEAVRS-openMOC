import subprocess
import tester_options

#Instantiates "options" object from "options" module and assigns it to options
options = tester_options.options()

#Gave the user multiple options to modify attributes for the simulation
options.parseArguments()

filename = options.filename
trackstest = options.trackstest
tracksvalues = options.tracksvalues
azimtest = options.azimtest
azimvalues = options.azimvalues
ringstest = options.ringstest
ringsvalues = options.ringsvalues
sectorstest = options.sectorstest
sectorsvalues = options.sectorsvalues
energygroups = options.energygroups

#turns strings that look like lists into actual lists
if tracksvalues != [0.1]:
    tracksvalues = [float(i) for i in tracksvalues.split(',')]
if azimvalues != [4]:
    azimvalues = [int(i) for i in azimvalues.split(',')]
if ringsvalues != [3]:
    ringsvalues = [int(i) for i in ringsvalues.split(',')]
if sectorsvalues != [16]:
    sectorsvalues = [int(i) for i in sectorsvalues.split(',')]

def tracks_tester(filename, tracksvalues, energygroups):
    print 'Varying Tracks...'
    for spacing in tracksvalues:
        f = open(filename, 'r+')
        for line in f:
            if 'numgroups = ' in line:
                print line
                old = str(line)
                line = line.replace(old, 'numgroups = %d' % (energygroups))
                print line
        f.close()
        subprocess.call(['python' , filename, '-s', str(spacing)])
        f = open(filename, 'r+')
        for line in f:
            if 'numgroups = ' in line:
                print line
                new = str(line)
                line = line.replace(new, old)
                print line
        f.close()
        print 'hi'

if trackstest == 'y':
    tracks_tester(filename, tracksvalues, energygroups)
