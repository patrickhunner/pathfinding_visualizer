import pygame
import sys
from sys import exit
import random
pygame.init()
clock = pygame.time.Clock()

class Algorithm():
    def __init__(self, done = False, board_width = 38, board_height = 30, board = [], mouse_down = False, start_placed = False, end_placed = False, found = False, go = True, starting__coord = [], end_coord = [], dijkstra_algorithm = False, a_star_algorithm = False, value = 0):
        self.board_width = board_width
        self.board_height = board_height
        self.board = board
        self.mouse_down = mouse_down
        self.start_placed = start_placed
        self.end_placed = end_placed
        self.found = found
        self.go = go
        self.starting_coord = starting__coord
        self.end_coord = end_coord
        self.SCREEN = pygame.display.set_mode((1200, 631))
        self.dijkstra_algorithm = dijkstra_algorithm
        self.a_star_algorithm = a_star_algorithm
        self.value = value
        self.done = done

    def reset_board(self):
        for i in range(0,30):
            self.board.append([])
            for j in range(0,38):
                self.board[i].append(["Infinity","not visited"])
        BLACK = (0, 0, 0)
        WHITE = (200, 200, 200)
        self.SCREEN.fill(BLACK)
        pygame.display.set_caption('Pathfinding Visualizer')
        for i in range(0,631,21):
            pygame.draw.rect(self.SCREEN,WHITE,[0,i,799,1])
        for i in range(0,801,21):
            pygame.draw.rect(self.SCREEN,WHITE,[i,0,1,630])
        title_font = pygame.font.Font(None, 60)
        directions_font = pygame.font.Font(None, 30)
        title1 = title_font.render("Pathfinding", False, 'White')
        title2 = title_font.render("Visualizer", False, 'White')
        directions = directions_font.render("Directions", False, 'White')
        place_points = directions_font.render("select start/end points and then drag for walls", False, 'White')
        rand = directions_font.render("Random wall generation: r", False, 'White')
        dijk = directions_font.render("Dijkstra: d", False, 'White')
        self.SCREEN.blit(title1, (850,50))
        self.SCREEN.blit(title2, (850,90))
        self.SCREEN.blit(directions, (850,140))
        self.SCREEN.blit(place_points,(850,190))
        self.SCREEN.blit(rand, (850,210))
        self.SCREEN.blit(dijk, (850,230))

    def set_start_end(self,coordinate,color):
        if color == 'Green':
            type_piece = 'infinity'
            visited = 'wall'
        elif color == 'Yellow':
            self.start_placed = True
            type_piece = 0
            visited = 'start'
            self.starting_coord = [[coordinate[0] // 21, coordinate[1] // 21]]
        elif color == 'Red':
            self.end_placed = True
            type_piece = 'ending'
            visited = 'ending'
            self.end_coord = [[coordinate[0] // 21, coordinate[1] // 21]]
        x_index = coordinate[0] // 21
        y_index = coordinate[1] //21
        self.board[y_index][x_index][0] = type_piece
        self.board[y_index][x_index][1] = visited
        for rows in self.board:
            for points in rows:
                if points != '.':
                    pygame.draw.rect(self.SCREEN,color,[((x_index * 21) + 1),((y_index * 21) + 1),20,20])
        pygame.display.update()

    def random_walls(self):
        for i in range(0,400):
            x = random.randint(0,37)
            y = random.randint(0,29)
            if self.board[y][x][1] == 'wall' or self.board[y][x][1] == 'not visited':
                self.board[y][x][0] = 'infinity'
                self.board[y][x][1] = 'wall'
                pygame.draw.rect(self.SCREEN,'Green',[((x * 21) + 1),((y * 21) + 1),20,20])

    def fill_in_visited(self):
        for rows in range(0,30):
            for points in range(0,38):
                # if self.dijkstra_algorithm == True:
                if self.board[rows][points][1] == 'visited':
                    x = (points * 21) + 1
                    y = (rows * 21) + 1
                    pygame.draw.rect(self.SCREEN,'White',[x,y,20,20])
                if self.board[rows][points][1] == 'retrace':
                    x = (points * 21) + 1
                    y = (rows * 21) + 1
                    pygame.draw.rect(self.SCREEN,'Orange',[x,y,20,20])
                # elif self.a_star_algorithm == True:
                #     return
        pygame.display.update()

    def retrace(self,peripheral):
        print("made it")
        print(peripheral)
        if peripheral == []:
            peripheral = self.end_coord
        new_peripherals = []
        for nodes in peripheral:
            peripheral_list = [(nodes[0] + 1,nodes[1]),(nodes[0],nodes[1] + 1),(nodes[0] - 1,nodes[1]),(nodes[0],nodes[1] - 1)]
            for poss in peripheral_list:
                print(self.board[poss[1]][poss[0]][0])
                print(self.value)
                if self.done == True:
                    return
                if poss[0] > 37 or poss[0] < 0 or poss[1] > 29 or poss[1] < 0 or self.done == True:
                    pass
                elif self.board[poss[1]][poss[0]][1] == 'start':
                    self.go = False
                    return
                elif self.board[poss[1]][poss[0]][0] == self.value:
                    self.board[poss[1]][poss[0]][1] = 'retrace'
                    self.done = True
                    if [poss[0],poss[1]] not in new_peripherals:
                        new_peripherals.append([poss[0],poss[1]])
                        break
        self.fill_in_visited()
        if self.go == True:
            self.retrace(new_peripherals)
        else:
            return

class Dijkstra(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

    def find_next_nodes(self, peripheral):
        self.new_peripherals = []
        if self.found == False:
            self.value += 1
        elif self.found == True:
            self.value -= 1
        for nodes in peripheral:
            peripheral_list = [(nodes[0] + 1,nodes[1]),(nodes[0],nodes[1] + 1),(nodes[0] - 1,nodes[1]),(nodes[0],nodes[1] - 1)]
            for poss in peripheral_list:
                if self.found == True:
                    self.retrace(self.end_coord)
                    return
                if poss[0] > 37 or poss[0] < 0 or poss[1] > 29 or poss[1] < 0:
                    pass
                elif self.board[poss[1]][poss[0]][1] == 'ending':
                    self.found = True
                    self.new_peripherals = []
                    self.new_peripherals.append([poss[0],poss[1]])
                    self.find_next_nodes(self.new_peripherals)
                    return
                elif self.board[poss[1]][poss[0]][1] == 'not visited':
                    self.board[poss[1]][poss[0]][1] = 'visited'
                    self.board[poss[1]][poss[0]][0] = self.value
                    if [poss[0],poss[1]] not in self.new_peripherals:
                        self.new_peripherals.append([poss[0],poss[1]])
        self.fill_in_visited()
        self.find_next_nodes(self.new_peripherals)

class A_star(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

    def set_board(self):
        for i in range(0,38):
            for j in range(0,30):
                heuristic = abs((i - self.starting_coord[0][0])) + abs((j - self.end_coord[0][1]))
                self.board[j][i].append(heuristic)
        starting_heuristic = abs((self.starting_coord[0][0] - self.end_coord[0][0])) + abs((self.starting_coord[0][1] - self.end_coord[0][1]))
        self.run_it()

    def find_next_nodes(self,starting):
        return

start = Algorithm()
dijk = Dijkstra()
a = A_star()
start.reset_board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                start.dijkstra_algorithm = True
                dijk.find_next_nodes(start.starting_coord)
                break
            if event.key == pygame.K_a:
                a.find_next_nodes(start.starting_coord)
                break
            if event.key == pygame.K_c:
                start = Algorithm()
                a = A_star()
                dijk = Dijkstra()
                start.reset_board()
            if event.key == pygame.K_r:
                start.random_walls()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start.end_placed == True:
                start.mouse_down = True
            elif start.end_placed == False:
                tuple = pygame.mouse.get_pos()
                if start.start_placed == False:
                    start.set_start_end(tuple,'Yellow')
                else:
                    start.set_start_end(tuple,'Red')
        elif event.type == pygame.MOUSEBUTTONUP:
            if start.end_placed == True:
                start.mouse_down = False
    if start.mouse_down == True:
        tuple = pygame.mouse.get_pos()
        if tuple[0] <= 800:
            start.set_start_end(tuple,'Green')
        if start.found == True:
            print("win")


    pygame.display.update()
