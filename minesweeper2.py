import pygame, sys, os, random, time
from pygame.locals import *
from pygame import surface
from collections import OrderedDict
pygame.init()
pygame.font.init()
numfont=pygame.font.Font(pygame.font.match_font(pygame.font.get_default_font()), 20)

Inp=input("'e' for easy, 'm' for medium, 'h' for hard: ")
if Inp=='e' or Inp=='easy':
    dimensions=(9, 9)
    mines=10
if Inp=='m' or Inp=='medium' or Inp=='':
    dimensions=(16, 16)
    mines=40
if Inp=='h' or Inp=='hard':
    dimensions=(30, 16)
    mines=99

screen = pygame.display.set_mode((dimensions[0]*25, dimensions[1]*25))
pygame.display.set_caption("Minesweeper")

places=[0]*(dimensions[0]*dimensions[1])

for i in range(mines):
    r=random.randint(0, len(places)-1)
    while places[r]==1:
        r=random.randint(0, len(places)-1)
    places[r]=1
    
def check(x, y):
    global mines, dimensions
    a=0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if [x+dx, y+dy] in mines:
                a+=1   
    return a
def wcheck(x, y):
    global mines, dimensions
    if x<0 or y<0 or x>=dimensions[0] or y>=dimensions[1]:
        a=8
    else:
        a=0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if ([x+dx, y+dy] in mines):
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
markr=pygame.Rect(0, 0, (screen.get_width()/dimensions[0])/2, (screen.get_height()/dimensions[1])/2)
def endall(s):
    
    global mines, dimensions
    mmm=list(mines)
    random.shuffle(mmm)
    mmm.append(mmm[0])
    mmm[0]=s
    mrect=pygame.Rect(0, 0, screen.get_width()/dimensions[0], screen.get_height()/dimensions[1])
    timew=.1
    timem=.005
    c=-1
    for m in mmm:
        c+=1
        mrect.x=int(m[0]*(screen.get_width()/dimensions[0]))
        mrect.y=int(m[1]*(screen.get_height()/dimensions[1]))
        if [x, y] in mmm:
            screen.fill((255, 0, 0), mrect)
            pygame.draw.rect(screen, (128, 128, 128), mrect, 2)
            pygame.display.update()
            if timew>0:
                time.sleep(timew)
            timew-=timem
    time.sleep(1)
    pygame.quit()
    sys.exit()
def returnzerosaround(d):
    x, y=d[0], d[1]
    newzeros=[]
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if [dx,dy]!=[0,0] and wcheck(x+dx,y+dy)==0:
                newzeros.append([x+dx, y+dy])
    return newzeros
def around(d):
    [x, y]=d
    a=[]
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if [dx,dy]!=[0,0]:
                a.append([x+dx,y+dy])
    return a
def sfrompos(pos):
    global dimensions
    cx=screen.get_width()/dimensions[0]
    dx=0
    [x,y]=pos
    while x>0:
        dx+=1
        x-=cx
    cy=screen.get_height()/dimensions[1]
    dy=0
    while y>0:
        dy+=1
        y-=cy
    return [dx-1, dy-1]
def win():
    global totaltime
    print("\nYou won in ", end='')
    Min=0
    sec=totaltime.get_ticks()/1000
    while 1:
        sec-=60
        Min+=1
        if sec<0:
            sec+=60
            Min-=1
            break
    if Min>0 and sec>0:
        print(round(Min,2), 'minute'+(['', 's'][int(Min!=1)]),'and', round(sec,2), 'second'+(['.', 's.'][int(sec!=1)]))
    if Min>0 and sec<=0:
        print(round(Min,2), 'minute'+(['.', 's.'][int(Min!=1)]))
    if Min<=0 and sec>0:
        print(round(sec,2), 'second'+(['.', 's.'][int(sec!=1)]))
		
    pygame.quit()
    sys.exit()
def color(n):
    c=(0, 0, 0)
    if n == 1:
        c=(65, 80, 190)
    if n == 2:
        c=(35, 100, 0)
    if n == 3:
        c=(175, 5, 10)
    if n == 4:
        c=(0, 0, 125)
    if n == 5:
        c=(125, 0, 0)
    if n == 6:
        c=(15, 135, 125)
    if n == 7:
        c=(200, 0, 200)
    if n == 8:
        c=(255, 220, 60)
    return c
