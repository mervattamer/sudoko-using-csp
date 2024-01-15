import pygame
import time
from merv_input_gui import Grid
import suduko_main
background_image = pygame.image.load('game_bg.jpg')

def main():
    pygame.font.init()
    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku")
    b=[[0 for _ in range(9)] for _ in range(9)]
    board = Grid(b, 9, 9, 540, 540, win)
    key = None
    run = True
    while run:
        #win.fill((255,255,255))
        win.blit(background_image, (0, 0))
        board.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    grid_to_solve = board.validate_board()
                    if grid_to_solve != None:
                        pygame.quit()
                        print (grid_to_solve)
                        suduko_main.main_gui(grid_to_solve)
                        run = False

                    #pass array to suduko main
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        if board.selected and key is not None:
            board.sketch(key)

        

    pygame.quit()
#main()