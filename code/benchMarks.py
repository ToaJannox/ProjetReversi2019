from localGame import *
import myPlayer
import myPlayerBook
import RandomPlayer
from itertools import permutations

def benchmark(n,players):
    
    matches = list(permutations(players,2))
    data = []
    for match in matches:       
        print(match[0].getPlayerName()," vs ",match[1].getPlayerName())
        matchData = [0,0,0]
        for j in range(0,n):
            players = []
            player1 = match[0]
            player2 = match[1]
            players.append(player1)
            players.append(player2)
            result = localGame(players)
            matchData[result] +=1
            players.clear()
            print("Game ",j+1," done")
        data.append(matchData)
    for i in range(0,len(matches)):
        black = matches[i][0]
        white = matches[i][1]
        print("===[Results of ",black.getPlayerName()," vs ",white.getPlayerName(),"]===")
        blackWins = data[i][2]
        whiteWins = data[i][1]
        draws = data[i][0]
        blackRate = (blackWins/n)*100
        whiteRate = (whiteWins/n)*100
        drawRate = (draws/n)*100
        print("%s won %d %% (%d) of the time" % (black.getPlayerName(), blackRate,blackWins))
        print("%s won %d %% (%d) of the time" % (white.getPlayerName(), whiteRate,whiteWins))
        print("Draw %d %% (%d) of the time" % (drawRate,draws))
        print("===============================")

    
n = 1

playerRand = RandomPlayer.RandomPlayer()
playerV1 = myPlayer.myPlayer()
playerV2 = myPlayerBook.myPlayerBook()

players = []

players.append(playerV1)
players.append(playerV2)

benchmark(n,players)