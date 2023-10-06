
import math
import sys
import numpy as np
import pygame
import sys
import pygame_gui



grid = \
    [[1, 1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 0, 0, 0, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 1, 1, 1]]

def interface():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (128,128,128)

    WIDTH = 93
    HEIGHT = 93
    MARGIN = 2

    WINDOWS_SIZE = [760, 830]

    pygame.init()
    screen = pygame.display.set_mode(WINDOWS_SIZE)
    pygame.display.set_caption("Map Grid Creator")
    smallfont = pygame.font.Font(None, 35)
    text = smallfont.render('Jugar', True, WHITE)


    close = False
    clock = pygame.time.Clock()
    pygame.init()
    mouse_pressed = False
    num = 0
    while not close:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                close = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pressed = True
                num = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pressed = True
                num = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
            pos = pygame.mouse.get_pos()

            # Click el boton de OK
            if mouse_pressed and 320 <= pos[0] <= 320 + 140 and 760 <= pos[1] <= 760 + 60:
                close = True
            # Click en las celdas
            elif mouse_pressed and 0<pos[0]<760 and 0<pos[1]<830 :
                close = False
                # User clicks the mouse. Get the position
                # Change the x/y screen coordinates to grid coordinates

                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                # Set that location to one
                try:
                    grid[row][column] = num
                except IndexError:
                    pass

        # Draws button
        pygame.draw.rect(screen, GREEN, [320, 760, 140, 60])
        screen.blit(text, (345, 780))



        # Draw the grid
        for row in range(8):
            for column in range(8):

                if grid[row][column] == 1:
                    pygame.draw.rect(screen,
                                     WHITE,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])
                else:
                    pygame.draw.rect(screen,
                                     GREY,
                                     [(MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT])
        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

    map = []
    for i in range(8):
        for j in range(8):
            map.append(grid[i][j])
    return map


def main():
    interface()



if "__main__" == __name__:

    main()
