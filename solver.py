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

v_array = np.copy(array)

def identify_num(board):
    # finds the coordinates of all the nums
    num = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                num.append((int(board[i][j]),i, j))
    return num

def identify_domains(board,numbers):
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
    for i in range(len(numbers)):
        domains.append([(numbers[i][1],numbers[i][2]),(int(board[numbers[i][1]][numbers[i][2]]),check_surrounding(board,numbers[i][1],numbers[i][2]))])
    return domains

def mine_location(board,coordinates):
    for diffx in [-1,0,1]:
        for diffy in [-1,0,1]:
            newx, newy = coordinates[0]+diffx, coordinates[1]+diffy
            if 0<= newx < len(board) and 0 <= newy < len(board[0]) and board[newx][newy] == -1:
                board[newx][newy] = 10
def guaranteed_mines(board,domain):
    print(domain)
    for i in range(len(domain)):
        if domain[i][1][0] == domain[i][1][1]:
            print("Mine")
            mine_location(board,domain[i][0])

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
            elif cell == 10:
                print(colorama.Back.WHITE + colorama.Fore.RED + "M", end = " ")
        print(colorama.Style.RESET_ALL, end="\n")


visualise_board(array)

guaranteed_mines(array,identify_domains(array,identify_num(array)))

visualise_board(array)