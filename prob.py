def prob_calc(board):
    dirs = [(dx,dy) for dx in (-1,0,1) for dy in (-1,0,1) if (dx,dy) != (0,0)]
    sig = []
    rows = len(board)
    cols = len(board[0])
    
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != -1:
                continue
            for dx,dy in dirs:
                x,y=i+dx,j+dy
                if 0 <= x < rows and 0 <= y < cols and 1 <= board[x][y] <= 8:
                    sig.append((i, j))
                    break
    return sig
    