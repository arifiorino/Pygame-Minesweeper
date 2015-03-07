import pygame, sys, os, random
from pygame.locals import *
from pygame import surface

pygame.init()
pygame.font.init()
numfont=pygame.font.Font(pygame.font.match_font(pygame.font.get_default_font()), 20)
#pygame.display.init()
screen = pygame.display.set_mode((500, 500))#, RESIZABLE)
pygame.display.set_caption("Minesweeper")

dimensions=(20, 20)
mines=80

places=[0]*(dimensions[0]*dimensions[1])
screen.fill((0, 255, 0))
for i in range(mines):
    r=random.randint(0, len(places)-1)
    while r==1:
        r=random.randint(0, len(places))
    places[r]=1
    
def check(x, y):
    global mines
    a=0
    if [x-1, y-1] in mines:
        a+=1
    if [x-1, y] in mines:
        a+=1
    if [x-1, y+1] in mines:
        a+=1
    if [x, y-1] in mines:
        a+=1
    if [x, y+1] in mines:
        a+=1
    if [x+1, y-1] in mines:
        a+=1
    if [x+1, y] in mines:
        a+=1
    if [x+1, y+1] in mines:
        a+=1
    
    return a
    
    
    
c=-1
mines=[]
for x in range(dimensions[0]):
    for y in range(dimensions[1]):
        c+=1
        if places[c]:
            mines.append([x, y])
    
mrect=pygame.Rect(0, 0, screen.get_width()/dimensions[0], screen.get_height()/dimensions[1])

def endall():
    pygame.quit()
    sys.exit()


while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            endall()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for x in range(dimensions[0]):
                for y in range(dimensions[1]):
                    if pos[0]>int(x*(screen.get_width()/dimensions[0])) and pos[0]<int((x+1)*(screen.get_width()/dimensions[0])) and pos[1]>int(y*(screen.get_height()/dimensions[1])) and pos[1]<int((y+1)*(screen.get_height()/dimensions[1])):
                        if [x, y] in mines:
                            endall()
                        else:
                            a=check(x,y)
                            ais=[a]
                            aiscoor=[[x,y]]
                            secaiscoor=[]
                            xx, yy=x, y
                            while len(aiscoor)>=1:
                                for i in aiscoor:
                                    aa=0
                                    if check(i[0]-1, i[1]-1)==0:
                                        aiscoor.append(i[0]-1, i[1]-1)
                                    if check(i[0]-1, i[1])==0:
                                        aiscoor.append(i[0]-1, i[1])
                                    if check(i[0]-1, i[1]+1)==0:
                                        aiscoor.append(i[0]-1, i[1]+1)
                                    if check(i[0], i[1]-1)==0:
                                        aiscoor.append(i[0], i[1]-1)
                                    if check(i[0], i[1]+1)==0:
                                        aiscoor.append(i[0], i[1]+1)
                                    if check(i[0]+1, i[1]-1)==0:
                                        aiscoor.append(i[0]+1, i[1]-1)
                                    if check(i[0]+1, i[1])==0:
                                        aiscoor.append(i[0]+1, i[1])
                                    if check(i[0]+1, i[1]+1)==0:
                                        aiscoor.append(i[0]+1, i[1]+1)
                                    secaiscoor.append(i)
                                
                                    
                                
                            cc=-1
                            for xv in range(dimensions[0]):
                                for yv in range(dimensions[1]):
                                    cc+=1
                                    if [xv, yv]==[x, y]:
                                        places[cc]=str(a)
                            
    c=-1
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            c+=1
            mrect.x=int(x*(screen.get_width()/dimensions[0]))
            mrect.y=int(y*(screen.get_height()/dimensions[1]))
            if places[c]==0 or places[c]==1:
                screen.fill((0, 0, 0), mrect)
            elif places[c]==str(places[c]):
                screen.fill((255, 255, 255), mrect)
                num=numfont.render(places[c], 1, (0, 0, 0))
                numrect=num.get_rect()
                numrect.x=int(x*(screen.get_width()/dimensions[0]))
                numrect.y=int(y*(screen.get_height()/dimensions[1]))
                screen.blit(num, numrect.center)
                
            pygame.draw.rect(screen, (128, 128, 128), mrect, 2)
    pygame.display.update()