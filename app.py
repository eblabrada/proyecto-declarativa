from game2dboard import Board
from tkinter import messagebox
import random
import os

FIELD_DIM = 25
BLOCK_SIZE = 25

robot = []
moves = []
it = 0
lastMove = ""
sx = 0
sy = 0

def kbd_fn(key):
    global lastMove
    if key == "F2":
        setup()
    elif key == "Escape":
        field.close()

def timer_fn():
    global it
    head_row, head_col = robot[0]
    lastMove = moves[it]
    it += 1
    if lastMove == "Left":
        head_col -= 1
    elif lastMove == "Right":
        head_col += 1
    elif lastMove == "Up":
        head_row -= 1
    elif lastMove == "Down":
        head_row += 1
    caught = False
    if it == len(moves):
        field.stop_timer()
        if messagebox.askyesno("Robot Collector Path", "Finished!\nRestart?"):
            setup()
            return
        else:
            field.close()
    field[head_row][head_col] = 'dancebot'
    robot.insert(0, (head_row, head_col))
    last_row, last_col = robot[-1]
    robot.pop()
    if not caught:
        field[last_row][last_col] = None
    
    if field[sx][sy] == None:
        field[sx][sy] = 'house'

def garbage_random_position():
    for _ in range(random.randint(1, 15)):
      while True:
          r = random.randint(0, FIELD_DIM-1)   # Random row
          c = random.randint(0, FIELD_DIM-1)    # Random collumn
          if field[r][c] is None:                 # It must be an empty place
              field[r][c] = "garbage"
              break

def setup():
    global robot, lastMove, moves, it, sx, sy
    sx = random.randint(0, FIELD_DIM - 1)
    sy = random.randint(0, FIELD_DIM - 1)
    it = 0
    field.fill(None)
    robot = [(sx, sy)]      # Initial robot position
    for pos in robot:
        field[pos[0]][pos[1]] = 'dancebot'  # Draw the robot
    garbage_random_position()
    send_map()

    os.system("ghc prog.hs")
    os.system("./prog")
    
    moves = get_moves()
    
    os.system("rm map.txt")
    os.system("rm path.txt")
    os.system("rm prog")
    
    field.start_timer(300)              # 300 ms

def send_map():
    mat = [[0 for i in range(FIELD_DIM)] for j in range(FIELD_DIM)]
    for i in range(FIELD_DIM):
        for j in range(FIELD_DIM):
            if field[i][j] == "garbage":
                mat[i][j] = 2
            elif field[i][j] == "dancebot":
                mat[i][j] = 1
    
    with open('map.txt', 'w') as f:
        for row in mat:
            f.write(' '.join([str(a) for a in row]) + '\n')

def get_moves():
    path = []
    with open('path.txt', 'r') as f:
        path = f.readline()
    path = path.replace('(', '').replace(')', '').replace('\n', '').split(' ')
    path = path + [path[0]]
    
    result = []
    for i in range(len(path) - 1):
        result += get(path[i], path[i + 1])
    return result

def get(coord1, coord2):
    x1, y1 = map(int, coord1.split(','))
    x2, y2 = map(int, coord2.split(','))

    result = []
    if x1 > x2:
        for _ in range(x1 - x2):
            result.append("Up")
    else:
        for _ in range(x2 - x1):
            result.append("Down")
    
    if y1 > y2:
        for _ in range(y1 - y2):
            result.append("Left")
    else:
        for _ in range(y2 - y1):
            result.append("Right")

    return result

field = Board(FIELD_DIM, FIELD_DIM)
field.cell_size = BLOCK_SIZE
field.title = "Robot Collector Path"
field.cursor = None                         # Hide the cursor
field.margin = 10
field.grid_color = "dark sea green"
field.margin_color = "dark sea green"
field.cell_color = "PaleGreen4"
field.on_key_press = kbd_fn
field.on_timer = timer_fn

setup()
field.show()