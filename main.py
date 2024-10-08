#importing modules
import pygame
import os
import random


pygame.init()
#Classes

class Label(pygame.sprite.Sprite):
    def __init__(self, text, position, font_size=30, font_color=(255, 255, 255), font_name=None, alignment="topleft", groups=None):
        super().__init__(groups)
        pygame.font.init()
        self.text = text
        self.position = position
        self.font_color = font_color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.alignment = alignment
        self.image = self.font.render(self.text, True, self.font_color)
        self.rect = self.image.get_rect()
        self.set_position(position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update_text(self, new_text):
        self.text = new_text
        self.image = self.font.render(self.text, True, self.font_color)
        self.rect = self.image.get_rect()
        self.set_position(self.position)

    def set_position(self, new_position):
        self.position = new_position
        setattr(self.rect, self.alignment, self.position)

class Sprites(pygame.sprite.Sprite):
    def __init__(self,image,x,y,width,height,groups = []):
        super().__init__(*groups)
        self.original_image = image
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),self.original_image)),(width,height))
        self.rect = self.image.get_rect(topleft = (x,y))

    def draw(self,x,y, window):
        window.blit(self.image,(x,y))

class Gravity_Affected_Objects(Sprites):
    def __init__(self, image, x, y, width, height,Gravity_effect = 10, groups=[]):
        super().__init__(image, x, y, width, height, groups)
        self.Velocity = 0
        self.Gravity = Gravity_effect
    def update(self):
        self.Velocity += self.Gravity
        self.rect.y -= self.Velocity

class Player(Gravity_Affected_Objects):
    def __init__(self, image, x, y, width, height, Velocity=10,Jump_Vel = 20,Speed = 15, groups=[]):
        super().__init__(image, x, y, width, height, Velocity, groups)
        self.Jump_Vel = Jump_Vel
        self.Speed = Speed
    def update(self,):
        global game_window
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.Jump()
    def Jump(self):
        self.Velocity = self.Jump_Vel

#Creating Game window
game_window = pygame.display.set_mode((600,650))


#Setting name to our window
pygame.display.set_caption("Game Window")

#Variables
Pygame_Clock = pygame.time.Clock()
Game_FPS = 60
Game_Cycle_End = False
Game_Pause = False
Frames = 0
Every_Object = pygame.sprite.Group()
#Objects
Game_Player = Player("player.png",300,300,25,25,10,20,15,Every_Object)

#setting game cycle
while not Game_Cycle_End:
    #getting events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game_Cycle_End = True



    if not Game_Pause:
        game_window.fill((255,255,255))
        Frames += 1
        Every_Object.update()
        Every_Object.draw(game_window)
    pygame.display.flip() # or pygame.display.update

    Pygame_Clock.tick(Game_FPS) #To limit game FPS

#to actually quit
pygame.quit()