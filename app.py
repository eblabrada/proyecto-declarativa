from game2dboard import Board
from tkinter import messagebox
import random
import os

FIELD_DIM = 25
BLOCK_SIZE = 25

class RobotCollector:
    def __init__(self):
        self.robot = []
        self.moves = []
        self.it = 0
        self.last_move = ""
        self.sx = 0
        self.sy = 0
        self.field = Board(FIELD_DIM, FIELD_DIM)
        self.setup_board()

    def setup_board(self):
        self.field.cell_size = BLOCK_SIZE
        self.field.title = "Robot Collector Path"
        self.field.cursor = None
        self.field.margin = 10
        self.field.grid_color = "dark sea green"
        self.field.margin_color = "dark sea green"
        self.field.cell_color = "PaleGreen4"
        self.field.on_key_press = self.kbd_fn
        self.field.on_timer = self.timer_fn
        self.setup()
        self.field.show()

    def kbd_fn(self, key):
        if key == "F2":
            self.setup()
        elif key == "Escape":
            self.field.close()

    def timer_fn(self):
        head_row, head_col = self.robot[0]
        self.last_move = self.moves[self.it]
        self.it += 1
        if self.last_move == "Left":
            head_col -= 1
        elif self.last_move == "Right":
            head_col += 1
        elif self.last_move == "Up":
            head_row -= 1
        elif self.last_move == "Down":
            head_row += 1
        if self.it == len(self.moves):
            self.field.stop_timer()
            if messagebox.askyesno("Robot Collector Path", "Finished!\nRestart?"):
                self.setup()
                return
            else:
                self.field.close()
        self.field[head_row][head_col] = 'dancebot'
        self.robot.insert(0, (head_row, head_col))
        last_row, last_col = self.robot.pop()
        self.field[last_row][last_col] = None
        if self.field[self.sx][self.sy] is None:
            self.field[self.sx][self.sy] = 'house'

    def garbage_random_position(self):
        for _ in range(random.randint(1, 15)):
            while True:
                r = random.randint(0, FIELD_DIM-1)
                c = random.randint(0, FIELD_DIM-1)
                if self.field[r][c] is None:
                    self.field[r][c] = "garbage"
                    break

    def setup(self):
        self.sx = random.randint(0, FIELD_DIM - 1)
        self.sy = random.randint(0, FIELD_DIM - 1)
        self.it = 0
        self.field.fill(None)
        self.robot = [(self.sx, self.sy)]
        for pos in self.robot:
            self.field[pos[0]][pos[1]] = 'dancebot'
        self.garbage_random_position()
        self.send_map()
        self.compile_and_run_haskell()
        self.moves = self.get_moves()
        self.cleanup_files()
        self.field.start_timer(300)

    def send_map(self):
        mat = [[0 for _ in range(FIELD_DIM)] for _ in range(FIELD_DIM)]
        for i in range(FIELD_DIM):
            for j in range(FIELD_DIM):
                if self.field[i][j] == "garbage":
                    mat[i][j] = 2
                elif self.field[i][j] == "dancebot":
                    mat[i][j] = 1
        with open('map.txt', 'w') as f:
            for row in mat:
                f.write(' '.join(map(str, row)) + '\n')

    def compile_and_run_haskell(self):
        os.system("ghc prog.hs")
        os.system("./prog")

    def get_moves(self):
        with open('path.txt', 'r') as f:
            path = f.readline().strip()
        path = path.replace('(', '').replace(')', '').split(' ')
        path.append(path[0])
        result = []
        for i in range(len(path) - 1):
            result += self.get_directions(path[i], path[i + 1])
        return result

    def get_directions(self, coord1, coord2):
        x1, y1 = map(int, coord1.split(','))
        x2, y2 = map(int, coord2.split(','))
        result = []
        if x1 > x2:
            result.extend(["Up"] * (x1 - x2))
        else:
            result.extend(["Down"] * (x2 - x1))
        if y1 > y2:
            result.extend(["Left"] * (y1 - y2))
        else:
            result.extend(["Right"] * (y2 - y1))
        return result

    def cleanup_files(self):
        os.remove("map.txt")
        os.remove("path.txt")
        os.remove("prog")

if __name__ == "__main__":
    RobotCollector()