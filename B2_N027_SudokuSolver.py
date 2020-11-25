import pygame
import os

# To centre the window
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.font.init()

# Defining window size
screen = pygame.display.set_mode((500, 600))

# Title assigned to GUI window
pygame.display.set_caption("Sudoku DAA")

# Initializing variables 
x = 0
y = 0
dif = 500 / 9
val = 0

# Blank Sudoku Board. 
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Assigning fonts  
font1 = pygame.font.SysFont("verdana", 28)
font2 = pygame.font.SysFont("verdana", 15)


# Get position of cursor and determine where to place numbers, draw grid, etc.
# First cell is located
def get_coordinates(position):
    global x
    x = position[0] // dif
    global y
    y = position[1] // dif


# Highlight the cell selected 
def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (100, 20, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i) * dif), 7)
        pygame.draw.line(screen, (100, 30, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# Function to draw required lines for making Sudoku grid
def draw():
    # Draw the lines

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill color in numbered grid
                pygame.draw.rect(screen, (128, 212, 255), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))

    # To draw the boxes of the sudoku GUI
    for i in range(10):
        if i % 3 == 0:
            # For the main grid lines
            thick = 7
        else:
            # For the interior lines of the grid
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)


# Fill value entered in cell
def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))


# Raise error when wrong value entered
def throw_error():
    text1 = font1.render("Wrong input!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


# Check if the value entered in board is valid 
def check_valid(a, i, j, val):
    # Checking against each individual value already present on board
    # In corresponding row & column
    # To check against repeats
    for it in range(9):
        if a[i][it] == val:
            return False
        if a[it][j] == val:
            return False
    it = i // 3
    jt = j // 3
    # to check in the 3x3 sub block of the sudoku
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if a[i][j] == val:
                return False
    return True


# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    while grid[i][j] != 0:
        # Checking cursor position and moving accordingly
        if i < 8:
            i += 1
            # Moving to next row
        elif i == 8 and j < 8:
            i = 0
            j += 1
            # Reaching end of the sudoku block
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if check_valid(grid, i, j, it) == True:
            grid[i][j] = it
            global x, y
            x = i
            y = j
            # white color background
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)


            if solve(grid, i, j) == 1:
                return True
            else:
                grid[i][j] = 0
            # white color background
            screen.fill((255, 255, 255))

            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)

    return False


# Display instruction for the game
def instruction():
    text1 = font2.render("PRESS D TO VIEW SAMPLE PUZZLE / R TO EMPTY", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))


# Display options when solved 
def result():
    text1 = font1.render("Finished! Press R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))


run = True
flag1 = 0
flag2 = 0
rs = 0      # Result Flag
error = 0   # Error Flag
# The loop that keeps the window running 
while run:

    # White color background
    screen.fill((255, 255, 255))
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False
        # Using mouse chose block to enter number
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            position = pygame.mouse.get_pos()
            get_coordinates(position)
        # Get the number to be inserted
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                flag2 = 1
            # If R pressed clear the sudoku board
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            # If D is pressed reset the board to default hardcoded sample sudoku
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [0, 6, 0, 4, 0, 0, 0, 9, 2],
                    [0, 2, 5, 0, 0, 0, 4, 0, 0],
                    [7, 4, 0, 2, 3, 9, 0, 0, 0],
                    [5, 9, 6, 0, 2, 0, 0, 0, 1],
                    [4, 0, 0, 0, 0, 5, 0, 7, 0],
                    [2, 8, 7, 0, 4, 0, 0, 0, 0],
                    [0, 7, 0, 8, 0, 2, 0, 1, 5],
                    [8, 0, 0, 5, 0, 7, 3, 0, 0],
                    [0, 5, 0, 0, 0, 4, 0, 0, 0]
                ]
    if flag2 == 1:
        if solve(grid, 0, 0) == False:
            error = 1
        else:
            rs = 1
        flag2 = 0
    if val != 0:
        draw_val(val)
        # print(x)
        # print(y)
        if check_valid(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            throw_error()
        val = 0

    if error == 1:
        throw_error()
    if rs == 1:
        result()
    draw()
    if flag1 == 1:
        draw_box()
    instruction()

    # Update window
    pygame.display.update()

# Quit pygame window	 
pygame.quit()
