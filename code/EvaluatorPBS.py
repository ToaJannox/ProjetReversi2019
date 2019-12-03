# -*- coding: utf-8 -*-

from enum import Enum
import Reversi

# mobility = nb of move available
#

class GamePhase(Enum):
    EARLY_GAME = 0
    MID_GAME = 1
    LATE_GAME = 2

# Thanks to:
# Parth Parekh
# Urjit Singh Bhatia
# Kushal Sukthankar
class EvaluatorPBS: 

    positionnalMap = [[100,-20,10, 5, 5, 5, 5,10,-20,100],
                      [-20,-50,-2,-2,-2,-2,-2,-2,-50,-20],
                      [ 10, -2,-1,-1,-1,-1,-1,-1, -2, 10],
                      [  5, -2,-1,-1,-1,-1,-1,-1, -2,  5],
                      [  5, -2,-1,-1,-1,-1,-1,-1, -2,  5],
                      [  5, -2,-1,-1,-1,-1,-1,-1, -2,  5],
                      [  5, -2,-1,-1,-1,-1,-1,-1, -2,  5],
                      [ 10, -2,-1,-1,-1,-1,-1,-1, -2, 10],
                      [-20,-50,-2,-2,-2,-2,-2,-2,-50,-20],
                      [100,-20,10, 5, 5, 5, 5,10,-20,100]
                        ]
    @staticmethod
    def _get_game_phase(board):
        (c1, c2) = board.get_nb_pieces()
        nb_pieces = c1 + c2
        if nb_pieces < 33:
            return GamePhase.EARLY_GAME
        elif nb_pieces <= 66:
            return GamePhase.MID_GAME
        else:
            return GamePhase.LATE_GAME

    @staticmethod
    def eval(board, player):
        # if finished: 1000 discDiff
        # else:
        #   if EARLY:  1000*eval_corner + 50*eval_mobility
        #   elif MID:  1000*eval_corner + 20*eval_mobility + 10*eval_disc_diff + 100*eval_parity
        #   elif LATE: 1000*eval_corner + 100*eval_mobility + 500*eval_disc_diff + 500*eval_parity

        if board.is_game_over():
            return 1000 * EvaluatorPBS._eval_disc_diff(board, player)

        game_phase = EvaluatorPBS._get_game_phase(board)

        if game_phase == GamePhase.EARLY_GAME:
            return 1000 * EvaluatorPBS._eval_corner(board, player) + 50 * EvaluatorPBS._eval_mobility(board, player)
        elif game_phase == GamePhase.MID_GAME:
            return 1000 * EvaluatorPBS._eval_corner(board, player) + 20 * EvaluatorPBS._eval_mobility(board, player) + 10\
                   * EvaluatorPBS._eval_disc_diff(board, player) + 100 * EvaluatorPBS._eval_parity(board)
        else:  # game_phase == GamePhase.LATE_GAME:
            return 1000 * EvaluatorPBS._eval_corner(board, player) + 100 * EvaluatorPBS._eval_mobility(board, player) + 500\
                   * EvaluatorPBS._eval_disc_diff(board, player) + 500 * EvaluatorPBS._eval_parity(board)

    @staticmethod
    def _eval_corner(board, player):
        opponent = board._flip(player)

        cpt_player = 0
        cpt_opponent = 0

        # Player
        if board._board[0][0] == player:
            cpt_player += 1
        if board._board[0][board.get_board_size()-1] == player:
            cpt_player += 1
        if board._board[board.get_board_size()-1][0] == player:
            cpt_player += 1
        if board._board[board.get_board_size()-1][board.get_board_size()-1] == player:
            cpt_player += 1

        # Opponent
        if board._board[0][0] == opponent:
            cpt_opponent += 1
        if board._board[0][board.get_board_size()-1] == opponent:
            cpt_opponent += 1
        if board._board[board.get_board_size()-1][0] == opponent:
            cpt_opponent += 1
        if board._board[board.get_board_size()-1][board.get_board_size()-1] == opponent:
            cpt_opponent += 1

        return 100 * (cpt_player - cpt_opponent) / (cpt_player + cpt_opponent + 1)

    @staticmethod
    def _eval_mobility(board, player):
        opponent = board._flip(player)

        cpt_player = 0
        cpt_opponent = 0
        for x in range(0, board.get_board_size()):
            for y in range(0, board.get_board_size()):
                if board.lazyTest_ValidMove(player, x, y):
                    cpt_player += 1
                if board.lazyTest_ValidMove(opponent, x, y):
                    cpt_opponent += 1

        return 100 * (cpt_player - cpt_opponent) / (cpt_player + cpt_opponent + 1)

    @staticmethod
    def _eval_disc_diff(board, player):
        (whites, blacks) = board.get_nb_pieces()
        if player == board._BLACK:
            return 100 * (blacks - whites) / (blacks + whites)
        else:
            return 100 * (whites - blacks) / (whites + blacks)

    @staticmethod
    def _eval_parity(board):
        (c1, c2) = board.get_nb_pieces()
        nb_pieces = c1 + c2
        size = board.get_board_size()
        rem_discs = (size * size) - nb_pieces
        return -1 if rem_discs % 2 == 0 else 1
