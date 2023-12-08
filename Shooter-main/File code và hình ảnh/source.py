
import pygame
from pygame.locals import * 
import random 
import os


pygame.init()
clock = pygame.time.Clock()

#Screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
tile_size = SCREEN_HEIGHT//10
FPS = 60
SCROLL_THRESH = 200
SCREEN_SCROLL = 0
BG_SCROLL = 0

score = 0

#Char Variable
moving_left = False
moving_right = False
moving_up = False
moving_down = False
jump = False
shoot = False
GRAVITY = 1

#bullet
bullet_w = 70
bullet_h = 50

#Button
button_scales = 0.9

#enemy_variable
enemy_jump = False
enemy_moving_left = True
enemy_moving_right = not enemy_moving_left

win_image = pygame.image.load(r'win.jpg')

#Definite font and text
font = pygame.font.SysFont("Furuta", 50)
def draw_text(x,y,content,color):
    text = font.render(content,True,color)
    screen.blit(text,(x,y))

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Shoot")
def draw_bg():
    bg = pygame.image.load("background.png")
    background = pygame.transform.scale(bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
    for start_index in range (5):
        screen.blit(background,(start_index*SCREEN_WIDTH - BG_SCROLL,0))
'''Button'''
start_img = pygame.image.load("ac482875f47f35216c6e.jpg").convert_alpha()
exit_img = pygame.image.load("782a8d17511d9043c90c.jpg").convert_alpha()


class Button:
    def __init__(self,x,y,image,scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image,(int(self.width*scale),(int(self.height*scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        #Get mouse position
        pos = pygame.mouse.get_pos()
        
        #Check if mouse position is on the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #Mouse press [0] is left press, [1] is middle press, [2] is  right press
                self.clicked = True
                action = True
        screen.blit(self.image,self.rect)
        return action

    

start_button = Button((SCREEN_WIDTH/6),300,start_img,button_scales)
exit_button = Button((SCREEN_WIDTH*3/5),300,exit_img,button_scales)		

'''Character area'''
class soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed,char_type):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.x = x 
        self.y = y
        self.width = tile_size
        self.height = tile_size
        self.shoot_cooldown = 1
        self.health = 100
        self.max_health = self.health
        self.speed = speed
        self.flip = False
        self.direction = 1
        self.animation_list = []
        self.frame_index = 0
        self.currAction = 0
        self.update_ani = pygame.time.get_ticks()
        self.vel_y = 0
        self.in_air = True
        self.char_type = char_type.upper()
        
        #Enemy specific variable
        self.vision = pygame.Rect(0,0,SCREEN_WIDTH//2,20)
        self.move_counter = 0 
        self.idling = False
        self.idling_counter = 0
        self.enemy_moving_left = False
        self.enemy_moving_right = True
        self.enemy_jump = False
        if self.char_type == 'PLAYER':
            self.num_type = 3
        else:
            self.num_type = 1 
        behaviours = ["Idle","Walking","Attack","Dying"]
        for behaviour in behaviours:
            temp_lst = []
            num_img = len(os.listdir(r'{}\{}'.format(self.char_type,behaviour)))
            for img_index in range (num_img):
                if img_index <10:
                    img = pygame.image.load(r'{}\{}\Wraith_0{}_{}_00{}.png'.format(self.char_type,behaviour,self.num_type,behaviour,img_index)).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                    temp_lst.append(img)
                else:
                    img = pygame.image.load(r'{}\{}\Wraith_0{}_{}_0{}.png'.format(self.char_type,behaviour,self.num_type,behaviour,img_index)).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width()*scale), int(img.get_height()*scale)))
                    temp_lst.append(img)
            self.animation_list.append(temp_lst)
        
        
        
        #animation_list: 0 is idle, 1 is walking, 2 is attacking, 3 is dying
        
        self.image = self.animation_list[self.currAction][self.frame_index]
# =============================================================================
#         self.rect = self.image.get_rect()
#         self.rect.center = (x,y)
# =============================================================================
                
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.rect.center = (x,y)
        self.scale = scale
    
    
    
    def draw(self):
        

        #pygame.draw.rect(screen, (255,255,255), self.rect)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
    
    def shoot(self):    
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 10
            bullet = Bullet(self.rect.centerx + int(((self.rect.size[0] +20)* self.direction )), self.rect.centery, self.direction)
            bullet_group.add(bullet)
    
    #Check if the soldier is alive
    def check_alive(self):
        if self.health<=0:
            self.alive = False
            self.update_action(3)
            
    
    def update(self):
       self.update_animation()
       #Update cooldown
       if self.shoot_cooldown > 0:
           self.shoot_cooldown -= 1      

    def update_animation(self):
        self.check_alive()
        self.image = self.animation_list[self.currAction][self.frame_index]
        UPDATE_TIME = 100
        if self.frame_index == 14 and self.currAction == 3:
            pass
        elif pygame.time.get_ticks() - self.update_ani >= UPDATE_TIME:
            self.update_ani = pygame.time.get_ticks()
            self.frame_index += 1
        elif self.frame_index == (len(self.animation_list[self.currAction]) - 1 ):
            self.frame_index = 0
            
    #Check if the new action is different form the old one
    def update_action(self,new_action):
        if self.currAction != new_action:
            self.currAction = new_action
            self.update_ani = pygame.time.get_ticks()
            self.frame_index = 0
    
    def robot(self):
        
        if self.alive and player.alive:
            if self.idling == False and random.randint(1,200)==1:
                self.idling = True
                self.idling_counter = 20 
                self.update_action(0)
            #Check if the enemy near the player
            if self.vision.colliderect(player.rect):
                self.update_action(2)
                
                self.shoot()        
            if self.idling == False:
                if self.direction == 1:
                    self.enemy_moving_right = True
                    self.enemy_moving_left = False
                else:
                    self.enemy_moving_right = False
                    self.enemy_moving_left = True
                self.move(self.enemy_moving_left,self.enemy_moving_right,self.enemy_jump)
                self.update_action(1)
                self.move_counter +=1
                self.vision.center = (self.rect.centerx + 75*self.direction,self.rect.centery)
                #pygame.draw.rect(screen,(255,0,0),self.vision)
                if self.move_counter == 20:
                    self.direction *=-1
                    self.move_counter *= -1 
            else:
                self.idling_counter -= 1
                if self.idling_counter <=0:
                    self.idling = False
        #Scroll
        self.rect.x += SCREEN_SCROLL
                
    
    def move(self,moving_left,moving_right,jump):
        
        dx = 0
        dy = 0
        if moving_left:
            dx -= self.speed
            self.flip = True
            self.direction = -1
        elif moving_right:
            dx += self.speed
            self.flip = False
            self.direction = 1
        elif jump and self.in_air == False:
            self.vel_y = -15
            jump = False
            self.in_air= True
        self.vel_y += GRAVITY
        if self.rect.y > SCREEN_HEIGHT:
            self.health = 0
        if self.vel_y >10:
            self.vel_y
        dy += self.vel_y
        for tile in world.tiles_list:  #tiles list: index 0 is image, 1 is img rect
            #Check for collision in  y direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y,self.width,self.height):
                if self.direction >0:
                    dx = tile[1].left - self.rect.right
                elif self.direction <0:
                    dx = tile[1].right - self.rect.left
                 
            #Check for collision in  y direction            
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width,self.height):
                #Check if below the ground i.e jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    
                #Check if player is on the ground
                elif self.vel_y > 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y =0
                    self.in_air = False
                     
        #update rectangle x, y 
        self.rect.y += dy
        self.rect.x += dx
        #update roll base on player position
        SCREEN_ROLL = 0
        if self.char_type == 'PLAYER':
            if (self.rect.right > SCREEN_WIDTH-SCROLL_THRESH and BG_SCROLL < (tile_size*world.length_data)-SCREEN_WIDTH)  or (self.rect.left < SCREEN_ROLL and BG_SCROLL > abs(dx)) :
                self.rect.x -=dx
                SCREEN_ROLL = -dx
        return SCREEN_ROLL

'''Bullet'''
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.direction = direction
        if self.direction ==1:
            self.flip = False
        else:
            self.flip = True
        bullet_img = pygame.image.load('06.png').convert_alpha()
        self.image = pygame.transform.flip(pygame.transform.scale(bullet_img, (bullet_w, bullet_h)),self.flip,False)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        #move bullet
        self.rect.x += (self.speed*self.direction) 
        
        #Check if bullet has gone off screen
        if self.rect.right <0 or self.rect.left >1500:
            self.kill()
        
        for tile in world.tiles_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #Check collisions with character
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                self.kill()
                player.health -=10
                
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    self.kill()
                    
                    enemy.health-=25
'''Health bar'''
class Health_bar:
    def __init__(self,x,y,health,max_health):
        self.x = x
        self.y = y
        self. health = health 
        self.max_health = max_health
    def draw(self,health):
        self.health = health
        ratio = self.health/self.max_health
        pygame.draw.rect(screen,(255,0,0),(self.x,self.y,150,20))
        pygame.draw.rect(screen,(0,255,0),(self.x,self.y,150 * ratio,20))
        
        
            

''' World arena '''
world_data = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,2,0,2,0,2,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[1,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2,2],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],]

