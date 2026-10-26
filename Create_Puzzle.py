import os
import json
import re
import numpy as np
from random import shuffle, randint
from Complete_Grid import update_possibilities, print_grid
from copy import deepcopy

def find_grid(prefix="sudoku_grid_no_", extension=".json"):
    exclude = ("easy", "medium", "hard", "evil")
    count = 0
    for f in os.listdir():
        if f.startswith(prefix) and f.endswith(extension) and not any(tag in f for tag in exclude):
            count += 1
    new_filename = f"{prefix}{count}{extension}"
    return new_filename


def choose_difficulty():
    valid_choice = False
    difficulty = '1'
    while not valid_choice:
        choice = input("Sudoku Difficult (Easy/Medium/Hard/Evil): ").strip()
        match choice:
            case "Easy" | "easy":
                difficulty = 'easy'
                min_num = randint(36, 46)
            case "Medium" | "medium":
                difficulty = 'medium'
                min_num = randint(27, 35)
            case "Hard" | "hard":
                difficulty = 'hard'
                min_num = randint(22, 27)
            case "Evil" | "evil":
                difficulty = 'evil'
                min_num = randint(17, 22)
            case _:
                print("That was not a valid difficulty, please try again.")
        if not difficulty.isnumeric():
            valid_choice = True
    return difficulty, min_num


def random_cell_list(grid):
    list = np.arange(0, 81, 1)
    shuffle(list)
    return list
    
    
def generate_possibilities(grid):
    possibilities = [[[1, 2, 3, 4, 5, 6, 7, 8, 9] for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                possibilities = update_possibilities(possibilities, grid[i][j], i, j)
            else:
                continue
    return possibilities
     
        
def check_valid(puzzle, full_grid):
    if puzzle == full_grid:
        return True
    else:
        return False
    
    
def difficulty_techniques(difficulty):
    easy_difficulty = [naked_single, hidden_single]
    medium_difficulty = ["naked_pair", "hidden_pair", "pointing_pair_triple", "box_line_reduction"]
    hard_difficulty = ["naked_triple_quad", "hidden_triple_quad", "X_wing", "Swordfish", "Y_wing", "XYZ_wing"]
    evil_difficulty =["Simple_coloring", "X_cycles", "Unique_rectangles", "Forcing_chains", "Bowmans_bingo"]
    if difficulty == 'easy':
        return easy_difficulty
    elif difficulty == 'medium':
        techniques = easy_difficulty + medium_difficulty
        return techniques
    elif difficulty == 'hard':
        techniques = easy_difficulty + medium_difficulty + hard_difficulty
        return techniques
    elif difficulty == 'evil':
        techniques = easy_difficulty + medium_difficulty + hard_difficulty + evil_difficulty
        return techniques
    
    
def create_puzzle(grid, difficulty, min_num):
    puzzle = deepcopy(grid)
    cells = random_cell_list(grid)
    for cell in cells:
        if sum(cell == 0 for row in puzzle for cell in row) == min_num:
            return puzzle
        i = cell // 9 
        j = cell % 9 
        backup = puzzle[i][j]
        puzzle[i][j] = 0
        if difficulty == 'easy':
            solvable = can_solve_with(deepcopy(puzzle), difficulty_techniques(difficulty), grid)
        elif difficulty == 'medium':
            solvable = can_solve_with(deepcopy(puzzle), difficulty_techniques(difficulty), grid)
        elif difficulty == 'hard':
            solvable = can_solve_with(deepcopy(puzzle), difficulty_techniques(difficulty), grid)
        elif difficulty == 'evil':
            solvable = can_solve_with(deepcopy(puzzle), difficulty_techniques(difficulty), grid)
        unique = count_solutions(deepcopy(puzzle)) == 1
        if not solvable or not unique:
            puzzle[i][j] = backup
    return puzzle
  
  
def can_solve_with(puzzle, techniques, full_grid):
    possibilities = generate_possibilities(puzzle)
    solved = False
    while not solved:
        step_success = False
        for tech in techniques:
            working_technique, puzzle, possibilities = tech(puzzle, possibilities) 
            if working_technique:
                step_success = True
                break
        if not step_success:
            solved = check_valid(puzzle, full_grid)
            if solved: 
                return True
            else:
                return False


def naked_single(puzzle, possibilities):
    naked_singles = []
    for i in range(9):
        for j in range(9):
            if isinstance(possibilities[i][j], list) and len(possibilities[i][j]) == 1:
                puzzle[i][j] = possibilities[i][j][0]
                possibilities = update_possibilities(possibilities, puzzle[i][j], i, j)
                return True, puzzle, possibilities
    return(False, puzzle, possibilities)


def hidden_single(puzzle, possibilities):
    for i in range(9):
        for num in range(1, 10):
            row_poss = [possibilities[i][c] for c in range(9)]
            count_rows = sum(num in cell for cell in row_poss if isinstance(cell, list))
            if count_rows == 1:
                col = next(c for c in range(9) if isinstance(possibilities[i][c], list) and num in possibilities[i][c])
                puzzle[i][col] = num
                possibilities = update_possibilities(possibilities, num, i, col)
                return True, puzzle, possibilities

            col_poss = [possibilities[r][i] for r in range(9)]
            count_cols = sum(num in cell for cell in col_poss if isinstance(cell, list))
            if count_cols == 1:
                row = next(r for r in range(9) if isinstance(possibilities[r][i], list) and num in possibilities[r][i])
                puzzle[row][i] = num
                possibilities = update_possibilities(possibilities, num, row, i)
                return True, puzzle, possibilities
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            for num in range(1, 10):
                block_cells = [(r, c)
                    for r in range(br, br+3)
                    for c in range(bc, bc+3)
                    if isinstance(possibilities[r][c], list) and num in possibilities[r][c]]
                if len(block_cells) == 1:
                    r, c = block_cells[0]
                    possibilities[r][c] = num
                    return True, puzzle, possibilities
    return False, puzzle, possibilities


def count_solutions(puzzle, limit=2):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                count = 0
                for num in range(1, 10):
                    puzzle[i][j] = num
                    if is_valid_placement(puzzle, i, j, num):
                        count += count_solutions(puzzle, limit)
                        if count >= limit:
                            puzzle[i][j] = 0
                            return count
                puzzle[i][j] = 0  # backtrack after trying all nums for this cell
                return count
    return 1


def is_valid_placement(puzzle, ni, nj, num):
    if puzzle[ni].count(num) > 1:
        return False
    if [puzzle[r][nj] for r in range(9)].count(num) > 1:
        return False
    br, bc = (ni // 3) * 3, (nj // 3) * 3
    block = [puzzle[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
    if block.count(num) > 1:
        return False
    return True


def save_puzzle(puzzle, file_name, difficulty):
    for ch in file_name:
        if ch.isdigit():
            num = int(ch)
            break
    new_file_name = f"sudoku_grid_no_{num}_{difficulty}.json"
    with open(new_file_name, "w") as f:
        json.dump(puzzle, f)
        
    
if __name__ == "__main__":
    file_name = find_grid()
    with open(file_name, "r") as f:
        grid = json.load(f)
    #difficulty, min_num = choose_difficulty()
    difficulty, min_num = 'easy', 39
    puzzle = create_puzzle(grid, difficulty, min_num)
    save_puzzle(puzzle, file_name, difficulty)
    print_grid(grid)
    print()
    print_grid(puzzle)
    
