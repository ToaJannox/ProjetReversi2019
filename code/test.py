stableValue = [[-1 for i in range(0,10)] for j in range(0,10)]

stableValue[0][0] = 9
stableValue[0][9] = 5
stableValue[9][0] = 6
stableValue[9][9] = 7

for x in stableValue:
    print(x)