marks=[0]*(dimensions[0]*dimensions[1])
totaltime=pygame.time
totaltime.get_ticks()
firstclick=1
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for x in range(dimensions[0]):
                for y in range(dimensions[1]):
                    if pos[0]>int(x*(screen.get_width()/dimensions[0])) and pos[0]<int((x+1)*(screen.get_width()/dimensions[0])) and pos[1]>int(y*(screen.get_height()/dimensions[1])) and pos[1]<int((y+1)*(screen.get_height()/dimensions[1])):

                        if firstclick and ([x, y] in mines):
                            firstclick=0
                            mines[mines.index([x, y])] = [random.randint(0, dimensions[0]-1), random.randint(0, dimensions[1]-1)]
                            while [x, y] in mines:
                                mines[mines.index([x, y])] = [random.randint(0, dimensions[0]-1), random.randint(0, dimensions[1]-1)]
                                
                        elif [x, y] in mines:
                            endall([x, y])
                        
                        else:
                            if check(x, y)==0 and len(returnzerosaround([x, y]))>=1:
                                allz=[[x, y]]
                                onestocheck=allz
                                tbadded=[]
                                addedz=1
                                while addedz>=1:
                                    addedz=0
                                    tbadded=[]
                                    for i in onestocheck:
                                        tbadded.extend(returnzerosaround(i))
                                    onestocheck=[]
                                    for i in tbadded:
                                        if (not (i in allz)):
                                            onestocheck.append(i)
                                            allz.append(i)
                                            addedz+=1
                                next20=[]
                                for i in allz:
                                    for g in around(i):
                                        if not (g in allz):
                                            next20.append(g)
                                
                                cc=-1
                                for xv in range(dimensions[0]):
                                    for yv in range(dimensions[1]):
                                        cc+=1
                                            
                                        if ([xv, yv] in allz):
                                            places[cc]='0'
                                        elif [xv, yv] in next20:
                                            places[cc]=str(check(xv, yv))
                            elif check(x, y)==0:
                                cc=-1
                                for xv in range(dimensions[0]):
                                    for yv in range(dimensions[1]):

                                        cc+=1
                                        if [xv, yv] in around([x, y]):
                                            places[cc]=str(a)
                            else:
                                a=check(x, y)
                                cc=-1
                                for xv in range(dimensions[0]):
                                    for yv in range(dimensions[1]):

                                        cc+=1
                                        if [xv, yv]==[x, y]:
                                            places[cc]=str(a)
        if pygame.mouse.get_pressed()[2]:
            #print(2)
            pos = pygame.mouse.get_pos()
            pos=sfrompos(pos)
            cc=-1
            for xv in range(dimensions[0]):
                for yv in range(dimensions[1]):
                    cc+=1
                    if [xv, yv]==list(pos):
                        if places[cc]==0 or places[cc]==1:
                            if marks[cc]:
                                marks[cc]=0
                            else:
                                marks[cc]=1
    c=-1
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            c+=1
            mrect.x=int(x*(screen.get_width()/dimensions[0]))
            mrect.y=int(y*(screen.get_height()/dimensions[1]))
            if places[c]==0 or places[c]==1:
                screen.fill((0, 0, 0), mrect)
            elif places[c]==str(places[c]) and places[c]!='0':
                screen.fill((255, 255, 255), mrect)
                num=numfont.render(places[c], 1, color(int(places[c])))
                numrect=num.get_rect()
                numrect.center=mrect.center
                screen.blit(num, numrect)
            elif places[c]=='0':
                screen.fill((255, 255, 255), mrect)
            if marks[c]:
                markr.center=mrect.center
                screen.fill((0, 0, 255), markr)
            pygame.draw.rect(screen, (128, 128, 128), mrect, 2)

    c=-1
    tapped=0
    for x in range(dimensions[0]):
        for y in range(dimensions[1]):
            c+=1
            if places[c]==str(places[c]):
                tapped+=1
    if tapped>=(dimensions[0]*dimensions[1])-len(mines):
        win()
            
    pygame.display.update()
