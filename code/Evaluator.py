# -*- coding: utf-8 -*-

# Thanks to:
# Vaishnavi Sannidhanam
# and Muthukaruppan Annamalai

from enum import Enum
import Reversi


class Evaluator:
    _STABLE = 1
    _UNSTABLE = -1

    @staticmethod
    def eval(board,player):
        opponent = board._flip(player)

        if board.is_game_over():
            return Evaluator._eval_parity(board, player)
        return Evaluator._eval_corner(board, player, opponent) + Evaluator._eval_mobility(board, player, opponent) + Evaluator._eval_stability(board, player, opponent)

    @staticmethod
    def _eval_parity(board, player):
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
        upRightCorner = board._board[0][board.get_board_size()-1] 
        downLeftCorner = board._board[board.get_board_size()-1][0]
        downRightCorner =board._board[board.get_board_size()-1][board.get_board_size()-1]

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

    # stability can be evaluated as follows
    # if a piece is in a corner it's stable
    # else if it is on a edge vertical or horizontal we check for the stablitily of neighbours above and under or on the left or right
    # else if it has 4 stable neighbours in 4 differents direction (horizontal,vertical or diagonals)
    # else we check that piece is the intersection of a complete vertical line, complete horizontal line and 2 complete diagonals
    @staticmethod
    def _eval_stability(board,player,opponent):
        boardSize = board.get_board_size()
        stableValues = [[Evaluator._UNSTABLE for i in range(0, boardSize)] for j in range(0, boardSize)]

        playerStability = 0
        opponentStability= 0

        upLeftCorner = board._board[0][0]
        upRightCorner = board._board[0][boardSize-1] 
        downLeftCorner = board._board[boardSize-1][0]
        downRightCorner =board._board[boardSize-1][boardSize-1]
        # the first step is to check if the piece is in a corner. If so the piece is assured to be stable

        if upLeftCorner != board._EMPTY:
            if upLeftCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[0][0]=Evaluator._STABLE

        if upRightCorner != board._EMPTY:
            if upRightCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[0][boardSize-1]=Evaluator._STABLE

        if downLeftCorner != board._EMPTY:
            if downLeftCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[boardSize-1][0]=Evaluator._STABLE


        if downRightCorner != board._EMPTY:
            if downRightCorner == player:
                playerStability += 1
            else:
                opponentStability += 1
            stableValues[boardSize-1][boardSize-1]=Evaluator._STABLE
        # if the piece is not in a corner, then we have to manually check the stability of every other piece
        if (playerStability+opponentStability)!=0:
            for x in range(0, boardSize):
                for y in range(0, boardSize):
                    cell = board._board[x][y]
                    # we of course don't check for already stable pieces (the corners)
                    if((cell !=board._EMPTY) and (stableValues[x][y] != Evaluator._STABLE)):
                        # then we check for every piece that are on the edge of the board
                        if(x==0): #cell is on left edge
                            
                            if((stableValues[x][y-1] == Evaluator._STABLE) or (stableValues[x][y + 1] == Evaluator._STABLE)):
                                stableValues[x][y] = Evaluator._STABLE
                                continue


                        elif(x==boardSize-1): #cell is on right edge
                            if((stableValues[x][y-1] == Evaluator._STABLE) or (stableValues[x][y + 1] == Evaluator._STABLE)):
                                stableValues[x][y] = Evaluator._STABLE
                                continue

                        else:
                            if(y==0): #cell is on top edge
                                if((stableValues[x-1][y] == Evaluator._STABLE) or (stableValues[x + 1][y] == Evaluator._STABLE)):
                                    stableValues[x][y] = Evaluator._STABLE
                                    continue
                            elif(y==boardSize-1): #cell is on on bottom edge
                                if((stableValues[x-1][y] == Evaluator._STABLE) or (stableValues[x + 1][y] == Evaluator._STABLE)):
                                    stableValues[x][y] = Evaluator._STABLE
                                    continue
                                
                            else:
                                # if the piece is neither on a edge or in a corner we check if it has 4 neighbours in 4 differents directions
                                stableNeighbours = 0
                                if((stableValues[x-1][y] == Evaluator._STABLE) or (stableValues[x + 1][y] == Evaluator._STABLE)):
                                    stableNeighbours +=1
                                if((stableValues[x][y-1] == Evaluator._STABLE) or (stableValues[x][y + 1] == Evaluator._STABLE)):
                                    stableNeighbours +=1
                                if ((stableValues[x-1][y-1] == Evaluator._STABLE) or
                                   (stableValues[x+1][y+1] == Evaluator._STABLE)):
                                    stableNeighbours +=1
                                if ((stableValues[x-1][y+1] == Evaluator._STABLE)or
                                   (stableValues[x+1][y-1] == Evaluator._STABLE)):
                                    stableNeighbours +=1
                                if(stableNeighbours ==4):
                                    stableValues[x][y]= Evaluator._STABLE
                                    continue
                                # if this is not enough we finally check if the piece is standing in the intersection of a complete column, line and 2 diagonals
                                columnComplete = True
                                i = 0
                                while (i < boardSize) and columnComplete:
                                    if(board._board[i][y]==board._EMPTY):
                                        columnComplete = False
                                    i+=1
                                if(not columnComplete):
                                    continue
                                i = 0
                                lineComplete = True
                                while (i < boardSize) and lineComplete:
                                    if(board._board[x][i]==board._EMPTY):
                                        lineComplete = False
                                    i+=1
                                if(not lineComplete):
                                    continue
                                i = 0
                                diag1Complete = True
                                diag2Complete = True
                                i = 0
                                while(i < boardSize) and (diag1Complete and diag2Complete):
                                    j = 0
                                    while(j < boardSize) and (diag1Complete and diag2Complete):
                                        if((x-y) == (i-j)):
                                            if(board._board[i][j]==board._EMPTY):
                                                diag1Complete = False;
                                        if((x+y) == (i+j)):
                                            if(board._board[i][j]==board._EMPTY):
                                                diag2Complete = False;
                                        j+=1
                                    i+=1
                                if( (not diag1Complete) or (not diag2Complete)):
                                    continue
                                stableValues[x][y]=Evaluator._STABLE;

            for x in range(0,boardSize):                    
                for y in range(0,boardSize):
                    if(stableValues[x][y]==Evaluator._STABLE):
                        if(board._board[x][y]==player):
                            playerStability+=1
                        else:
                            opponentStability+=1

            return 100 * (playerStability-opponentStability)/(playerStability+opponentStability)
        else:
            return 0

