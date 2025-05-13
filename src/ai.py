# pyright: strict

import cv2
from src.commons import *
from src.vision import BoardDetector
from typing import Optional, Tuple # <--- Añadido
import random
from collections import Counter

img_count = 0

class TicTacToeAI:
    """
    The decision making of the AI. Also has the main loop.
    """

    def __init__(self, show_detections: bool = True):
        self.previous_board = [BoardSlot.Empty for _ in range(9)]
        self.show_detections = show_detections
        self.ai_player = BoardSlot.Circle
        self.human_player = BoardSlot.Cross

    def get_empty_slots(self, board: BoardLike) -> list[int]: # <--- Método añadido
        """
        Devuelve una lista con los índices de las casillas vacías.
        """
        return [i for i, slot in enumerate(board) if slot == BoardSlot.Empty]

    def next_move(self, board: BoardLike) -> tuple[int, BoardSlot]:
        """
        Selects the next move based on a current position.
        """
        empty_indices = [i for i, slot in enumerate(board) if slot == BoardSlot.Empty]

        if not empty_indices:
            pass

        i = random.choice(empty_indices)
        return (i, BoardSlot.Circle)

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

        global img_count

        detector = BoardDetector()

        while True:
            ok, frame = detector.cam.read() # pyright: ignore
            if not ok:
                print('Error reading')
                return

            board = detector.detect_board(frame)

            if board is None:
                continue

            display, points, board = board

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

            current_counts = Counter(board)
            previous_counts = Counter(self.previous_board)

            opponent_moved = current_counts[BoardSlot.Cross] != previous_counts[BoardSlot.Cross]
            ai_moved = current_counts[BoardSlot.Circle] != previous_counts[BoardSlot.Circle]

            if board:
                highlight = None
                if opponent_moved and BoardSlot.Empty in board:
                    next_move = self.next_move(board)
                    print(next_move)
                    # update board state
                    i, slot = next_move
                    # board[i] = slot
                    highlight = next_move

                    detector.draw_highlight(points, slot, i, display)
                    cv2.imshow('out', display)
                    cv2.imwrite(f'captura_{img_count}.jpg', display)
                    img_count += 1
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
