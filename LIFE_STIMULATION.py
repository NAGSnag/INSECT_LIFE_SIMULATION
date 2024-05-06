import pygame
import random
import numpy as np

width,height=1500,800
win=pygame.display.set_mode((width,height))
fps=60




class w:
    def __init__(self):
        self.w=width
        self.h=height
        self.x=self.w//15
        self.y=self.h//8

    def clickpos(self,pos):
        x,y = pos
        row = x // (self.w // self.x)
        col = y // (self.h // self.y)
        return row,col

    def draw(self, x,y):
        for i in range(100):
            for j in range(100):
                if self.map[i][j] == 1:
                    pygame.draw.rect(win, (255, 255, 0),pygame.Rect(y*15, x *8, 10,10))



class creature:
    def __init__(self,x,y,color,id):
        self.x=x
        self.y=y
        self.color=color
        self.id=id
    def draw(self):
        pygame.draw.rect(win,self.color,pygame.Rect(self.x*15,self.y*8,5,10))
        pygame.draw.rect(win,(255,255,255),pygame.Rect(self.x*15,self.y*8+2,10,5))
    def scan(self):

        for i in world.map:
            for j in i:
                if j != 0 and j != 1:
                    if j.id == "m":
                        if world.map[j.x + 1][j.y + 1] or world.map[j.x - 1][j.y + 1] or world.map[j.x + 1][j.y - 1] or \
                                world.map[j.x - 1][j.y - 1] \
                                or world.map[j.x][j.y + 1] or world.map[j.x + 1][j.y] or world.map[j.x - 1][j.y] or \
                                world.map[j.x][j.y*222 - 1]:
                            print('e')


    def act(self):
        self.x+=1
        self.y+=1

world=w()

def main():
    clock=pygame.time.Clock()
    run=True
    creature_deck_a=[]
    creature_deck_b=[]
    for i in range(60):
        a=creature(random.randint(0,99),random.randint(0,99),(255,50,200),i)
        creature_deck_a.append(a)
        world.map[a.x][a.y] = a
        b=creature(random.randint(0,99),random.randint(0,99),(50,255,25),i)
        creature_deck_b.append(b)
        world.map[b.x][b.y] = b
    dumchar=creature(random.randint(0,99),random.randint(0,99),(255,255,255),"m")
    x,y=dumchar.x,dumchar.y
    world.map[dumchar.x][dumchar.y]=dumchar

    while run:
        win.fill((0, 0, 0))

        clock.tick(fps)
        pygame.display.set_caption(f"LIFE_STIMuLATION  {round(clock.get_fps())}")

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            key = pygame.key.get_pressed()
            if key == pygame.K_ESCAPE:
                run = False
            if key[pygame.K_w]:
                obj=world.map[x][y]
                obj.y-=1
                world.map[x][y-1]=obj
            if key[pygame.K_s]:
                for i in world.map:
                    for j in i:
                        if j!=0 and j!=1:
                            if j.id=="m":
                                if world.map[j.x+1][j.y+1] or world.map[j.x-1][j.y+1] or world.map[j.x+1][j.y-1] or world.map[j.x-1][j.y-1]\
                                        or world.map[j.x][j.y+1] or world.map[j.x+1][j.y] or world.map[j.x-1][j.y] or world.map[j.x][j.y-1]:
                                    print('exist')


            left, middle, right = pygame.mouse.get_pressed()
            if left:
                try:
                    pos = pygame.mouse.get_pos()
                    row,col=world.clickpos(pos)
                    world.map[col][row]=1
                    world.draw(col,row)
                except Exception as e:pass


        for i in world.map:
            for j in i:
                if j!=0 and j!=1:
                    j.scan()
                    j.draw()



        pygame.display.update()
    pygame.quit()

if __name__=='__main__':
    main()