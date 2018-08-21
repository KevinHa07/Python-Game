"""main Module -- A game I made in Pygame.

This module is where the main method of my game will be. This game is a
puzzle game where you try to match as many combos in order to damage the
enemy in front of you. Get the the 5th stage and you win.

Example(s):
    To use this module, you can run it by double clicking on the this or use console command

    Run the program from the command line:
        $ python main.py

    Import other classes from command line:
        import orb.py
        import monsters.py
        import units.py
        import stage.py

    Use the -d flag to run the module in data mode.
        $ python -d main.py

    Attribute(s):
        board_width (int): The width of the playing board.
        board_height (int) : The height of the playing board.
        window_width (int) : The width of the window screen.
        window_height (int) : The height of the window screen.
        WHITE (int, int, int) : The RGB colors of white.
        BLACK (int, int, int) : The RGB colors of black.
        orb_size (int) : The size of orb image.
        x_margin (int) : The indent of the board so it's not at the edge of screen.
        y_margin (int) : The y margin of the board.
        orb_pic (list) : List of pictures of orbs.
        board_rectangles (list) : List of pygame rectangles.
"""
import pygame
from stage import Stage
from pygame.locals import *
import sys
import random
import copy
import os
from orb import Orb
from units import Unit
from monsters import Monsters


board_width = 6
board_height = 5
window_width = 500
window_height = 700

WHITE = (255,255,255)
BLACK = (0, 0, 0)

orb_size = 77 #orbs width and height

x_margin = 20
y_margin = 300

orb_pic = {'1':'Fire.png',
           '2':'Water.png',
           '3':'Wood.png',
           '4':'Light.png',
           '5':'Dark.png',
           '6':'Heart.png'}

board_rectangles = [] #make a list of rectangles for the board.
for x in range(board_width):
    board_rectangles.append([])
    for y in range(board_height):
        rect = pygame.Rect((x_margin + (x * orb_size),
                            y_margin + (y * orb_size),
                            orb_size, orb_size))
        board_rectangles[x].append(rect)

