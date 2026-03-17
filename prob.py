import numpy as np
import colorama 
import collections
import math
import solver

def square_size(board):
    rows = len(board)
    columns = len(board[0])
    size = math.gcd(rows,columns)
    while math.log(rows,size) < 2:
        if rows % 2 == 0 and columns % 2 == 0:
            size //= 2
        elif rows % 3 == 0 and columns % 3 == 0:
            size //= 3
        else:
            continue
    return size

def prob_call(board,totalmines):
    v_board = np.copy(board)
    domains = solver.identify_domains(board, v_board, solver.identify_num(board))
    totalmines = totalmines - collections.Counter(board.flatten())[10]
    sim_size = square_size(board)
    
    return totalmines

print(prob_call(solver.one_step_solve(solver.array),40))