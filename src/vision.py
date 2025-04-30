# pyright: strict

from src.commons import *

import cv2
from cv2.typing import MatLike


class BoardDetector:
    """
    Tools for detecting the board and the shapes on each slot.
    """

    def __init__(self, cam_id: int = 0):
        self.detected_lines = []
        self.cam = cv2.VideoCapture(cam_id)

    def show_detected(self, highlight: tuple[int, BoardSlot] | None):
        """
        Displays detected lines and slots.
        Displays in another color a highlight.
        """

        # el highlight es el movimiento que escoge la computadora
        # dibuja líneas de algún color sobre el tablero y sobre las figuras detectadas
        raise Exception('Not implemented')


    def detect_board(self, img: MatLike) -> BoardLike | None:
        """
        Finds a board in an image. Updates self.detected_lines and
        returns new filled BoardLike.
        """

        # detecta el tablero y las figuras en él
        # la idea es que se haga un recorte de los rectángulos y se pasen a
        # __detect_slot() para que reconozca qué figura es

        raise Exception('Not implemented')

    def __detect_slot(self, slot: MatLike) -> BoardSlot:
        """
        Returns the shape within the slot. To be used within self.detect_board().
        """

        # detecta qué hay en cada espacio
        # `slot` es el recorte de la imagen original que
        # solo contiene un espacio del tablero

        raise Exception('Not implemented')
