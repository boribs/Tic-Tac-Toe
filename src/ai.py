# pyright: strict

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

    def check_win(self, board: BoardLike) -> bool:
        """
        Checks for win condition: 3 in a row.
        """
        win_tuples = [(0,1,2),
                      (3,4,5),
                      (6,7,8),
                      (0,3,6),
                      (1,4,7),
                      (2,5,8),
                      (0,4,8),
                      (2,4,6),
                      ]
        
        def checkRows(board:BoardLike):
            global jugador
                for element in board:
                    
                    if item != element:
                        win_check = False
                if win_check == True:
                    jugador=item
                    return win_check
            return win_check

        def checkColumns(board:BoardLike):
            global jugador
            for column in range(0,3):
                element = board[0][column]
                win_check = True
                for row in range(1,3):
                    item = board[row][column]
                    if item != element:
                        win_check = False
                if win_check == True:
                    jugador=item
                    return win_check
            return win_check

        def checkDiag(board:BoardLike):
            global jugador
            element = board[0][0]
            win_check = True
            for i in range(3):
                item = board[i][i]
                if item != element:
                    win_check = False
            if win_check == True:
                jugador=item
                return win_check
            
            win_check = True
            element = board[0][2]
            for j in range(3):
                item = board[j][3-j-1]
                if item != element:
                    win_check = False
            if win_check == True:
                jugador=item
                return win_check
            return win_check
        win_check = checkColumns(board)
        win_check = win_check ^ checkRows(board)
        win_check = win_check ^ checkDiag(board)

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

            board = detector.detect_board(frame)

            if board:
                highlight = None
                if board != self.previous_board:
                    next_move = self.next_move(board)

                    # update board state
                    i, slot = next_move
                    board[i] = slot
                    highlight = next_move

                    self.previous_board = board

                if self.show_detections:
                    detector.show_detected(highlight)

            # alguien ya ganó
            if self.check_win(self.previous_board):
                # mostrar quién ganó (en la misma ventana)
                # esperar a que presione alguna tecla para salir
                break
