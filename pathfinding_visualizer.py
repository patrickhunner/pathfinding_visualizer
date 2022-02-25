from tracemalloc import start
from turtle import back
from xmlrpc.client import FastParser
import pygame
from sys import exit
import sys
pygame.init()

GRAY = (169,169,169)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 631
WINDOW_WIDTH = 1000
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
mouse_down = False
SCREEN.fill(BLACK)
starting_point_placed = False
ending_point_placed = False

def background():
    for i in range(0,631,21):
        pygame.draw.rect(SCREEN,WHITE,[0,i,799,1])
    for i in range(0,801,21):
        pygame.draw.rect(SCREEN,WHITE,[i,0,1,630])

def draw_border(coordinate,color):
    global starting_point_placed
    global ending_point_placed
    x_coordinate = coordinate[0] - ((coordinate[0] - 1) % 21)
    y_coordinate = coordinate[1] - ((coordinate[1] - 1) % 21)
    pygame.draw.rect(SCREEN,color,[x_coordinate,y_coordinate,20,20])
    pygame.display.update()
    if color == 'Yellow':
        starting_point_placed = True
    elif color == 'Red':
        ending_point_placed = True




while True:
    background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ending_point_placed == True:
                mouse_down = True
            elif ending_point_placed == False:
                tuple = pygame.mouse.get_pos()
                if starting_point_placed == False:
                    draw_border(tuple,'Yellow')
                else:
                    draw_border(tuple,'Red')
        elif event.type == pygame.MOUSEBUTTONUP:
            if ending_point_placed == True:
                mouse_down = False
            
                

    if mouse_down == True:
        tuple = pygame.mouse.get_pos()
        if tuple[0] <= 800:
            draw_border(tuple,'Green')


    pygame.display.update()

