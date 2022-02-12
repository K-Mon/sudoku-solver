import numpy as np
from bs4 import BeautifulSoup
import numpy as np
import re
import requests

class SudokuPuzzle:
    def __init__(self, board):
        self.board = board
        self.dimension = board.shape
    
    def print_puzzle(self):
        print()
        for i in range(self.dimension[0]):
            row_string = ""
            for j in range(self.dimension[1]):
                if j == 0:
                    row_string = row_string + f"{self.board[i,j]} "
                elif j%3 == 0:
                    row_string = row_string + f"|| {self.board[i,j]} "
                else:
                    row_string = row_string + f"| {self.board[i,j]} "
            print(row_string)
            if (i+1)%3 == 0 and (i+1) != 9:
                print("-----------------------------------")
                print("-----------------------------------")
            elif i < 8:
                print("-----------------------------------")   
        print()

    def get_grid(self, row, col):
        step = 3
        for row_section in range(step,step*3+1, step):
            if row < row_section:
                for col_section in range(step,step*3+1,step):
                    if col < col_section:
                        return self.board[row_section-step:step, col_section-step:col_section].flatten()

    def check_value(self, number, row, col):
        row_check = self.board[row]
        col_check = [self.board[i,col] for i in range(self.dimension[1])]
        grid = self.get_grid(row, col)
        
        if number in col_check or number in row_check or number in grid:
            return False
        else:
            return True

    def find_empty_space(self):
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                if self.board[i][j] == 0:
                    return (i,j)
        return False

    def solve_puzzle(self):

        empty_space = self.find_empty_space()
        if empty_space == False:
            return True

        for number in range(1,10):
            if self.check_value(number, empty_space[0], empty_space[1]) == True:
                self.board[empty_space[0]][empty_space[1]] = number

                if self.solve_puzzle() == True:
                    return True
                
                self.board[empty_space[0]][empty_space[1]] = 0
        return False

    def reset_board(self, board):
        self.board = board

class NyTimesPuzzles:
    
    def __init__(self):
        self.puzzles = {}

    def get_todays_puzzles(self):
        soup = BeautifulSoup(requests.get("https://www.nytimes.com/puzzles/sudoku/easy").content,
                             features="html.parser")
        soup = re.findall(r'"puzzle":\[(.*?)\]', soup.find("div", class_="pz-game-wrapper").script.string)
        difficulty = ["Easy","Hard","Medium"]
        for indx,puzzle_lst in enumerate(soup):
            puzzle_numbers = [int(number) for number in puzzle_lst.split(",")]
            puzzle = np.zeros(shape=(9,9), dtype=int)
            for i in range(9):
                for j in range(9):
                    x = puzzle_numbers.pop(0)
                    puzzle[i,j] = x
            self.puzzles[difficulty[indx]] = puzzle
            
    def get_difficulties(self):
        if len(self.puzzles) < 1:
            print("No Puzzles Collectec, Please run get_todays_puzzles")
        else:
            print(list(self.puzzles.keys()))
    def get_puzzle(self,diff):
        return self.puzzles[diff]

def main():
    ## Create puzzle
    board = np.array([
            [6,0,1,5,8,4,0,0,0],
            [5,3,7,0,0,1,0,0,6],
            [0,0,0,0,0,0,9,1,5],
            [4,0,8,0,1,0,5,0,0],
            [0,1,0,0,5,2,0,7,4],
            [7,5,0,4,6,0,0,0,1],
            [0,4,5,1,0,0,0,0,0],
            [0,6,9,0,0,0,0,3,7],
            [1,0,0,3,0,6,0,5,0]])
    
    puzzle = SudokuPuzzle(board)
    puzzle.print_puzzle()
    print()
    puzzle.solve_puzzle()
    puzzle.print_puzzle()
    print("--------")
    ny_times = NyTimesPuzzles()
    ny_times.get_todays_puzzles()
    ny_times.get_difficulties()
    puzzle.reset_board(ny_times.get_puzzle("Hard"))
    puzzle.print_puzzle()
    print()
    puzzle.solve_puzzle()
    puzzle.print_puzzle()

main()
    
        
