# pyright: strict

import cv2
from src.commons import *
from src.vision import BoardDetector
from typing import Optional, Tuple # <--- Añadido
import random

class TicTacToeAI:
    """
    The decision making of the AI. Also has the main loop.
    """

    def __init__(self, show_detections: bool = True):
        self.previous_board = [BoardSlot.Empty for _ in range(9)]
        self.show_detections = show_detections

    def next_move(self, board: BoardLike) -> tuple[int, BoardSlot]:
        """
        Selects the next move based on a current position.
        """
        empty_indices = [i for i, slot in enumerate(board) if slot == BoardSlot.Empty]

        if not empty_indices:
            pass

        i = random.choice(empty_indices)
        return (i, BoardSlot.Circle)
        # raise Exception('Not implemented')

    def check_win(self, board: BoardLike) -> BoardSlot:
        """
        Checks for win condition: 3 in a row.
        """
        
        win_tuples = [(0,1,2), # filas
                      (3,4,5),
                      (6,7,8),
                      (0,3,6),# columnas
                      (1,4,7),
                      (2,5,8),
                      (0,4,8),# diagonales
                      (2,4,6),
                      ]

       
        for a,b,c in win_tuples:
            print(a)
            if board[a] == board[b] == board[c] and board[a] != BoardSlot.Empty:
                return board[a]
        if BoardSlot.Empty not in board:
            return BoardSlot.Tie
        else:
            return BoardSlot.Empty
           

    def main(self):
        """
        Program's main loop.
        """

        detector = BoardDetector()

        while True:
            ok, frame = detector.cam.read() # pyright: ignore
            if not ok:
                print('Error reading')
                return

            board = detector.detect_board(frame)

            if board is None:
                continue

            # cv2.imshow('board', board)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            
            # alguien ya ganó
            if self.check_win(self.previous_board) == BoardSlot.Circle:
                print(f"Ganó: O")
                break
            elif self.check_win(self.previous_board) == BoardSlot.Cross:
                print(f"Ganó X")
                break
            elif self.check_win(self.previous_board) == BoardSlot.Tie:
                print("Empate")
                break
            else: 
                pass

            if board:
                highlight = None
                if board != self.previous_board and BoardSlot.Empty in board:
                    next_move = self.next_move(board)
                    print(next_move)
                    # update board state
                    i, slot = next_move
                    board[i] = slot
                    highlight = next_move
                
                self.previous_board = board.copy()


            # alguien ya ganó
            if self.check_win(self.previous_board) == BoardSlot.Circle:
                print(f"Ganó: O")
                break
            elif self.check_win(self.previous_board) == BoardSlot.Cross:
                print(f"Ganó X")
                break
            elif self.check_win(self.previous_board) == BoardSlot.Tie:
                print("Empate")
                break
            else: 
                pass
