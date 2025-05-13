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
        self.ai_player = BoardSlot.Cross 
        self.human_player = BoardSlot.Circle 

    def get_empty_slots(self, board: BoardLike) -> list[int]: # <--- Método añadido
        """
        Devuelve una lista con los índices de las casillas vacías.
        """
        return [i for i, slot in enumerate(board) if slot == BoardSlot.Empty]

    def next_move(self, board: BoardLike) -> Optional[Tuple[int, BoardSlot]]:
        """
        Selecciona el próximo movimiento para la IA basado en reglas heurísticas.
        Prioridades: Ganar > Bloquear > Centro > Esquina Opuesta > Esquina > Lado.

        Args:
            board (BoardLike): El estado actual del tablero.

        Returns:
            tuple[int, BoardSlot] | None: Tupla con (índice de casilla, símbolo de IA) o None si no hay jugada.
        """

        empty_slots = self.get_empty_slots(board) # Obtiene lista de casillas vacías

        if not empty_slots: # Si no hay casillas vacías
            return None     # No se puede mover

        # 1. Comprobar si la IA puede ganar en el próximo movimiento
        for i in empty_slots:
            board_copy = board.copy() # Crear una copia para simular
            board_copy[i] = self.ai_player # Simula el movimiento de la IA
            # Cambiado check_winner a check_win para coincidir con el método existente
            if self.check_win(board_copy) == self.ai_player: # Si este movimiento gana
                print(f"IA: Jugando para ganar en {i}") # Mensaje de depuración/log
                return (i, self.ai_player) # Devuelve este movimiento ganador

        # 2. Comprobar si el humano puede ganar en el próximo movimiento y bloquearlo
        for i in empty_slots:
            board_copy = board.copy() # Crear una copia para simular
            board_copy[i] = self.human_player # Simula el movimiento del humano
            # Cambiado check_winner a check_win para coincidir con el método existente
            if self.check_win(board_copy) == self.human_player: # Si el humano ganaría con este movimiento
                print(f"IA: Bloqueando al humano en {i}") # Mensaje de depuración/log
                return (i, self.ai_player) # La IA juega aquí para bloquear

        # 3. Intentar tomar el centro (casilla 4) si está libre
        if 4 in empty_slots:
            print("IA: Jugando en el centro (4)") # Mensaje de depuración/log
            return (4, self.ai_player)

        # 4. Intentar tomar una esquina opuesta a la del oponente
        corners = [0, 2, 6, 8]
        opposite_corners = {0: 8, 8: 0, 2: 6, 6: 2}
        for corner in corners:
            # Si el humano está en una esquina 'corner' y la opuesta 'opposite' está vacía
            if board[corner] == self.human_player and opposite_corners[corner] in empty_slots:
                move = opposite_corners[corner]
                print(f"IA: Jugando esquina opuesta ({move}) a la del humano ({corner})")
                return (move, self.ai_player)

        # 5. Intentar tomar una esquina vacía cualquiera
        empty_corners = [i for i in corners if i in empty_slots]
        if empty_corners: # Si hay esquinas vacías
            move = random.choice(empty_corners) # Elige una esquina vacía al azar (o la primera)
            print(f"IA: Jugando en esquina vacía ({move})")
            return (move, self.ai_player)

        # 6. Intentar tomar un lado vacío cualquiera
        sides = [1, 3, 5, 7]
        empty_sides = [i for i in sides if i in empty_slots]
        if empty_sides: # Si hay lados vacíos
            move = random.choice(empty_sides) # Elige un lado vacío al azar (o el primero)
            print(f"IA: Jugando en lado vacío ({move})")
            return (move, self.ai_player)

        # Fallback: Si por alguna razón no se cumplió ninguna regla anterior
        if empty_slots:
             print(f"IA: Jugando en la primera casilla vacía disponible ({empty_slots[0]}) (Fallback)")
             return (empty_slots[0], self.ai_player)

        return None # Seguridad, aunque no debería llegar aquí si empty_slots fue verificado

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
