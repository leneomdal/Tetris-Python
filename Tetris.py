import pygame
import random


"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
pygame.init()

winWidth = 400

win = pygame.display.set_mode((1000,1000))

background_image = pygame.image.load("tetris1.png").convert()


# GLOBALS VARIABLES
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS(copied)

S = [['.....',
      '......',
      '..00..',
      '.00...',
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

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '0000.',
      '.....',
      '.....']]

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
shape_colors = [(244, 124, 124), (247, 244, 139), (161, 222, 147), (112, 161, 215), (255, 165, 0), (255, 150, 200), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):#!!!
    grid = [[(210,220,255) for x in range (10)] for x in range (20)]  # {mulig det bør være [[]] her

    for i in range (len(grid)):
        for j in range (len(grid[i])):
            if (j,i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c                          #grid er gitt ved grid[y][x]
                                                        # locked_pos er gitt ved (x,y)
    return grid

def convert_shape_format(shape):

    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate (format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)   # sjekk avhengigheten til disse konstantene

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j,i)for j in range(10) if grid[i][j] == (210,220,255)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]   # endrer til endim liste

    formatted = convert_shape_format(shape) #list of positions to compare with accepted

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True



def check_failure(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape(shapes):
    return Piece(5,0, random.choice(shapes))


def draw_text_middle(surface, text, size, color, up = 0, down = 0, right = 0, left = 0):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (int(top_left_x + int(play_width/2) - int(label.get_width()/2) + right - left), int(top_left_y + int(play_height/2) - int(label.get_height()/2)) + down - up))



def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range (len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range (len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size,sy), (sx+ j*block_size, sy + play_height ))



def clear_rows2(grid, locked_pos):
    inc = 0
    for i in range(len(grid)-1,-1,-1 ):
        row = grid[i]
        if (210,220,255) not in row:
            inc += 1

            for j in range(len(row)):
                try:
                    del locked_pos[(j,i)]
                except:
                    continue

            for k in range(i-1, -1, -1):
                for l in range(len(grid[k])):
                    if (l,k) in locked_pos:
                        locked_pos[(l, k+1)] = locked_pos.get((l,k))
                        #locked_pos[(k+1,l)] = locked_pos[(k,l)]
                        try:
                            del locked_pos[(l, k)]
                        except:
                            continue
    return inc






def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsanse', 30)
    label = font.render('Next shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = int(top_left_y + play_height/2 -100)

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i , line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size,sy + i*block_size, block_size, block_size ), 0)
    surface.blit(label, (sx + 20, sy - 30))                                 #


def draw_window(surface, grid, score = 0, last_score = 0):
    surface.fill((210,220,255))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    surface.blit(label,(top_left_x + int(play_width/2) - int(label.get_width()/2), 30))

    #current score
    font = pygame.font.SysFont('comicsanse', 30)
    label = font.render('Current Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x - 220
    sy = int(top_left_y + play_height/2 + 90)

    surface.blit(label, (sx + 20, sy - 150))

    #last score
    label = font.render('High Score: ' + str(last_score), 1, (255, 255, 255))

    sx = top_left_x - 220
    sy = int(top_left_y + play_height/2 + 50)

    surface.blit(label, (sx + 20, sy - 150))

    for i in range (len(grid)):
        for j in range (len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)  # kan bytte 30 med blocksize her

    pygame.draw.rect(surface, (0, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5) # den svarte firkanten rundt


    draw_grid(surface, grid)
    #pygame.display.update()

def update_score(nscore):
    scores = [0,0,0,0,0]
    with open('score', 'r') as f:
        lines = f.readlines()
        for i in range(0, 5):
            scores[i] = lines[i].strip()

    #score = highest_score()
    index = 0

    for i in range(0, 5):
        if nscore > int(scores[i]):
            index = i
            break
    for i in range (4, index, -1):
        scores[i] = scores[i-1]
    scores[index] = nscore

    with open('score', 'w') as f:
        for i in range (0,5):
            f.write(str(scores[i])+ "\n")

        #if int(score)>nscore :
        #    f.write(str(score))
        #else:
        #    f.write(str(nscore))

def highest_score():
    with open('score', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return  score

def move_piece_down(current_piece):
    pass





def main(win):
    global grid
    last_score = highest_score()

    locked_pos = {}
    grid = create_grid(locked_pos)

    change_piece = False
    run = True
    swiched_piece = False
    move_down = False

    current_piece = get_shape(shapes)
    next_piece = get_shape(shapes)
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        r = random.randint(0, 4)

        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()


        if level_time/1000 > 5:              #øker farten den faller med hvert 5 sek
            level_time = 0
            if fall_speed > 0.12:        # terminal fart
                fall_speed -= 0.005         # hvor fort den når max hast

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece,grid)) and current_piece.y > 0:  # sjekk om det har truffet bunn, eller en annen brikke
                current_piece.y -= 1
                change_piece = True
                #...

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                #pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x +=1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation +=1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_DOWN:

                    move_down = True
                    #current_piece.y +=1
                    #if not(valid_space(current_piece, grid)):
                    #    current_piece.y -= 1

                if event.key == pygame.K_SPACE and swiched_piece == False:
                    current_piece = next_piece
                    next_piece = get_shape(shapes)
                    swiched_piece = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    move_down = False

        if move_down == True:
            current_piece.y += 1
            pygame.time.delay(10)
            if not (valid_space(current_piece, grid)):
                move_down = False
                current_piece.y -= 1
                change_piece = True


        shape_pos = convert_shape_format(current_piece)

        for i in range (len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color  # legger til farge til shapene

        #hvis brikken treffer bunnen
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color     #locked pos e en dict med pos(key) og color(value)
            current_piece = next_piece
            next_piece = get_shape(shapes)
            change_piece = False
            swiched_piece = False
            score += clear_rows2(grid, locked_pos) * 10



        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_failure(locked_pos):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def high_score_list(win):
    run = True

    scores = [0,0,0,0,0]
    with open('score', 'r') as f:
        lines = f.readlines()

        for i in range (0,5):
            scores[i] = lines[i].strip()
    for j in range (0,5):
        draw_text_middle(win,str(scores[j]), 60, (255,255,255), 0, i*10)

    while run:
        win.fill(((210,220,255)))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('HIGH SCORES', 1, (255, 255, 255))

        win.blit(label, (top_left_x + int(play_width / 2) - int(label.get_width() / 2), 30))
        for j in range(0, 5):
            draw_text_middle(win,str(j+1)+ ".   " + str(scores[j]), 60, (255, 255, 255), 140, j * 60)



        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False





def main_menu(win):
    run = True
    while run:
        win.blit(background_image, [0, 0])
        #win.fill((0,0,0))
        draw_text_middle(win, "Press enter to play!", 90, (255,255,255), 120)
        draw_text_middle(win, "Or space for high scores!", 70, (255, 255, 255), 0, 20 )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main(win)
                if event.key == pygame.K_SPACE:
                    high_score_list(win)


    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game
