import pygame
import random
import numpy as np
import os
import math

width,height=1500,800
win=pygame.display.set_mode((width,height))
fps=60
ball_width,ball_height=20,22


background=pygame.image.load("D:\\pyprogs\\stimulation\\lifestimulation_project\\Quantum-Dark-Matter-Multiverse-String-Theory-46095018-1.png")
background=pygame.transform.scale(background,(width,height))

background = background.convert_alpha()
transparency = 128
background.fill((255, 255, 255, transparency), special_flags=pygame.BLEND_RGBA_MULT)
path= os. getcwd()

brownsprite=[]
os.chdir('./spyder sprite 2')
for i in os.listdir():
    img = pygame.image.load(i)
    img = pygame.transform.scale(img, (40,40))
    #img = pygame.transform.rotate(img,90)
    brownsprite.append(img)
os.chdir(path)

flysprite=[]
os.chdir('./spyder sprite 1')
for i in os.listdir():
    img = pygame.image.load(i)
    img = pygame.transform.scale(img, (40,40))
    img = pygame.transform.rotate(img,180)
    flysprite.append(img)
os.chdir(path)


blacksprite=[]
os.chdir('./spyder sprite 3')
for i in os.listdir():
    img = pygame.image.load(i)
    img = pygame.transform.scale(img, (40,40))
    #img = pygame.transform.rotate(img,90)
    blacksprite.append(img)
os.chdir(path)
greensprite=[]
os.chdir('./spyder sprite 4')
for i in os.listdir():
    img = pygame.image.load(i)
    img = pygame.transform.scale(img, (40,40))
    #img = pygame.transform.rotate(img,90)
    greensprite.append(img)
os.chdir(path)
class w:
    def __init__(self):
        self.w=width
        self.h=height
        self.x=self.w//15
        self.y=self.h//8

    def draw(self, x,y):
        self.obj=pygame.draw.rect(win, (255, 255, 0),pygame.Rect(y*15, x *8, 10,10))



class creature:
    def __init__(self,x,y,color,id,team):
        self.x=x
        self.y=y
        self.color=color
        self.id=(id,team)
        self.health=20
        self.hunger=random.randint(0,20)
        self.anger=False
        self.strength=random.randint(0,10)
        self.carry=False
        self.rect=0
        self.x_direction=1
        self.speed_factor =0.8
        self.y_direction=1
        self.t=0
        self.split=0
        self.rect_pos = pygame.Vector2(self.x, self.y)
        self.enemy_target=0
        self.bulets=10
        self.shoote=False
        self.angle=0
        self.current_sprite=0
        if self.id[1]=="A":
            self.sprites=brownsprite
        elif self.id[1]=='B':
            self.sprites=greensprite
        elif self.id[1]=='C':
            self.sprites=flysprite
        else:
            self.sprites = blacksprite

    def draw(self):
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0

        print(self.angle)
        if self.hunger>=10:

            self.image=pygame.transform.rotate(self.sprites[0], -self.angle)
        else:
            self.image = self.sprites[int(self.current_sprite)]
            self.image = pygame.transform.rotate(self.sprites[int(self.current_sprite)], -self.angle)
        self.obj=win.blit(self.image,(self.x,self.y))
        self.current_sprite += 0.2


    def scanfood(self):
        global food_deck
        dist=[]
        for i in food_deck:
            if i.present==True and i.x>=1 and i.y>=1 and i.x<=1500 and i.y<=800:
                dist.append((pygame.math.Vector2(self.x,self.y).distance_to((i.x,i.y)),i.id))
        m=min(dist,key=lambda x:x[0])
        return m
    def move(self,pos):
        global food_deck
        try:

            if self.x>=1 and self.y>=1 and self.x<=1500 and self.y<=800:
                posx,posy=food_deck[pos[1]].x,food_deck[pos[1]].y
                target_position = pygame.Vector2(posx,posy)
                radians = math.atan2(posx- self.x, posy - self.y)
                self.angle = math.degrees(radians) * -1
                direction = target_position - self.rect_pos
                direction.normalize_ip()
                self.rect_pos += direction * self.speed_factor
                self.x = self.rect_pos.x
                self.y = self.rect_pos.y
            else:self.t=self.scanfood()

        except Exception:pass
    def settarget(self):
        global char_deck
        diste=[]
        for i in char_deck:
            if self.id[1]!=i.id[1]:
                diste.append((pygame.math.Vector2(self.x, self.y).distance_to((i.x, i.y)), i.id))
        t=min(diste,key=lambda x:x[0])
        return t

    def shoot(self,target):
        global blist, char_deck,count
        if count%25==0:
            if(self.bulets!=0):
                tx,ty=0,0
                for i in char_deck:
                    if i.id[0]==target[1][0] and i.id[1]==target[1][1]:
                        tx,ty=i.x,i.y
                b=bullet(self.x,self.y-5,tx,ty)
                blist.append(b)
            self.bulets-=1

    def reporduce(self):
        global char_deck
        char_deck.append(creature(self.x+10,self.y-10,self.color,len(char_deck)+1,self.id[1]))
    def act(self):
        try:
            if self.health<10:
                self.anger=True
            elif self.hunger >15:
                self.hunger = False
                self.anger=False

            if self.hunger<10:
                self.move(self.scanfood())
                if self.hunger<7:
                    self.anger=True
            if self.anger:
                self.shoote=True
                self.anger=False
            if self.split==3:
                self.split=0
                self.reporduce()
            if self.shoote:
                self.shoot(self.settarget())
                self.shoote=False


        except Exception as e:
            print("in act",e)

