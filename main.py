import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 1000
s_height = 630
play_width = 270  # meaning 270 // 10 = 27 width per block
play_height = 540  # meaning 540 // 20 = 27 height per block
block_size = 27

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '.....',
      '0000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 200, 0), (200, 0, 0), (0, 200, 200), (200, 200, 0), (200, 165, 0), (0, 0, 200), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    grid_p2 = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
                grid_p2[i][j] = c
    return grid, grid_p2


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False

#random shape generator
def get_shape():
    return Piece(5, 0, random.choice(shapes)), Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("impact", size, bold=False)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))

#Grid
def draw_grid(surface, grid):
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (150, sy + i*block_size), (150+play_width, sy+ i*block_size))
        pygame.draw.line(surface, (128, 128, 128), (550, sy + i * block_size), (550 + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (150 + j*block_size, sy),(150 + j*block_size, sy + play_height))
            pygame.draw.line(surface, (128, 128, 128), (550 + j * block_size, sy),(550 + j * block_size, sy + play_height))

def clear_rows(grid, grid_p2, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    for i in range(len(grid_p2)-1, -1, -1):
        row = grid_p2[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_next_shape(shape, surface, shape_p2):
    font = pygame.font.SysFont('impact', 30)
    label = font.render('Next Piece', 1, (255,255,255))
    format = shape.shape[shape.rotation % len(shape.shape)]
    format_p2 = shape_p2.shape_p2[shape_p2.rotation % len(shape_p2.shape_p2)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (850 + j * block_size, 170 + i * block_size, block_size - 2, block_size - 2), 0)

    for i, line in enumerate(format_p2):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape_p2.color, (10 + j * block_size, 170 + i * block_size, block_size - 2, block_size - 2), 0)

    surface.blit(label, (850, 120))
    surface.blit(label, (10, 120))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, grid_p2, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('impact', 60)
    label = font.render('TeamTris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 20))

    # current score
    font = pygame.font.SysFont('impact', 25)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (10, sy*1.5))
    # high score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    surface.blit(label, (s_width-label.get_width()-10, sy*1.5))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (150 + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
            pygame.draw.rect(surface, grid_p2[i][j], (550 + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (150, top_left_y, play_width, play_height), 5)
    pygame.draw.rect(surface, (255, 0, 0), (550, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    # pygame.display.update()


def main(win):  # *
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)[0]
    grid_p2 = create_grid(locked_positions)[1]

    change_piece = False
    run = True
    current_piece = get_shape()[0]
    current_piece_p2 = get_shape()[1]
    next_piece = get_shape()[0]
    next_piece_p2 = get_shape()[1]
    clock = pygame.time.Clock()
    fall_time = 0
    start_fall_speed = 0.35
    fall_speed = 0.35
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)[0]
        grid_p2 = create_grid(locked_positions)[1]
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            current_piece_p2.y +=1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
            if not (valid_space(current_piece_p2, grid_p2)) and current_piece_p2.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_x:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x += 2
                            if not (valid_space(current_piece, grid)):
                                current_piece.x -= 1
                                current_piece.rotation -= 1
                if event.key == pygame.K_z:
                    current_piece.rotation -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x-=1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x +=2
                            if not (valid_space(current_piece, grid)):
                                current_piece.x-=1
                                current_piece.rotation+=1
                if event.key == pygame.K_SPACE:
                    for i in range(20):
                        current_piece.y+=1
                        if not(valid_space(current_piece, grid)):
                            current_piece.y -= 1
                if event.key == pygame.K_a:
                    current_piece_p2.x -= 1
                    if not(valid_space(current_piece_p2, grid_p2)):
                        current_piece_p2.x += 1
                if event.key == pygame.K_d:
                    current_piece_p2.x += 1
                    if not(valid_space(current_piece_p2, grid_p2)):
                        current_piece_p2.x -= 1
                if event.key == pygame.K_s:
                    current_piece_p2.y += 1
                    if not(valid_space(current_piece_p2, grid_p2)):
                        current_piece_p2.y -= 1
                if event.key == pygame.K_w:
                    current_piece_p2.rotation += 1
                    if not(valid_space(current_piece_p2, grid_p2)):
                        current_piece_p2.rotation -= 1
                if event.key == pygame.K_LCTRL:
                    for i in range(20):
                        current_piece_p2.y+=1
                        if not(valid_space(current_piece_p2, grid_p2)):
                            current_piece_p2.y -= 1

        shape_pos = convert_shape_format(current_piece, current_piece_p2)

        for i in range(len(shape_pos[0])):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        for i in range(len(shape_pos[1])):
            x, y = shape_pos[i]
            if y > -1:
                grid_p2[y][x] = current_piece_p2.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                p_p2 = (pos_p2[0], pos_p2[1])
                locked_positions[p] = current_piece.color
                locked_positions_p2[p_p2] = current_piece_p2.color
            current_piece = next_piece
            current_piece_p2 = next_piece_p2
            next_piece = get_shape()[0]
            next_piece_p2 = get_shape()[1]
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            if score > 200:
                fall_speed = start_fall_speed/(score/200)

        draw_window(win, grid, grid_p2, score, last_score)
        draw_next_shape(next_piece, next_piece_p2, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(5000)
            run = False
            update_score(score)


def main_menu(win):  # *
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TeamTris')
main_menu(win)