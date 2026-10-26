import numpy as np
from random import randint
import os
import json

def number_check_order():
    possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    number_order = []
    for i in range(0, 9):
        j = randint(0, len(possible_numbers)-1)
        number_order.append(possible_numbers[j])
        possible_numbers.pop(j)
    return number_order


def populate_grid(list, order):
    for i in range(0, 9):
        for j in range(0, 9):
            list[i][j] = order[:]
    return list
  
    
def check_valid_rows(grid):
     for i in range(0, 9):
        row_seen, row_duplicates = set(), []
        for j in range(0, 9):
            if grid[i][j] == 0:
                continue
            elif grid[i][j] in row_seen:
                row_duplicates.append(grid[i][j])
            else:
                row_seen.add(grid[i][j])
        if len(row_duplicates) > 0:
            return False
     return True 
        
        
def check_valid_columns(grid):
    for j in range(0, 9):
        column_seen, column_duplicates = set(), []
        for i in range(0, 9):
            if grid[i][j] == 0:
                continue 
            elif grid[i][j] in column_seen:
                column_duplicates.append(grid[i][j])
            else:
                column_seen.add(grid[i][j])
        if len(column_duplicates) > 0:
            return False
    return True


def check_valid_block(grid):
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [grid[r][c]
                     for r in range(br, br+3)
                     for c in range(bc, bc+3)]
            
            vals = [x for x in block if x != 0]
            if len(vals) != len(set(vals)):
                return False
    return True

    
def check_valid(grid):
    row_result = check_valid_rows(grid)
    column_result = check_valid_columns(grid)    
    block_result = check_valid_block(grid)
    if row_result and column_result and block_result:
        return True
    else:
        return False 
 

