import numpy as np
import colorama 
import collections
import math

#array = np.zeros((16,16),dtype=int)
array = np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,1,1,1,1,1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,1,0,0,0,1,1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,1,0,1,1,1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,1,0,1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,1,1,2,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]])

def identify_num(board):
    # finds the coordinates of all the nums
    num = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0 and board[i][j] < 9:
                num.append((int(board[i][j]),i, j))
    return num

def identify_domains(board,vboard,numbers):
    domains = []
    def check_surrounding(board,x,y):
        count = 0
        rows = len(board)
        cols = len(board[0])
        for diffx in [-1,0,1]:
            for diffy in [-1,0,1]:
                if diffx == 0 and diffy == 0:
                    continue
                newx, newy = x+diffx, y+diffy
                if 0 <= newx < rows and 0 <= newy < cols and board[newx][newy] == -1:
                    count += 1
        return count
    def mine_count(board,vboard,x,y):
        count = vboard[x][y]
        for diffx in [-1, 0, 1]:
            for diffy in [-1, 0, 1]:
                if diffx == 0 and diffy == 0:
                    continue
                newx, newy = x + diffx, y + diffy
                if 0 <= newx < len(board) and 0 <= newy < len(board[0]) and board[newx][newy] == 10:
                    count -= 1
        return count
    for i in range(len(numbers)):
        x, y = numbers[i][1], numbers[i][2]
        adj_count = int(mine_count(board, vboard, x, y))
        uncovered = check_surrounding(board, x, y)
        domains.append([(x, y), (adj_count, uncovered)])
    return domains

def mine_location(board,coordinates):
    change = False
    for diffx in [-1,0,1]:
        for diffy in [-1,0,1]:
            newx, newy = coordinates[0]+diffx, coordinates[1]+diffy
            if 0<= newx < len(board) and 0 <= newy < len(board[0]) and board[newx][newy] == -1:
                board[newx][newy] = 10
                change = True
    return change

def safe_location(board,coordinates):
    change = False
    for diffx in [-1,0,1]:
        for diffy in [-1,0,1]:
            newx, newy = coordinates[0]+diffx, coordinates[1]+diffy
            if 0<= newx < len(board) and 0 <= newy < len(board[0]) and board[newx][newy] == -1:
                board[newx][newy] = 9
                change = True
    return change

def guaranteed_spaces(board,domain):
    changes = False
    for i in range(len(domain)):
        if domain[i][1][0] == domain[i][1][1]:
            changes = changes or mine_location(board,domain[i][0])
        elif domain[i][1][0] == 0:
            changes = changes or safe_location(board,domain[i][0])
    return changes

def visualise_board(board):
    # for testing only, will be altered later when GUI introduced
    for row in board:
        for cell in row:
            if cell == -1:
                print(colorama.Back.BLACK + " ", end=" ")
            elif cell == 0:
                print(colorama.Back.WHITE + " ", end=" ")
            elif cell == 1:
                print(colorama.Back.WHITE + colorama.Fore.BLUE + "1", end=" ")
            elif cell == 2:
                print(colorama.Back.WHITE + colorama.Fore.GREEN + "2", end=" ")
            elif cell == 3:
                print(colorama.Back.WHITE + colorama.Fore.RED + "3", end=" ")
            elif cell == 4:
                print(colorama.Back.WHITE + colorama.Fore.CYAN + "4", end=" ")
            elif cell == 5:
                print(colorama.Back.WHITE + colorama.Fore.MAGENTA + "5", end=" ")
            elif cell == 6:
                print(colorama.Back.WHITE + colorama.Fore.YELLOW + "6", end=" ")
            elif cell == 9:
                print(colorama.Back.WHITE + colorama.Fore.BLACK + "S", end = " ")
            elif cell == 10:
                print(colorama.Back.WHITE + colorama.Fore.RED + "M", end = " ")
        print(colorama.Style.RESET_ALL, end="\n")

def one_step_solve(board):
    v_board = np.copy(board)
    changed = True
    while changed is True:
        domains = identify_domains(board, v_board, identify_num(board))
        changed = guaranteed_spaces(board,domains)
    visualise_board(board)
    print(f"{collections.Counter(board.flatten())[10] - collections.Counter(v_board.flatten())[10]} total mines identified")
    print(f"{collections.Counter(board.flatten())[9] - collections.Counter(v_board.flatten())[9]} total safe spaces identified")
    print(f"{collections.Counter(v_board.flatten())[-1] - collections.Counter(board.flatten())[-1]} total cells identified")
    return board


#figure out how to identify for prob calc
#figure out how to calc without taking too long


