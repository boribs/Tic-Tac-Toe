# pyright: strict

from src.commons import *

import numpy as np
import cv2
from cv2.typing import MatLike


class BoardDetector:
    """
    Tools for detecting the board and the shapes on each slot.
    """

    def __init__(self, cam_id: int = 0):
        self.detected_lines = []
        # self.cam = cv2.VideoCapture(cam_id)

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

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5,5), np.uint8)

        # turn into thresholded binary
        _, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # remove noise from binary
        thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

        t = cv2.bitwise_not(thresh1)
        cv2.imshow('asdf', t)
        # cv2.waitKey(0)

        contours, _ = cv2.findContours(t, 1, cv2.CHAIN_APPROX_SIMPLE)
        conts = cv2.drawContours(np.zeros(img.shape[:2], np.uint8), contours, -1, (255,255,255), 4)
        cv2.imshow('asdf', conts)
        cv2.waitKey(0)

        lines = cv2.HoughLinesP(
            conts,
            1.2,
            np.pi / 180,
            90,
            minLineLength=25,
            maxLineGap=0,
        )

        intersections: list[Point] = []
        out = cv2.cvtColor(conts.copy(), cv2.COLOR_GRAY2BGR)

        def dist_points(a: Point, b: Point):
            return (abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2)**0.5


        i = True
        for line in lines:
            x1, y1, x2, y2 = line[0] # pyright: ignore
            cv2.line(out, (x1, y1), (x2, y2), (0,255,0) if i else (255,0,0), 1) # pyright: ignore
            i = not i

        cv2.imshow('out', out)
        cv2.waitKey(0)

        for i, line in enumerate(lines):
            for j, line2 in enumerate(lines):

                if i == j: continue
                intr = self.__compute_intersection(line[0], line2[0])

                if intr:
                    for point in intersections:
                        d = dist_points(intr, point)
                        print(d, point, intr)
                        if d < 15: break
                    else:
                        print('a')
                        intersections.append(intr)
                        cv2.circle(out, intr, 3, (255,0,255), 3)

        print(len(intersections))

        cv2.imshow('out', out)
        cv2.waitKey(0)

    def __compute_intersection(self, line1: MatLike, line2: MatLike):
        """
        Compute the intersection point of segments p1-p2 and p3-p4.
        """

        p1, p2 = line1[:2], line1[2:]
        p3, p4 = line2[:2], line2[2:]

        def det(a: tuple[int, int], b: tuple[int, int]):
            return a[0]*b[1] - a[1]*b[0]

        xdiff = (p1[0] - p2[0], p3[0] - p4[0])
        ydiff = (p1[1] - p2[1], p3[1] - p4[1])

        div = det(xdiff, ydiff)
        if div == 0:
            return None  # Lines are parallel or coincident

        d = (det(p1, p2), det(p3, p4)) # pyright: ignore
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        # Check if the intersection point (x, y) is within both segments
        if (
            min(p1[0]-3, p2[0]-3) <= x <= max(p1[0]+3, p2[0]+3) and
            min(p1[1]-3, p2[1]-3) <= y <= max(p1[1]+3, p2[1]+3) and
            min(p3[0]-3, p4[0]-3) <= x <= max(p3[0]+3, p4[0]+3) and
            min(p3[1]-3, p4[1]-3) <= y <= max(p3[1]+3, p4[1]+3)
        ):
            return (int(x), int(y))
        else:
            return None  # Intersection point not within both segments


    def __detect_slot(self, slot: MatLike) -> BoardSlot:
        """
        Returns the shape within the slot. To be used within self.detect_board().
        """

        # detecta qué hay en cada espacio
        # `slot` es el recorte de la imagen original que
        # solo contiene un espacio del tablero

        raise Exception('Not implemented')
