import numpy
#numgroups = 2 #make user input
filename = "c4.pwru240c00.out"
directory = "Cross-Section-Output/8-group/" #%(numgroups)
f = open(directory + filename, "r")
#f.read()
lines = []
counter = 0
for line in f:
    if counter == 1:
        words = line.split()
        print line
        numgroups = int(words[3])
        break
    if "KRMXSN" in line:
        lines.append(line)
        counter += 1
print numgroups
print lines
f.close()
