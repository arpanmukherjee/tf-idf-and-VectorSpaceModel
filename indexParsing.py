import sys

path = sys.argv[1]
f = open(path+"docId.txt", "w")
lines = [line.rstrip('\n') for line in open(path+'/index.html')]
for item in lines:
    temp = item.split(' ')
    f.write(temp[2]+" ")
    for i in range(4, len(temp)):
        f.write(temp[i]+" ")
    f.write("\n")
f.close()