import numpy as np
#numgroups = 2 #make user input
filename = "c4.pwru240c00.out"
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
sigt = np.zeros((numregions, numgroups))
sigf = np.zeros((numregions, numgroups))
signf = np.zeros((numregions, numgroups))
sigs = np.zeros((numregions, numgroups, numgroups))

f = open(directory + filename, "r")
lines = []
counter = 0
for line in f: 
    if "SIGA" in line:
        words = line.split()
        print line
        siga[counter, :] = [float(xs) for xs in words[2:2+numgroups]] 
        counter += 1
    if counter == numregions:
        break
print siga
f.close()