# ---------------------------------------------------------------------#
def main():
    """
    The main method there the game runs in.
    """
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.music.set_volume(.3)
    pygame.mixer.music.load('bgm.wav')
    pygame.mixer.music.play(-1)

    window_size = (window_width, window_height)
    global screen, held, turn, stage, empty_space, fps, fps_clock, element, hit, orb_movement
    fps = 30
    fps_clock = pygame.time.Clock()
    timer = 180
    held = False
    turn = 1
    stage = 1
    hit = pygame.mixer.Sound('hit.wav')
    hit.set_volume(1)
    orb_movement = pygame.mixer.Sound('orb_movement.wav')
    game_over = pygame.mixer.Sound('gameover.wav')

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Project")

    screen.fill(WHITE)

    empty_space = Orb('BlankOrb.png', -1)

    # making units
    unit_row1_x = 150
    unit_row1_y = [50, 110, 170]
    unit_row2_x = 90
    unit_row2_y = [80, 140]

    unit_list = []
    hp = [4534, 6236, 6082, 5125, 4300]
    attack = [2540, 2710, 3810, 2700, 2960]
    recovery = [511, 295, 191, 372, 356]
    typing = [1, 2, 3, 4, 5]
    sprite = ['unit1.png', 'unit2.png', 'unit3.png', 'unit4.png', 'unit5.png']

    for x in range(5):
        unit_list.append(Unit(hp[x], attack[x], recovery[x],
                              typing[x], sprite[x]))

    # making enemies
    enemy_list = []
    hp = [1007988, 752364, 824658, 1048752, 1289554]
    attack = [7012, 15025, 9487, 10451, 17487]
    typing = [3, 4, 2, 1, 5]
    turns = [1,2,1,1,2]
    sprite = ['enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png', 'enemy5.png']

    for x in range(5):
        enemy_list.append(Monsters(hp[x], attack[x], typing[x], turns[x], sprite[x], x + 1))

    # background
    stage_list = []
    background_list = ['EmbodimentSDM.png', 'SMD.png', 'SDMLobby.png']
    for enemy in enemy_list:
        # print(enemy.stage)
        if enemy.stage == 1:
            stage_list.append(Stage(enemy.stage, background_list[0]))
        elif enemy.stage == 2 or enemy.stage == 3:
            stage_list.append(Stage(enemy.stage, background_list[1]))
        elif enemy.stage == 4 or enemy.stage == 5:
            stage_list.append(Stage(enemy.stage, background_list[2]))


    gameBoard = get_blank_board()
    gameBoard = fill_board(gameBoard, orb_pic)
    current_selected_orb = None

    # multipliers
    #--------------------------------------------------------#
    combo = 0
    combo_multiplier = .5
    extra_orb_multiplier = 1
    recovery_multiplier = .25
    leader_skill_multiplier = 25

    total_hp = 0
    for unit in unit_list:
        total_hp += unit.hp
    current_hp = total_hp

    fire = 0
    water = 0
    wood = 0
    light = 0
    dark = 0
    for unit in unit_list:
        if unit.type == 1:
            fire += unit.attack
        elif unit.type == 2:
            water += unit.attack
        elif unit.type == 3:
            wood += unit.attack
        elif unit.type == 4:
            light += unit.attack
        else:
            dark += unit.attack

    total_recovery = 0
    for unit in unit_list:
        total_recovery += unit.recovery


    # game loop
    # --------------------------------------------------------------------#
    while True:
        total_attacks = [0,0,0,0,0,0]
        swapping_orb = None
        combo = 0

        screen.fill(BLACK)
        mouse_coordinates = pygame.mouse.get_pos()
        for x in range(board_width):
            if x % 2 == 0:
                for y in range(board_height):
                    if y % 2 == 0:
                        pygame.draw.rect(screen, (110, 57, 58), board_rectangles[x][y], 0)
                    else:
                        pygame.draw.rect(screen, (150, 90, 91), board_rectangles[x][y], 0)
            elif x % 2 == 1:
                for y in range(board_height):
                    if y % 2 == 1:
                        pygame.draw.rect(screen, (110, 57, 58), board_rectangles[x][y], 0)
                    else:
                        pygame.draw.rect(screen, (150, 90, 91), board_rectangles[x][y], 0)

        # display background
        for background in stage_list:
            if background.stage == stage:
                display_background(stage, stage_list)


        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            # -----------Mouse Events----------- #
            if event.type == MOUSEBUTTONUP:
                num_orbs = 0
                held = False
                element = []
                match_orbs = check_match(gameBoard)
                num_orb_list = []
                if match_orbs == []: # no matching orbs
                    dmg_taken = enemy_list[stage - 1].attack_return(turn)
                    current_hp = update_hp_dmg(current_hp, dmg_taken)
                else:
                    while match_orbs != []:
                        for orb_set in match_orbs:
                            for orb in orb_set:
                                num_orbs += 1
                                draw_board(gameBoard)
                                pygame.display.update()
                                pygame.time.delay(30)
                            num_orb_list.append(num_orbs)
                            num_orbs = 0
                        gameBoard = get_falling_orbs(gameBoard)
                        match_orbs = check_match(gameBoard)

                    #---------------------------------------------------------------#
                    index = 0
                    for typing in element:
                        combo += 1
                        if typing == '1':
                            total_attacks[0] += fire + (fire * (num_orb_list[index]
                                                                * extra_orb_multiplier))
                            index += 1
                        elif typing == '2':
                            total_attacks[1] += water + (water * (num_orb_list[index]
                                                                  * extra_orb_multiplier))
                            index += 1
                        elif typing == '3':
                            total_attacks[2] += wood + (wood * (num_orb_list[index]
                                                                * extra_orb_multiplier))
                            index += 1
                        elif typing == '4':
                            total_attacks[3] += light + (light * (num_orb_list[index]
                                                                  * extra_orb_multiplier))
                            index += 1
                        elif typing == '5':
                            total_attacks[4] += dark + (dark * (num_orb_list[index]
                                                                * extra_orb_multiplier))
                            index += 1
                        else:
                            total_attacks[5] += total_recovery + (total_recovery
                                             * (num_orb_list[index] * extra_orb_multiplier))
                            index += 1


                    for x in range(6):
                        if x == 0:
                            total_attacks[x] += (combo_multiplier * combo) * total_attacks[x]
                        elif x == 1:
                            total_attacks[x] += (combo_multiplier * combo) * total_attacks[x]
                        elif x == 2:
                            total_attacks[x] += (combo_multiplier * combo) * total_attacks[x]
                        elif x == 3:
                            total_attacks[x] += (combo_multiplier * combo) * total_attacks[x]
                        elif x == 4:
                            total_attacks[x] += (combo_multiplier * combo) * total_attacks[x]
                        else:
                            total_attacks[x] += (combo_multiplier * combo) * total_attacks[x]

                    enemy_list[stage - 1].update_hp(total_attacks)
                    current_hp = update_hp_rcv(current_hp, total_hp, total_attacks[5])
                    if enemy_list[stage - 1].current_hp != 0:
                        dmg_taken = enemy_list[stage - 1].attack_return(turn)
                        current_hp = update_hp_dmg(current_hp, dmg_taken)



                    for x in range(6):
                        print(total_attacks[x])



            elif event.type == MOUSEBUTTONDOWN:
                held = True
                timer = 180
                current_selected_orb = check_orb_clicked(mouse_coordinates)

            # ---------------------------------- #

        # if holding down mouse 1
        if held:
            timer -= 1
            if timer == 0:
                held = False # 6 seconds to make move
                gameBoard[current_selected_orb['x']][current_selected_orb['y']] = current_orb_copy

            if timer == 179:
                current_orb_copy = gameBoard[current_selected_orb['x']][current_selected_orb['y']]

            gameBoard[current_selected_orb['x']][current_selected_orb['y']] = empty_space
            current_orb_copy.update(screen)
            if current_selected_orb['x']+1 < 6 and current_selected_orb['y']+1 < 5:
                if(board_rectangles[current_selected_orb['x']+1]
                   [current_selected_orb['y']].collidepoint(mouse_coordinates[0],
                                                            mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']-1]
                     [current_selected_orb['y']].collidepoint(mouse_coordinates[0],
                                                              mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']]
                     [current_selected_orb['y']-1].collidepoint(mouse_coordinates[0],
                                                                mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']]
                     [current_selected_orb['y']+1].collidepoint(mouse_coordinates[0],
                                                                mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)

            elif current_selected_orb['x'] == 5 and current_selected_orb['y'] == 4:
                if(board_rectangles[current_selected_orb['x']-1]
                   [current_selected_orb['y']].collidepoint(mouse_coordinates[0],
                                                            mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']]
                     [current_selected_orb['y']-1].collidepoint(mouse_coordinates[0],
                                                                mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)

            elif current_selected_orb['x'] == 5:
                if(board_rectangles[current_selected_orb['x']-1]
                   [current_selected_orb['y']].collidepoint(mouse_coordinates[0],
                                                            mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']]
                     [current_selected_orb['y']+1].collidepoint(mouse_coordinates[0],
                                                                mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']]
                     [current_selected_orb['y']-1].collidepoint(mouse_coordinates[0],
                                                                mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)

            elif current_selected_orb['y'] == 4:
                if(board_rectangles[current_selected_orb['x']+1]
                   [current_selected_orb['y']].collidepoint(mouse_coordinates[0],
                                                            mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']-1]
                     [current_selected_orb['y']].collidepoint(mouse_coordinates[0],
                                                              mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)
                elif(board_rectangles[current_selected_orb['x']]
                     [current_selected_orb['y']-1].collidepoint(mouse_coordinates[0],
                                                                mouse_coordinates[1])):
                    swapping_orb = check_orb_clicked(mouse_coordinates)
                    gameBoard = swap_orbs(gameBoard, current_selected_orb, swapping_orb)
                    current_selected_orb = check_orb_clicked(mouse_coordinates)
                    pygame.mixer.Sound.play(orb_movement)


        # displays unit sprites on the screen
        #---------------------------------------------------------#
        k = 0
        for unit in unit_list:
            unit.update(screen, (unit_row1_x, unit_row1_y[k]))
            k += 1
            if k == 3:
                k = 0
                break

        l = 0
        m = 0
        for unit in unit_list:
            l += 1
            if l > 3:
                unit.update(screen, (unit_row2_x, unit_row2_y[m]))
                m += 1

        #---------------------------------------------------------#
        if enemy_list[stage - 1].current_hp <= 0:
            stage += 1
            font = pygame.font.SysFont('arialblack', 15)
            text = font.render(str(stage), True, BLACK)
            screen.blit(text, (window_width/2.4 , y_margin - 200))
            pygame.time.delay(60)


        display_enemy(screen, stage, turn, enemy_list)

        draw_hp(screen, current_hp, total_hp)

        draw_board(gameBoard)

        if current_hp < 0:
            pygame.mixer.Sound.play(game_over)
            pygame.mixer.music.pause()
            pygame.display.update()
            current_hp = 0

        if current_hp == 0:
            display_message()


        if held:
            font = pygame.font.SysFont('arialblack', 12)
            text = font.render(str(int(timer / 30) + 1), True, BLACK)
            screen.blit(text, (mouse_coordinates[0] - 10, mouse_coordinates[1] - 10))
        pygame.display.update()  # Update the display when all events have been processed
        fps_clock.tick(fps)

def display_message():
    """Displays the game over message when hp = 0.
    Arguments:
        None
    """
    font = pygame.font.SysFont('arialblack', 18)
    text = font.render('Game Over', True, BLACK)
    screen.blit(text, ((window_width/2.5), (window_height/4)))

def get_blank_board():
    """
    Creates a new state of a blank board.
    return:
        board(list): Returns a blank board.
    """
    board = []
    for x in range(board_width):
        # creates empty lists for each column
        board.append([empty_space]*board_height)
    return board

def fill_board(gameBoard, orb_pics):
    """
    Fills the board with random orb objects.
    Arguments:
        gameBoard(list): Gets the state of the board in which case is a blank board.
        orb_pics(list):  List of orb pictures.
    Returns:
        gameBoard(list): Returns a filled board.
    """
    same = False
    orb_pic = orb_pics
    playing_board = gameBoard

    for x in range(board_width):
        for y in range(board_height):
            orb_color = str(random.randrange(6) + 1)
            orb_type = Orb(orb_pic[orb_color], orb_color)
            playing_board[x][y] = orb_type


            if y > 1: #check if there are 3 of same color for vertical
                if (playing_board[x][y].type == playing_board[x][y - 1].type and
                    playing_board[x][y].type == playing_board[x][y - 2].type):
                    same = True
                    while same:
                        orb_color = str(random.randrange(5) + 1)
                        playing_board[x][y] = Orb(orb_pic[str(orb_color)], orb_color)
                        if (playing_board[x][y].type != playing_board[x][y - 1].type and
                            playing_board[x][y].type != playing_board[x][y - 2].type):
                            same = False

            if x > 1: #check if there are 3 of same color for horizontal
                if (playing_board[x][y].type == playing_board[x - 1][y].type and
                    playing_board[x][y].type == playing_board[x - 2][y].type):
                    same = True
                    while same:
                        orb_color = str(random.randrange(5) + 1)
                        playing_board[x][y] = Orb(orb_pic[str(orb_color)], orb_color)
                        if (playing_board[x][y].type != playing_board[x - 1][y].type and
                        playing_board[x][y].type != playing_board[x - 2][y].type):
                            same = False
    return playing_board


def drop_orbs(gameBoard):
    """
    Generates random orb objects to fall onto the board.
    Arguments:
        gameBoard: Gets the state of the board.
    """
    for x in range(board_width):
        orbsInColumn = []
        for y in range(board_height):
            if gameBoard[x][y] != empty_space:
                orbsInColumn.append(gameBoard[x][y])
        # drops orbs to bottom of board and fills the rest with new orbs
        gameBoard[x] = ([empty_space] * (board_height - len(orbsInColumn))) + orbsInColumn

def get_falling_orbs(gameBoard):
    """
    Gets dropped orbs to fill the board when match is done.
    Arguments:
        gameBoard(list): Gets the state of the game board and fills it up with new orb objects.
    Returns:
        gameBoard(list): Returns a filled game board.
    """
    # boardCopy = copy.deepcopy(gameBoard)
    drop_orbs(gameBoard)

    # fallingOrbs = []
    for x in range(board_width):
        for y in range(board_height):
            if gameBoard[x][y] == empty_space:
                orb_color = str(random.randrange(6) + 1)
                orb_type = Orb(orb_pic[orb_color], orb_color)
                gameBoard[x][y] = orb_type
    return gameBoard

def swap_orbs(gameBoard, selected_orb_xy, swapping_orb_xy):
    """
    Swaps orb objects with the selected orb with another adjacent orb.
    Arguments:
        gameBoard(list): Gets the state of the board.
        selected_orb_xy(int,int):  Coordinates of the selected orb.
        swapping_orb_xy(int,int): Coordinates of the swapping orb.
    Returns:
        gameBoard(list): Returns the state of the board after swap.
    """
    current_orb = gameBoard[selected_orb_xy['x']][selected_orb_xy['y']]
    swapping_orb = gameBoard[swapping_orb_xy['x']][swapping_orb_xy['y']]
    gameBoard[selected_orb_xy['x']][selected_orb_xy['y']] = swapping_orb
    gameBoard[swapping_orb_xy['x']][swapping_orb_xy['y']] = current_orb
    return gameBoard

def check_orb_clicked(pos):
    """
    Check which orb is currently clicked.
    Arguments:
        pos(int,int): Coordinates  of the mouse cursor.
    Returns:
        {'x':x, 'y':y}: when pos is over a rectangle object.
        None: If pos is over None Type.
    """
    for x in range(board_width):
        for y in range(board_height):
            if board_rectangles[x][y].collidepoint(pos[0], pos[1]):
                return {'x': x, 'y': y}
    return None

def draw_board(gameBoard):
    """
    iterates through the game board and blits the orb ojects.
    Arguments:
        gameBoard: Gets the state of the board to blit.
    """
    for x in range(board_width):
        for y in range(board_height):
            if gameBoard[x][y] != empty_space:
                screen.blit(gameBoard[x][y].orb, board_rectangles[x][y])


def check_match(gameBoard):
    """
    This method checks to see if there are any 3 or more orbs connected to
    each other horizontally or vertically.
    Arguments:
        gameBoard(list): Gets the state of the board.
    Returns:
        orb_remove(int,int): Gets the matching orbs and gets their xy coordinates
    """
    orb_remove = [] # a list of lists of orbs in matching triplets that should be removed
    still_have_match_orbs = True
    num = 0
    # loop through each space, checking for 3 adjacent identical orbs
    while still_have_match_orbs:
        for x in range(board_width):
            for y in range(board_height):
                # look for horizontal matches
                if x <= 3:
                    if gameBoard[x][y].type == gameBoard[x + 1][y].type == gameBoard[x + 2][y].type and gameBoard[x][y] != empty_space:
                        target_orb = gameBoard[x][y]
                        offset = 0
                        removeSet = []
                        while gameBoard[x + offset][y].type == target_orb.type:
                            if offset == 0:
                                element.append(gameBoard[x][y].type)
                            # keep checking if there's more than 3 orbs in a row
                            removeSet.append((x + offset, y))
                            gameBoard[x + offset][y] = empty_space
                            if x + offset != 5:
                                offset += 1
                            else:
                                break
                        orb_remove.append(removeSet)
                        num += 1

                # look for vertical matches
                if y <= 2:
                    if gameBoard[x][y].type == gameBoard[x][y + 1].type == gameBoard[x][y + 2].type and gameBoard[x][y] != empty_space:
                        target_orb = gameBoard[x][y]
                        offset = 0
                        removeSet = []
                        while gameBoard[x][y + offset].type == target_orb.type:
                            if offset == 0:
                                element.append(gameBoard[x][y].type)
                            # keep checking, in case there's more than 3 orbs in a row
                            removeSet.append((x, y + offset))
                            gameBoard[x][y + offset] = empty_space
                            if y + offset != 4:
                                offset += 1
                            else:
                                break
                        orb_remove.append(removeSet) #list of (x,y) tuples
                        num += 1
        if num == 0:
            still_have_match_orbs = False
        else:
            num = 0
    return orb_remove

def update_hp_rcv(current_hp, total_hp, recovery):
    """
    Updates the players hp bar when recovering.
    Arguments:
        current_hp(int): Current hp of player.
        total_hp(int): Total hp of player.
        recovery(int): How much hp to add to current hp.
    Returns:
        current_hp(int): returns the players current_hp after recovery.
    """
    current_hp += recovery
    if current_hp > total_hp:
        current_hp = total_hp
    return current_hp

def update_hp_dmg(current_hp, damage_taken):
    """
    Updates the players hp bar after taking damage.
    Arguments:
        current_hp(int): Current hp of player.
        damage_taken(int): Damage taken from enemy.
    Returns:
        current_hp(int): returns the players current_hp after taken damage.
    """
    current_hp -= damage_taken
    if damage_taken != 0:
        pygame.mixer.Sound.play(hit)
    return current_hp

def draw_hp(screen, current_hp, total_hp):
    """
    Updates the players hp bar after taking damage.
    Arguments:
        screen: The surface of the game to display the hp bar of player.
        current_hp(int): Current hp of player.
        total_hp(int): Total hp of player.
    """
    font = pygame.font.SysFont('arialblack', 15)
    text = font.render(str(current_hp) + '/' + str(total_hp), True, BLACK)
    percent = current_hp / total_hp
    hp_length = 450 * percent
    pygame.draw.rect(screen, (255, 255, 255), (20 , y_margin - 15, 450, 15), 0)
    pygame.draw.rect(screen, (250, 145, 243), (20 , y_margin - 15, hp_length, 15), 0)
    screen.blit(text, (window_width/2.4 , y_margin - 20))

def display_enemy(screen, stage, turn, enemy_list):
    """
    Displays the enemy on screen.
    Arguments:
        screen: The surface of the game to display the enemy.
        stage(int): Current stage.
        turn(int): The number of turns until the enemy attacks.
        enemy_list(list): List of enemies to display.
    """
    for enemy in enemy_list:
        if stage == enemy.stage:
            enemy.update(screen)

def display_background(stage, stage_list):
    """
    Displays the background based on stage.
    Argument:
        stage(int): Current stage.
        stage_list: List of stage pictures to blit onto screen.
    """
    for background in stage_list:
        if stage == background.stage:
            background.update(screen)

if __name__ == "__main__":
    main()