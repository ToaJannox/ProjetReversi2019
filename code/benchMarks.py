from localGame import *

data = [0, 0, 0]
n = 1

for i in range(0,n):
    res  = localGame()
    data[res] += 1
print(data)
blackRate = (data[2]/n)*100
whiteRate = (data[1]/n)*100
drawRate = (data[0]/n)*100
print("Black won %d %% of the time" % blackRate)
print("White won %d %% of the time" % whiteRate)
print("Draw %d %% of the time" % drawRate)