class bullet:
    def __init__(self,x,y,tx,ty):
        self.x = x
        self.y = y
        self.speed = 10
        self.cooldown = 500
        dx = tx - self.x
        dy = ty - self.y
        self.angle = math.atan2(dx, dy)
        self.present=True

    def move(self):
        self.bul = pygame.draw.rect(win,'blue', (self.x, self.y, 3,4))
        self.mvx = math.sin(self.angle) * self.speed
        self.mvy = math.cos(self.angle) * self.speed
        self.x += self.mvx
        self.y += self.mvy
        if self.x<0 or self.x>1500 or  self.y<0 or self.y>800:
            self.present=False


class food:
    def __init__(self,id,x1,x2):
        self.x=random.randint(x1,x2)
        self.y=random.randint(5,780)
        self.id=id
        self.present=True
    def draw(self):
        self.obj=pygame.draw.rect(win,(140,200,1),(self.x,self.y,5,5))

def foodgen(r=250):
    for i in range(r//2):
        obj=food(i,10,725)
        food_deck.append(obj)
    for i in range(r // 2):
        obj=food(i,725,1480)
        food_deck.append(obj)


world=w()
food_deck = []
char_deck=[]
blist=[]
count=0
def main():
    clock=pygame.time.Clock()
    run=True
    global count


    for i in range(8):
        char_deck.append(creature(random.randint(0,1450),random.randint(0,750),(255,0,0),i,"A"))
        char_deck.append(creature(random.randint(0,1450),random.randint(0,750),(0,0,255),i,"B"))
        char_deck.append(creature(random.randint(0,1450),random.randint(0,750),(0,255,0),i,"C"))
        char_deck.append(creature(random.randint(0,1450),random.randint(0,750),(0,255,0),i,"D"))
    foodgen()

    while run:
        if len(food_deck)==0:
            foodgen(10)
        if count<=100:
            count+=1
        else:count=0


        win.fill((200,200,200))
        #win.blit(background, (0, 0, width, height))

        clock.tick(fps)
        pygame.display.set_caption(f"LIFE_STIMuLATION  {round(clock.get_fps())}")
        for i in range(len(food_deck)):
            food_deck[i].id=i
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            key = pygame.key.get_pressed()
            if key == pygame.K_ESCAPE:
                run = False
            if key[pygame.K_s]:
               # print(char_deck)
                for i in char_deck:
                    i.scanfood()

            left, middle, right = pygame.mouse.get_pressed()
            if left:
                try:
                    pos = pygame.mouse.get_pos()
                    f=food(len(food_deck)+1,pos[0],pos[0])
                    f.x=pos[0]
                    f.y=pos[1]
                    food_deck.append(f)


                except Exception as e:pass
        for i in char_deck:
            i.draw()
            i.act()
        for i in food_deck:
            i.draw()
        for i in range(len(blist)):
            if blist[i].present:
                blist[i].move()



        ##collition
        # for i in food_deck:
        #     for j in char_deck:
        #         if i.obj.colliderect(j.obj):
        #             j.hunger+=5
        #             food_deck.pop(i.id)
        try:
            for i in range(len(food_deck)):
                for j in range(len(char_deck)):
                    if food_deck[i].obj.colliderect(char_deck[j].obj):
                        char_deck[j].hunger += 7
                        char_deck[j].health += 10
                        char_deck[j].bulets += 5
                        char_deck[j].t=0
                        char_deck[j].split+=1
                        food_deck[i].present=False
                        break
            for i in range(len(blist)):
                for j in range(len(char_deck)):
                    if blist[i].bul.colliderect(char_deck[j].obj):
                        char_deck[j].health-=0.2
                        # blist.pop(i)








        except Exception as e:print(e,'in colletion')

        for item in food_deck:
            if item.present == False:
                food_deck.remove(item)


        for i in char_deck:
            i.hunger-=0.01
            if i.health<=0:
                char_deck.remove(i)
                dead=food(len(food_deck)+1,0,0)
                dead.x=i.x
                dead.y=i.y
                food_deck.append(dead)


        pygame.display.update()
    pygame.quit()

if __name__=='__main__':
    main()