def update_possibilities(possibilities, new_number, ni, nj):
    possibilities[ni][nj] = 0
    for i in range(0, 9):
        if i != ni and isinstance(possibilities[i][nj],list) and new_number in possibilities[i][nj]:
            possibilities[i][nj].remove(new_number)
        if i != nj and isinstance(possibilities[ni][i],list) and new_number in possibilities[ni][i]:
            possibilities[ni][i].remove(new_number)
    br, bc = (ni // 3) * 3, (nj // 3) * 3
    for i in range(3):
        for j in range(3):
            if br+i == ni and bc+j == nj:
                continue
            elif isinstance(possibilities[br+i][bc+j], list) and new_number in possibilities[br+i][bc+j]:
                possibilities[br+i][bc+j].remove(new_number) 
    return possibilities       


def print_candidates(possibilities, grid):
    for sudoku_row in range(9):

        # Each Sudoku cell is printed as 3 text rows
        for mini_row in range(3):
            line = ""

            for sudoku_col in range(9):
                candidates = possibilities[sudoku_row][sudoku_col]

                # Solved cell
                if candidates == 0:
                    solved = grid[sudoku_row][sudoku_col]

                    for mini_col in range(3):
                        if mini_row == 1 and mini_col == 1:
                            line += str(solved)
                        else:
                            line += "."

                        if mini_col < 2:
                            line += " "

                # Unsolved cell
                else:
                    for mini_col in range(3):
                        num = mini_row * 3 + mini_col + 1

                        if num in candidates:
                            line += str(num)
                        else:
                            line += "."

                        if mini_col < 2:
                            line += " "

                line += "  "

                if sudoku_col in (2, 5):
                    line += "| "

            print(line)

        if sudoku_row in (2, 5):
            print("-" * len(line))
      
            
def print_grid(grid):
    for row in range(9):
        line = ""
        for col in range(9):
            line += str(grid[row][col])
            if col in (2, 5):
                line += " | "
            elif col < 8:
                line += " "
        print(line)
        if row in (2, 5):
            print("-" * len(line))
            
            
def build_sudoku(grid, possibilities, number_order):
    
    complete = False
    attempt_tracking, lost_possibilities = [], []
    max_depth_reached, steps_since_improvement, total_steps = 0, 0, 0
    while complete == False:
        total_steps += 1
        if total_steps > 50000:
            return False, 0
        if max_depth_reached < len(attempt_tracking):
            max_depth_reached = len(attempt_tracking)
            steps_since_improvement = 0
        else:
            steps_since_improvement += 1
        if steps_since_improvement > 5000:
            return False, 0      
        cells = [(len(possibilities[i][j]), i, j) 
         for i in range(9) for j in range(9) 
         if isinstance(possibilities[i][j], list)]
        if not cells:
            complete = True
            break
        
        smallest = min(c[0] for c in cells)
        if smallest == 0:
            ni, nj, new_number, attempt_tracking = backtrack(possibilities, attempt_tracking, number_order, lost_possibilities)
            continue
        else:
            candidates = [(i, j) for length, i, j in cells if length == smallest]
            ni, nj = candidates[randint(0, len(candidates)-1)]
            new_number = possibilities[ni][nj][0]
        attempt_tracking.append((ni, nj, new_number))
        lost_possibilities.append(possibilities[ni][nj])
        grid[ni][nj] = new_number
        possibilities = update_possibilities(possibilities, new_number, ni, nj) 
    #print_candidates(possibilities, grid)
    return True, grid
    
                
def backtrack(possibilities, attempt_tracking, number_order, lost_possibilities):
    li, lj, lnumber = attempt_tracking[-1]
    for i in range(0, 9):
        if i != li and isinstance(possibilities[i][lj],list) and lnumber not in possibilities[i][lj]:
            possibilities[i][lj] = insert_by_original_order(possibilities[i][lj], lnumber, number_order)
        if i != lj and isinstance(possibilities[li][i],list) and lnumber not in possibilities[li][i]:
            possibilities[li][i] = insert_by_original_order(possibilities[li][i], lnumber, number_order)
    br, bc = (li // 3) * 3, (lj // 3) * 3
    for i in range(3):
        for j in range(3):
            if br+i == li and bc+j == lj:
                continue
            elif isinstance(possibilities[br+i][bc+j], list) and lnumber not in possibilities[br+i][bc+j]:
                possibilities[br+i][bc+j] = insert_by_original_order(possibilities[br+i][bc+j], lnumber, number_order)
    new_possibilities = insert_by_original_order(lost_possibilities[-1], lnumber, number_order)
    possibilities[li][lj] = new_possibilities[:]
    ind = new_possibilities.index(lnumber)
    if ind == len(new_possibilities) - 1:
        attempt_tracking.pop(-1)
        lost_possibilities.pop(-1)
        return backtrack(possibilities, attempt_tracking, number_order, lost_possibilities)
    else:
        attempt_tracking[-1] = (li, lj, possibilities[li][lj][ind+1])
        return li, lj, possibilities[li][lj][ind+1], attempt_tracking
  
        
def insert_by_original_order(current, x, order):
    pos_x = order.index(x)
    for i, val in enumerate(current):
        if order.index(val) > pos_x:
            current.insert(i, x)
            return current
    current.append(x)
    return current


def run_test():
    solved = False
    while solved == False:
        empty_possibilities, grid = [[[] for _ in range(9)] for _ in range(9)], [[0 for _ in range(9)] for _ in range(9)]
        number_order = number_check_order() 
        #number_order = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        possibilities = populate_grid(empty_possibilities, number_order)
        start_i, start_j = randint(0, 8), randint(0, 8)
        #start_i, start_j = 0, 0
        grid[start_i][start_j] = number_order[0]
        possibilities = update_possibilities(possibilities, number_order[0], start_i, start_j)
        valid, grid = build_sudoku(grid, possibilities, number_order)
        if valid == True:
            solved = True
        else:
            print("Failed")
            continue             
    
    
def save_grid(grid, prefix="sudoku_grid_no_", extension=".json"):
    exclude = ("easy", "medium", "hard", "evil")
    count = 0
    for f in os.listdir():
        if f.startswith(prefix) and f.endswith(extension) and not any(tag in f for tag in exclude):
            count += 1
    next_num = count + 1
    new_filename = f"{prefix}{next_num}{extension}"
    with open(new_filename, "w") as f:
        json.dump(grid, f)
        
        
    return new_filename
       
                           
if __name__ == "__main__":
    solved = False
    while solved == False:
        empty_possibilities, grid = [[[] for _ in range(9)] for _ in range(9)], [[0 for _ in range(9)] for _ in range(9)]
        number_order = number_check_order() 
        #number_order = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        possibilities = populate_grid(empty_possibilities, number_order)
        start_i, start_j = randint(0, 8), randint(0, 8)
        #start_i, start_j = 0, 0
        grid[start_i][start_j] = number_order[0]
        possibilities = update_possibilities(possibilities, number_order[0], start_i, start_j)
        valid, grid = build_sudoku(grid, possibilities, number_order)
        if valid == True:
            print_grid(grid)
            solved = True
        else:
            print("Failed")
            continue
    print(save_grid(grid))
