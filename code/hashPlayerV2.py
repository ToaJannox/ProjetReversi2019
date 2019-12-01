# -*- coding: utf-8 -*-

import time

from Evaluator import Evaluator
import Reversi
import sys
from random import randint
from playerInterface import *
import OpeningBook
from TranspositionTable import *


class hashPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None
        self._opening_book = OpeningBook.OpeningBook()
        self._OB_active = True
        self._move_history = []
        self._hash_table = TranspositionTable()
        self._table_usage = 0

    def getPlayerName(self):
        return "Hash Player: Nega Max"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)

        # Compute player move
        move = self._play()

        self._board.push(move)
        print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)
        print("My current board :")
        print(self._board)

        self._move_history.append(move)  # Add player's move to history
        return (x, y)

    def playOpponentMove(self, x, y):
        assert (self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x, y))

        self._move_history.append([self._opponent, x, y])  # Add opponent's move to history
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2
        self._opening_book.init(self._board.get_board_size())

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")
        print("Used table %d times" % self._table_usage)


    def _play(self):
        # Killer move detection
        # # Corner
        max_value = - sys.maxsize - 1
        best_move = None
        corners = [[0, 0],
                   [0, self._board.get_board_size()-1],
                   [self._board.get_board_size()-1, 0],
                   [self._board.get_board_size()-1, self._board.get_board_size()-1]]
        for m in self._board.legal_moves():
            self._board.push(m)
            (_, x, y) = m
            if [x, y] in corners:
                max_value = max(max_value, Evaluator.eval(self._board, self._mycolor))
                best_move = m
            self._board.pop()

        if best_move is not None:
            return best_move

        # # Blocking move
        max_value = - sys.maxsize - 1
        best_move = None
        for m in self._board.legal_moves():
            self._board.push(m)
            if not self._board.at_least_one_legal_move(self._opponent):
                max_value = max(max_value, Evaluator.eval(self._board, self._mycolor))
                best_move = m
            self._board.pop()

        if best_move is not None:
            return best_move

        # Opening move
        if self._OB_active:
            move = self._opening_book.get_following_move(self._move_history)
            if move is not None:
                return move
            #  Else
            self._OB_active = False

        # minimax
        return self._start_negamax(3)

    def _get_result(self):
        (nb_whites, nb_blacks) = self._board.get_nb_pieces()
        if nb_whites > nb_blacks:
            return 1000 if self._mycolor == 1 else -1000
        elif nb_blacks > nb_whites:
            return 1000 if self._mycolor == 2 else -1000
        else:
            return 0

    def _start_negamax(self, depth):
        if self._board.is_game_over():
            return None

        maxx = - sys.maxsize - 1
        best_move = None
        for m in self._board.legal_moves():
            self._board.push(m)
            value = -self._negamax(depth - 1, self._opponent, -sys.maxsize - 1, sys.maxsize)
            if value > maxx:
                maxx = value
                best_move = m
            self._board.pop()

        return best_move

    def _negamax(self, depth, player, alpha, beta):
        alpha_origin = alpha
        self._table_usage += 1

        # Transposition table lookup
        current_hash = self._get_board_hash()
        tt_entry = self._hash_table.get_table_entry(current_hash)
        # Check in table whether or not we have to compute the best move
        if tt_entry is not None and tt_entry.depth >= depth:
            if tt_entry.flag == self._hash_table._EXACT:
                return tt_entry.value
            elif tt_entry.flag == self._hash_table._LOWERBOUND:
                alpha = max(alpha, tt_entry.value)
            else:  # tt_entry.flag == self._hash_table._UPPERBOUND:
                beta = min(beta, tt_entry.value)

            if alpha >= beta:
                return tt_entry.value

        self._table_usage -= 1

        # If game is over or depth limit reached
        if depth == 0 or self._board.is_game_over():
            return Evaluator.eval(self._board, self._mycolor) * (-1 if player != self._mycolor else 1)

        color = self._board._flip(player)

        # If player cannot move, opponent turn
        if not self._board.at_least_one_legal_move(player):
            return -self._negamax(depth - 1, color, -beta, -alpha)

        value = - sys.maxsize - 1
        for m in self._board.legal_moves():
            self._board.push(m)
            value = max(value, -self._negamax(depth - 1, color, -beta, -alpha))
            self._board.pop()
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Cutoff

        # Store in transposition table
        tt_entry = TableEntry()
        tt_entry.value = value
        if value <= alpha_origin:
            tt_entry.flag = self._hash_table._UPPERBOUND
        elif value >= beta:
            tt_entry.flag = self._hash_table._LOWERBOUND
        else:
            tt_entry.flag = self._hash_table._EXACT

        tt_entry.depth = depth
        self._hash_table.store(current_hash, tt_entry)

        return value

    def _get_board_hash(self):
        return hash(tuple([tuple(c) for c in self._board._board]))
