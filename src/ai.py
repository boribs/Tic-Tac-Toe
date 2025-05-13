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

    def next_move(self, board: BoardLike) -> tuple[int, BoardSlot]:
        """
        Selects the next move based on a current position.
        """

        raise Exception('Not implemented')

    def check_win(self, board: BoardLike) -> bool:
        """
        Checks for win condition: 3 in a row.
        """

        raise Exception('Not implemented')

    def main(self):
        """
        Program's main loop.
        """

        detector = BoardDetector()

        while True:
            ok, frame = detector.cam.read()
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

            #         self.previous_board = board

            #     if self.show_detections:
            #         detector.show_detected(highlight)

            # # alguien ya ganó
            # if self.check_win(self.previous_board):
            #     # mostrar quién ganó (en la misma ventana)
            #     # esperar a que presione alguna tecla para salir
            #     break
