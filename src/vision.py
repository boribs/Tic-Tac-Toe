# pyright: strict

from src.commons import *

import numpy as np
import cv2
from cv2.typing import MatLike, Point
import math


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

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((5,5), np.uint8)

        # turn into thresholded binary
        _, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # remove noise from binary
        thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

        t = cv2.bitwise_not(thresh1)
        cv2.imshow('out', t)
        # cv2.waitKey(0)

        contours, _ = cv2.findContours(t, 1, cv2.CHAIN_APPROX_SIMPLE)
        conts = cv2.drawContours(
            np.zeros(img.shape[:2], np.uint8), # pyright: ignore
            contours,
            -1,
            (255,255,255),
            4
        )
        cv2.imshow('out', conts)
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
                        if d < 15: break
                    else:
                        intersections.append(intr)
                        cv2.circle(out, intr, 3, (255,0,255), 3)

        rects = self.__find_rectangles(intersections, 20)

        if not rects:
            return None

        if len(rects) > 1:
            print("Me estoy confundiendo! Pon el tablero sobre una superficie con menos textura")
            return None

        a, b, c, d = rects[0]
        cv2.line(out, a, b, (255, 0, 255), 3)
        cv2.line(out, b, c, (0, 0, 255), 3)
        cv2.line(out, c, d, (0, 0, 255), 3)
        cv2.line(out, d, a, (0, 0, 255), 3)

        cv2.imshow('out', out)
        cv2.waitKey(0)

        for cnt in contours:
            inside = cv2.pointPolygonTest(cnt, a, False)
            if inside >= 0:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(out,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.imshow('out', out)
                cv2.waitKey(0)

                padding = 10
                cropped = cv2.cvtColor(conts.copy()[y-padding:y+h+padding, x-padding:x+w+padding], cv2.COLOR_GRAY2BGR)
                rows, cols, _ = cropped.shape
                rot = math.atan2((a[1] - b[1]), (a[0] - b[0]))

                # puntos relevantes (rectángulo central) a imagen rotada
                center = (cols // 2, rows // 2)
                a = self.__rotate_point((a[0]-x + padding, a[1]-y + padding), center, -rot)
                b = self.__rotate_point((b[0]-x + padding, b[1]-y + padding), center, -rot)
                c = self.__rotate_point((c[0]-x + padding, c[1]-y + padding), center, -rot)
                d = self.__rotate_point((d[0]-x + padding, d[1]-y + padding), center, -rot)

                # rotar imagen para que el tablero quede derecho
                mat = cv2.getRotationMatrix2D(center, rot * 180 / math.pi, 1)
                rotated = cv2.warpAffine(cropped, mat, (cols, rows))

                cv2.circle(rotated, a, 3, (0,0,255), 3)
                cv2.circle(rotated, b, 3, (255,0,255), 3)
                cv2.circle(rotated, c, 3, (0,255,0), 3)
                cv2.circle(rotated, d, 3, (255,0,0), 3)

                cv2.imshow('out', rotated)
                cv2.waitKey(0)

                _ = self.__extract_slots(rotated, b, a, d, c)

                break

    def __rotate_point(self, p: Point, around: Point, angle: float) -> Point:
        """
        Rotates the point `p` around another point `around`.
        """

        x0, y0 = around
        x1, y1 = p

        x2 = ((x1 - x0) * math.cos(angle)) - ((y1 - y0) * math.sin(angle)) + x0;
        y2 = ((x1 - x0) * math.sin(angle)) + ((y1 - y0) * math.cos(angle)) + y0;

        return (int(x2), int(y2))

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

    def __find_rectangles(self, points: list[Point], threshold: float = 0.5) -> list[tuple[Point, Point, Point, Point]]:
        """
        Finds which pairs of points form a rectangle.
        """

        # Para cada par de puntos sacar el punto que es la suma de los dos y la distancia entre estos.
        # Dos parejas de puntos serán los vértices de un rectángulo si sus distancias
        # son iguales y sus sumas son iguales.

        def pdist(a: Point, b: Point) -> float:
            return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

        def similar(a: Point | float, b: Point | float):
            if type(a) != float and type(b) != float:
                return abs(a[0] - b[0]) < threshold and abs(a[1] - b[1]) < threshold # pyright: ignore
            else:
                return abs(a - b) < threshold # pyright: ignore

        line_sum: dict[Point, Point] = {}
        line_dist: dict[Point, float] = {}
        lines: list[Point] = []
        out: list[tuple[Point, Point, Point, Point]] = []

        for i in range(len(points)):
            a = points[i]
            for j in range(i + 1, len(points)):
                b = points[j]
                line_sum[(i, j)] = (a[0] + b[0], a[1] + b[1])
                line_dist[(i, j)] = pdist(a, b)
                lines.append((i, j))

        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                a = lines[i]
                b = lines[j]

                if similar(line_dist[a], line_dist[b]) and \
                    similar(line_sum[a], line_sum[b]):
                    out.append((points[a[0]], points[b[0]], points[a[1]], points[b[1]]))

        return out

    def __extract_slots(self, rotated: MatLike, a: Point, b: Point, c: Point, d: Point, padding: int = 2) -> BoardLike:
        """
        Extracts the different slot images and analyzes them.
        """

        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = d

        slot_images = [
            rotated[padding:ay-padding, padding:ax-padding],       # 0
            rotated[padding:by-padding, ax+padding:bx-padding],    # 1
            rotated[padding:by-padding, bx+padding:-padding],      # 2
            rotated[ay+padding:dy-padding, padding:dx-padding],    # 3
            rotated[ay+padding:cy-padding, ax+padding:cx-padding], # 4
            rotated[ay+padding:cy-padding, cx+padding:-padding],   # 5
            rotated[dy+padding:, padding:dx-padding],              # 6
            rotated[dy+padding:, dx+padding:cx-padding],           # 7
            rotated[dy+padding:, cx+padding:-padding],             # 8
        ]


        kernel = np.ones((3, 3), np.uint8)
        for i in range(len(slot_images)):
            erosion = cv2.erode(slot_images[i],kernel,iterations = 1)
            print(i, self.__detect_slot(erosion))
            cv2.imshow(f"{i}", erosion)
        cv2.waitKey(0)

        slots: BoardLike = []
        return slots


    def __detect_slot(self, slot: MatLike) -> BoardSlot:
        """
        Returns the shape within the slot. To be used within self.detect_board().
        """
        def findCircle(image: MatLike):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            circles = cv2.HoughCircles(
                gray,
                cv2.HOUGH_GRADIENT,
                dp=1.2,
                minDist=20,
                param1=50,
                param2=30,
                minRadius=3,
                maxRadius=50
                )

            if circles is not None: # pyright: ignore
                return True
            else:
                return False

        def findCross(image: MatLike):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)

            lines = cv2.HoughLinesP(
                edges,
                rho=1,
                theta=np.pi / 180,
                threshold=10,
                minLineLength=10,
                maxLineGap=20
            )

            if lines is None or len(lines) < 2: #pyright: ignore
                return False

            def ccw(A: tuple[int, int], B: tuple[int, int], C: tuple[int, int]):
                return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

            def lines_intersect(l1: list[int], l2: list[int]):
                A = (l1[0], l1[1])
                B = (l1[2], l1[3])
                C = (l2[0], l2[1])
                D = (l2[2], l2[3])
                return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

            for i in range(len(lines)):
                for j in range(i + 1, len(lines)):
                    line1 = lines[i][0]
                    line2 = lines[j][0]

                    if lines_intersect(line1, line2):
                        return True

            return False

        if findCircle(slot):
            return BoardSlot.Circle
        elif findCross(slot):
            return BoardSlot.Cross
        else:
            return BoardSlot.Empty
