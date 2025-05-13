# pyright: strict

import cv2
from src.commons import *
from src.vision import BoardDetector

class TicTacToeAI:
    """
    The decision making of the AI. Also has the main loop.
    """

    def __init__(self, show_detections: bool = True):
        self.previous_board = [BoardSlot.Empty for _ in range(9)]
        self.show_detections = show_detections
        self.jugador = None

    def next_move(self, board: BoardLike) -> tuple[int, BoardSlot]:
        """
        Selects the next move based on a current position.
        """

        raise Exception('Not implemented')

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

            print(detector.detect_board(frame))

            # if board is None:
            #     continue

            # cv2.imshow('board', board)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

            # if board:
            #     highlight = None
            #     if board != self.previous_board:
            #         next_move = self.next_move(board)

            #         # update board state
            #         i, slot = next_move
            #         board[i] = slot
            #         highlight = next_move

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
