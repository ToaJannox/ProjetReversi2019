# -*- coding: utf-8 -*-

#Thanks to:
#Vaishnavi Sannidhanam 
# and Muthukaruppan Annamalai

from enum import Enum
import Reversi

class Stability(Enum):
    STABLE = 1
    UNSTABLE = -1

class EvaluatorVSMA:

    staticWeights = [[ 4,-3, 2, 2, 2, 2, 2, 2,-3, 4],
                     [-3,-4,-1,-1,-1,-1,-1,-1,-4,-3],
                     [ 2,-1, 1, 0, 0, 0, 0, 1,-1, 2],
                     [ 2,-1, 0, 1, 1, 1, 1, 0,-1, 2],
                     [ 2,-1, 0, 1, 1, 1, 1, 0,-1, 2],
                     [ 2,-1, 0, 1, 1, 1, 1, 0,-1, 2],
                     [ 2,-1, 0, 1, 1, 1, 1, 0,-1, 2],
                     [ 2,-1, 1, 0, 0, 0, 0, 1,-1, 2],
                     [-3,-4,-1,-1,-1,-1,-1,-1,-4,-3],
                     [ 4,-3, 2, 2, 2, 2, 2, 2,-3, 4]]
    @staticmethod
    def eval(board,player):
        opponent = board._flip(player)

    @staticmethod
    def _eval_partiy(board,player):
        (whites,blacks) = board.get_nb_pieces()
        if player == board._WHITE:
            return 100*(whites-blacks)/(whites+blacks)
        else:
            return 100*(blacks-whites)/(blacks+whites)

    @staticmethod
    def _eval_mobility(board,player,opponent):
        playerMobility = 0
        opponentMobility = 0
        for x in range(0, board.get_board_size()):
            for y in range(0, board.get_board_size()):
                if board.lazyTest_ValidMove(player, x, y):
                    playerMobility += 1
                if board.lazyTest_ValidMove(opponent, x, y):
                    opponentMobility += 1
        if (playerMobility + opponentMobility) != 0:
                return 100*(playerMobility-opponentMobility)/(playerMobility+opponentMobility)
        else:
            return 0
            
    @staticmethod
    def _eval_corner(board, player,opponent):
        playerCorners = 0
        opponentCorners= 0

        upLeftCorner = board._board[0][0]
        upRightCorner = [0][board.get_board_size()-1] 
        downLeftCorner = [board.get_board_size()-1][0]
        downRightCorner =[board.get_board_size()-1][board.get_board_size()-1]

        if upLeftCorner != board._EMPTY:
            if upLeftCorner == player:
                playerCorners += 1
            else:
                opponentCorners += 1

        if upRightCorner != board._EMPTY:
            if upRightCorner == player:
                playerCorners += 1
            else:
                opponentCorners += 1

        if downLeftCorner != board._EMPTY:
            if downLeftCorner == player:
                playerCorners += 1
            else:
                opponentCorners += 1

        if downRightCorner != board._EMPTY:
            if downRightCorner == player:
                playerCorners += 1
            else:
                opponentCorners += 1

        if(playerCorners + opponentCorners !=0):
            return 100 * (playerCorners - opponentCorners) / (playerCorners + opponentCorners)
        else :
            return 0
    @staticmethod
    def checkIfCellStable(x,y,board,stableValues):


       
    @staticmethod
    def _eval_stability(board,player,opponent):
        boardSize = board.get_board_size()-1
        stableValues = [[-1 for i in range(0,boardSize)] for j in range(0,boardSize)]

        playerStability = 0
        opponentStability= 0

        upLeftCorner = board._board[0][0]
        upRightCorner = [0][board.get_board_size()-1] 
        downLeftCorner = [board.get_board_size()-1][0]
        downRightCorner =[board.get_board_size()-1][board.get_board_size()-1]

        if upLeftCorner != board._EMPTY:
            if upLeftCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[0][0]=Stability.STABLE

        if upRightCorner != board._EMPTY:
            if upRightCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[0][board.get_board_size()-1]=Stability.STABLE

        if downLeftCorner != board._EMPTY:
            if downLeftCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[board.get_board_size()-1][0]=Stability.STABLE


        if downRightCorner != board._EMPTY:
            if downRightCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[board.get_board_size()-1][board.get_board_size()-1]=Stability.STABLE

        if (playerStability+opponentStability)!=0:
            for x in range(0, board.get_board_size()):
                for y in range(0, board.get_board_size()):
                    cell = board._board[x][y]
                    if(cell !=board._EMPTY and stableValues[x][y]!=Stability.STABLE):

                        if(x-1 <0): #cell is on left edge
                            
                            if((stableValues[x][y-1]==Stability.STABLE) or (stableValues[x][y+1]==Stability.STABLE)):
                                stableValues = Stability.STABLE
                                continue


                        elif(x+1 >boardSize): #cell is on right edge
                            if((stableValues[x][y-1]==Stability.STABLE) or (stableValues[x][y+1]==Stability.STABLE)):
                                stableValues = Stability.STABLE
                                continue

                        else:
                            if(y-1 <0): #cell is on top edge
                                if((stableValues[x-1][y]==Stability.STABLE) or (stableValues[x+1][y]==Stability.STABLE)):
                                    stableValues = Stability.STABLE
                                    continue
                            elif(y+1 > boardSize): #cell is on on bottom edge
                                if((stableValues[x-1][y]==Stability.STABLE) or (stableValues[x+1][y]==Stability.STABLE)):
                                    stableValues = Stability.STABLE
                                    continue
                            else:
                                stableNeighbours = 0
                                if((stableValues[x-1][y]==Stability.STABLE) or (stableValues[x+1][y]==Stability.STABLE)):
                                    stableNeighbours +=1
                                if((stableValues[x][y-1]==Stability.STABLE) or (stableValues[x][y+1]==Stability.STABLE)):
                                    stableNeighbours +=1
                                if((stableValues[x-1][y-1]==Stability.STABLE)or
                                   (stableValues[x-1][y+1]==Stability.STABLE)or
                                   (stableValues[x+1][y-1]==Stability.STABLE)or
                                   (stableValues[x+1][y+1]==Stability.STABLE)):
                                    stableNeighbours +=1
                                if(stableNeighbours ==3):
                                    stableValues[x][y]= Stability.STABLE
                                    continue
                                columnComplete = True
                                i = 0
                                while (i < boardSize) and columnComplete:
                                    if(board._board[i][y]==board._EMPTY):
                                        columnComplete = False
                                    i+=1
                                i = 0
                                lineComplete = True
                                while (i < boardSize) and lineComplete:
                                    if(board._board[x][i]==board._EMPTY):
                                        lineComplete = False
                                    i+=1
                                i = 0
                                diagDownComplete = True
                                # TODO
                                
            return 100 * (playerStability-opponentStability)/(playerStability+opponentStability)
        else:
            return 0

