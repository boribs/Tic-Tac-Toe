test_board = [
    ['X','O','X'],
    ['O','X','O'],
    ['O','X','X']
    ]


jugador = None
def checkBoard(board):
    def checkRows(board):
        global jugador
        for row in board:
            win_check = True
            item = row[0]
            for element in row:
                if item != element:
                    win_check = False
            if win_check == True:
                jugador=item
                return win_check
        return win_check

    def checkColumns(board):
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

    def checkDiag(board):
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
    
    return win_check

if checkBoard(test_board):
    print(f"gana {jugador}")
else:
    print("nadie gano")

# board = [['' for x in range(3)] for y in range(3)] # x = width, y = height

# player_one = 'X'
# player_two = 'O' 

# dicc = {
#     '9' : (1,3),
#     '8' : (1,2),
#     '7' : (1,1),
#     '6' : (2,3),
#     '5' : (2,2),
#     '4' : (2.1),
#     '3' : (3,3),
#     '2' : (3,2),
#     '1' : (3,1)
# }
# ans = None

# while ans != 'X' or ans != 'O':
#     ans = input("Quién empieza? X ó O").capitalize()
#     if  ans == 'X':
#         turn = 1
#     elif ans == 'O':
#         turn = 0

# for i in board:
#     if turn == 1:
#         opt = input("Elige donde poner un 'O'")
#         board[dicc[opt]] = 'O'
#         turn = 0
#         checkBoard(board)
        
#     if turn == 0:
#         opt = input("Elige donde poner un 'X'")
#         board[dicc[opt]] = 'X'
#         turn = 1
#         checkBoard(board)
