import src.ai
from src.vision import *

if __name__ == '__main__':
    ttt = src.ai.TicTacToeAI()
    ttt.main()

    # images = {
    #     'a': cv2.imread('a.jpeg'),
    #     'b': cv2.imread('b.jpg'),
    # }

    # detector = BoardDetector()
    # img = images['b'].copy()

    # print(detector.detect_board(img))
