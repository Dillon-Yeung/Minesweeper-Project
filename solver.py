import numpy as np
import colorama
import collections
from data_training import *
from screenshotter import take_screen
DEFAULT_TRAINING_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "knn_training_data.npz"
)


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


class board():
    def __init__(self, board):
        self.__board = board
        self.vboard = board.copy()
        self.rows = len(board)
        self.cols = len(board[0])
   
    def __identify_num(self):
        # finds the coordinates of all the nums
        num = []
        for i in range(len(self.vboard)):
            for j in range(len(self.vboard[i])):
                if self.vboard[i][j] > 0 and self.vboard[i][j] < 9:
                    num.append((int(self.vboard[i][j]),i, j))
        return num
   
    def __identify_domains(self,numbers):
        domains = []
       
        def __check_surrounding(x,y):
            #identifies domain size for each number
            count = 0
            for diffx in [-1,0,1]:
                for diffy in [-1,0,1]:
                    if diffx == 0 and diffy == 0:
                        continue
                    newx, newy = x+diffx, y+diffy
                    if 0 <= newx < self.rows and 0 <= newy < self.cols and self.__board[newx][newy] == -1:
                        count += 1
            return count
       
        def __mine_count(x,y):
            #if mine is present decreases domain size
            count = self.__board[x][y]
            for diffx in [-1, 0, 1]:
                for diffy in [-1, 0, 1]:
                    if diffx == 0 and diffy == 0:
                        continue
                    newx, newy = x + diffx, y + diffy
                    if 0 <= newx < len(self.__board) and 0 <= newy < len(self.__board[0]) and self.__board[newx][newy] == 10:
                        count -= 1
            return count
       
        for i in range(len(numbers)):
            #iterates for all and groups results
            x, y = numbers[i][1], numbers[i][2]
            adj_count = int(__mine_count(x, y))
            covered = __check_surrounding(x, y)
            domains.append([(x, y), (adj_count, covered)])
        return domains
   
    def __mine_location(self,x,y):
        #if number == domain size, identifies as mine
        change = False
        for diffx in [-1,0,1]:
            for diffy in [-1,0,1]:
                newx, newy = x+diffx, y+diffy
                if 0<= newx < len(self.__board) and 0 <= newy < len(self.__board[0]) and self.__board[newx][newy] == -1:
                    self.__board[newx][newy] = 10
                    change = True
        return change


    def __safe_location(self,x,y):
        #if mine count == number and domain size != mine count, identifies rest as safe
        change = False
        for diffx in [-1,0,1]:
            for diffy in [-1,0,1]:
                newx, newy = x+diffx, y+diffy
                if 0<= newx < self.rows and 0 <= newy < self.cols and self.__board[newx][newy] == -1:
                    self.__board[newx][newy] = 9
                    change = True
        return change


    def __guaranteed_spaces(self,domain):
        #identifies mines and safes
        changes = False
        for i in range(len(domain)):
            if domain[i][1][0] == domain[i][1][1]:
                changes = changes or self.__mine_location(*domain[i][0])
            elif domain[i][1][0] == 0:
                changes = changes or self.__safe_location(*domain[i][0])
        return changes
   
    def one_step_solve(self):
        changed = True
        while changed is True:
            domains = self.__identify_domains(self.__identify_num())
            changed = self.__guaranteed_spaces(domains)
        self.visualise_board()
        print(f"{collections.Counter(self.__board.flatten())[10] - collections.Counter(self.vboard.flatten())[10]} total mines identified")
        print(f"{collections.Counter(self.__board.flatten())[9] - collections.Counter(self.vboard.flatten())[9]} total safe spaces identified")
        print(f"{collections.Counter(self.vboard.flatten())[-1] - collections.Counter(self.__board.flatten())[-1]} total cells identified")
        return self.__board
   
    def visualise_board(self):
        # for testing only, will be altered later when GUI introduced
        for row in self.__board:
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
                elif cell == 7:
                    print(colorama.Back.WHITE + colorama.Fore.BLACK + "7", end=" ")
                elif cell == 8:
                    print(colorama.Back.WHITE + colorama.Fore.BLACK + "8", end=" ")
                elif cell == 9:
                    print(colorama.Back.WHITE + colorama.Fore.BLACK + "S", end = " ")
                elif cell == 10:
                    print(colorama.Back.WHITE + colorama.Fore.RED + "F", end = " ")
            print(colorama.Style.RESET_ALL, end="\n")


#figure out how to identify for prob calc


if __name__ == "__main__":
    _base = os.path.dirname(os.path.abspath(__file__))


    try:
        compare_dir = os.path.join(_base, 'compare')
        screenshots_dir = os.path.join(_base, 'screenshots')


        if not os.path.isdir(compare_dir):
            raise FileNotFoundError(f"Missing templates directory: {compare_dir}")
        if not os.path.isdir(screenshots_dir):
            raise FileNotFoundError(f"Missing screenshots directory: {screenshots_dir}")


        templates = load_templates(compare_dir)
        
        a = 0
        while os.path.exists(os.path.join(screenshots_dir, f'screenshot-{a}.png')):
            a += 1
        take_screen(a)
        real_img = cv2.imread(os.path.join(screenshots_dir, f'screenshot-{a}.png'))

        if real_img is not None:
            logger.info("=== Not Test: board ===")
            board_real = scan_board(real_img, templates,16,30,None)
            print("Real Board:")
            board1 = board(board_real)
            board1.visualise_board()
            print("")
            board1.one_step_solve()
        else:
            print(f"Screenshot not found at {os.path.join(screenshots_dir, f'screenshot-{a}.png')}")
        


    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(f"Error in solver main block: {exc}")
