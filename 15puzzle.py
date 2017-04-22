import random
import pygame
import os
import Tkinter as tk
import tkFileDialog
from PIL import Image

def subsection(i,j):
    a = board[i][j][0]
    b = board[i][j][1]
    return pygame.Rect(w*a/size, h*b/size, w/size, h/size)

def out():
    screen.fill(white)
    for i in range(size):
        for j in range(size):
            if board[i][j] != " ":
                screen.blit(img, (w*i/size,h*j/size), subsection(i,j))
    screen.blit(pygame.transform.scale(img,(scaledw,scaledh)), (w+40,40))
    screen.blit(font.render("Moves: " + str(moves), 1, black), (w+40,80+scaledh))
    pygame.display.flip()

def solved():
    for i in range(size):
        for j in range(size):
            if board[i][j] != solution[i][j]:
                return False
    return True

def read():
    image = Image.open(filename)
    if image.format == "PNG":
        s = "qwertyuiopasdfghjklzxcvbnm7894561230,./;'-=<>?:_+!@#$%^&*()\" \\"
        px = list(image.getdata())
        
        m = ""
        for i in range(len(px)):
            c = 16*(px[i][0] % 4) + 4*(px[i][1] % 4) + (px[i][2] % 4) - 1
            if c == -1:
                break
            if c >= 0 and c < len(s):
                m += s[c]
        print m

def write():
    image = Image.open(filename)
    if image.format == "PNG":
        s = "qwertyuiopasdfghjklzxcvbnm7894561230,./;'-=<>?:_+!@#$%^&*()\" \\"
        px = list(image.getdata())

        message = raw_input('Message? ')
        if image.size[0] * image.size[1] + 1 >= len(message) and len(px) > 0:
            for i in range(len(message) + 1):
                if i == len(px):
                    break
                if i < len(message):
                    p = [0,0,0]
                    
                    index = 0
                    for j in range(len(s)):
                        if s[j] == message[i]:
                            index = j
                            break
                    if s[index] != message[i]:
                        index = 0
                    else:
                        index += 1
                    
                    p[0] = px[i][0] - (px[i][0] % 4) + (index / 16)
                    p[1] = px[i][1] - (px[i][1] % 4) + ((index / 4) % 4)
                    p[2] = px[i][2] - (px[i][2] % 4) + (index % 4)
                    px[i] = (p[0],p[1],p[2])
                else:
                    p = [0,0,0]
                    p[0] = px[i][0] - (px[i][0] % 4)
                    p[1] = px[i][1] - (px[i][1] % 4)
                    p[2] = px[i][2] - (px[i][2] % 4)
                    px[i] = (p[0],p[1],p[2])
        newimg = Image.new(image.mode, image.size)
        newimg.putdata(px)
        newimg.save(filename)

size = 0
while size < 3:
    size = int(raw_input('Size? '))
pygame.init()
font = pygame.font.SysFont("Lucida Console", 32)

root = tk.Tk()
root.withdraw()
filename = tkFileDialog.askopenfilename()
img = pygame.image.load(filename)
w = img.get_width()
h = img.get_height()
scaled = float(320)/w
scaledw = 320
scaledh = int(h*scaled)

os.environ['SDL_VIDEO_WINDOW_POS'] = '30,30'
screen = pygame.display.set_mode((w + 400,h))
pygame.display.set_caption("15-Puzzle")
white = (255,255,255)
black = (0,0,0)
screen.fill(white)

moves = -1
x = size - 1
y = size - 1
solution = [[0] * size for i in range(size)]
board = [[0] * size for i in range(size)]
for i in range(size):
    for j in range(size):
        solution[i][j] = (i,j)
        board[i][j] = (i,j)
solution[x][y] = " "
board[x][y] = " "
for i in range(200):
    e = random.randrange(size)
    diffx = 0
    diffy = 0
    if e == 0 and y < size-1:
        diffy = 1
    elif e == 1 and y > 0:
        diffy = -1
    elif e == 2 and x < size-1:
        diffx = 1
    elif x > 0:
        diffx = -1
    if diffx !=0 or diffy != 0:
        board[x][y] = board[x+diffx][y+diffy]
        board[x+diffx][y+diffy] = " "
        x += diffx
        y += diffy

moved = True
done = False
upcnt = 0
dncnt = 0
while not done:
    if upcnt == 5:
        upcnt = 0
        write()
    if dncnt == 5:
        dncnt = 0
        read()
    if moved:
        moves += 1
        out()
        moved = False
        
    if solved():
        screen.blit(font.render("Solved!", 1, black), (w+40,140+scaledh))
        pygame.display.flip()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        os._exit(0)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            os._exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                dncnt += 1
            else:
                dncnt = 0
            if event.key == pygame.K_UP:
                upcnt += 1
            else:
                upcnt = 0
            
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                os._exit(0)
            if event.key == pygame.K_DOWN and y != 0:
                board[x][y] = board[x][y-1]
                y -= 1
                board[x][y] = " "
                moved = True
            if event.key == pygame.K_UP and y != size-1:
                board[x][y] = board[x][y+1]
                y += 1
                board[x][y] = " "
                moved = True
            if event.key == pygame.K_LEFT and x != size-1:
                board[x][y] = board[x+1][y]
                x += 1
                board[x][y] = " "
                moved = True
            if event.key == pygame.K_RIGHT and x != 0:
                board[x][y] = board[x-1][y]
                x -= 1
                board[x][y] = " "
                moved = True