class World:
    def __init__(self,world_data):
        self.tiles_list = []
        dirt_img = pygame.image.load(r'Dirt block.png')
        grass_img = pygame.image.load('Grass Block.png')
        self.length_data = len(world_data[0])
        
        for row_index,row in enumerate(world_data):
            for col_index,cell in enumerate(row):
                if cell == 1:
                    img = pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x= col_index* tile_size
                    img_rect.y= row_index* tile_size
                    tile = (img,img_rect)
                    self.tiles_list.append(tile)
                elif cell == 2:
                    img = pygame.transform.scale(grass_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x= col_index* tile_size
                    img_rect.y= row_index* tile_size
                    tile = (img,img_rect)
                    self.tiles_list.append(tile)
                
                    
    def draw(self):
        for img,img_rect in self.tiles_list:
            img_rect.x += SCREEN_SCROLL
            screen.blit(img,(img_rect))                  
                
'''Item '''
class Items(pygame.sprite.Sprite):
    def __init__(self, x, y, item):
        pygame.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y
        self.item_name = item.upper()
        star_img = pygame.image.load('star.png')
        heart_img =pygame.image.load('heart.png')
        if self.item_name == 'STAR':
            self.image = pygame.transform.scale(star_img,(tile_size,tile_size))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
        elif self.item_name == 'HEART':
            self.image = pygame.transform.scale(heart_img,(tile_size,tile_size))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            
        
    def update(self):
        
        global score
        if pygame.sprite.collide_rect(self, player):
            if self.item_name == "STAR":
                score +=1
            elif self.item_name == "HEART":
                if player.health + 25 >100:
                    player.health = 100
                else:
                    player.health += 25
            self.kill()
    
    def draw(self):
        self.rect.x += SCREEN_SCROLL
        screen.blit(self.image,self.rect)
        

#Create world
world = World(world_data)

#create sprite group:        
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()


#Enemy
enemy = soldier (1000,400, 0.25, 5,"enemy")
enemy2 = soldier (2200,50, 0.25, 5,'enemy')
enemy3 = soldier (100,50, 0.25, 5,"enemy")
enemy4 = soldier (3000,50, 0.25, 5,"enemy")
enemy5 = soldier (2000,50, 0.25, 5,"enemy")


enemy_group.add(enemy)
enemy_group.add(enemy2)
enemy_group.add(enemy3)
enemy_group.add(enemy4)
enemy_group.add(enemy5)



#Item
star = Items(300,500,'star')
star2 = Items(200,400,'star')
star3 = Items(1500,200,'heart')
star4 = Items(2000,400,'heart')
star5 = Items(1000,400,'heart')
star6 = Items(tile_size*20,200,'Star')
star7 = Items(tile_size*(world.length_data-2),500,'Star')
star8 = Items(tile_size*8,tile_size*4.5,'star')
star9 = Items(tile_size*7,tile_size*1,'star')

items_group.add(star)
items_group.add(star2)
items_group.add(star3)
items_group.add(star4)
items_group.add(star5)
items_group.add(star6)
items_group.add(star7)
items_group.add(star8)
items_group.add(star9)


winscore = 0
for item in items_group:
    if item.item_name == "STAR":
        winscore += 1


player = soldier(150,100,0.25,10,"player")
health_bar = Health_bar(50,50,player.health,player.max_health)


win = False
run = True
start = False
while run:
    screen.fill((202,228,241))
   
    if start == False:
        if start_button.draw():
            start = True
        if exit_button.draw():
            run = False
    else:
        if int(score) == winscore:
            win = True
        draw_bg()
        
        world.draw()
        draw_text(50,100, "Health bar", (200,200,200))
        draw_text (SCREEN_WIDTH/2,60,"Score: "+ str(score),(255,0,0))
        #Char
        if player.alive:
            player.draw()
            SCREEN_SCROLL = player.move(moving_left,moving_right,jump)
            BG_SCROLL -= SCREEN_SCROLL
            player.update()
            health_bar.draw(player.health)
            if win:
                screen.blit(win_image,(200,150))
            if shoot:
                player.update_action(2)
                player.shoot()
            elif moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)
            
        for item in items_group:
            item.draw()
            item.update()

         #Enemy
       
        for enemy in enemy_group:
            enemy.update()
            enemy.draw()
            enemy.robot()
            
        #Update & draw bullet group
        bullet_group.update()
        bullet_group.draw(screen)
        
            
            
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and player.alive:
            
            if event.key == pygame.K_ESCAPE:
               run = False
              
            elif event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_k:
                jump = True
            elif event.key == pygame.K_j:
                shoot = True
            elif event.key ==pygame.K_p:
               run = False
        
        elif event.type == pygame.KEYUP:
           
            if event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_k:
                jump = False
            elif event.key == pygame.K_j:
                shoot = False
    
    clock.tick(FPS)
    pygame.display.update()
    
pygame.quit()
