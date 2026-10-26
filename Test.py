import json
from Complete_Grid import update_possibilities
        
def generate_possibilities(grid):
    possibilities = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                possibilities = update_possibilities(possibilities, grid[i][j], i, j)
            else:
                continue
    return possibilities


with open("sudoku_grid_no_1.json", "r") as f:
        grid = json.load(f)
grid[0][0] = 0
grid[1][2] = 0
grid[0][1] = 0
grid[2][1] = 0
grid[0][5] = 0
grid[0][7] = 0
grid[4][0] = 0
grid[1][6] = 0
grid[6][2] = 0
grid[0][2] = 0
grid[7][3] = 0
grid[2][8] = 0
grid[6][5] = 0
possibilities = generate_possibilities(grid)

for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [( r, c, possibilities[r][c])
                for r in range(br, br+3)
                for c in range(bc, bc+3)
                if isinstance(possibilities[r][c], list)]
            print(block)
