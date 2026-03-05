import numpy as np
import colorama 
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
            if board[i][j] > 0:
                num.append((i, j))
    return num

numbers = identify_num(array)


def identify_domains(board,numbers):
    domains = {}
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
    for i in range(len(numbers)):
        domains.update

        

    

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
        print(colorama.Style.RESET_ALL, end="\n")


visualise_board(array)

