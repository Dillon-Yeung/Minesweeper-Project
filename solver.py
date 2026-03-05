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
    num = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                num.append((i, j))
    return num

numbers = identify_num(array)

def identify_domains(board,numbers):
    domains = {}
    

def visualise_board(board):
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

