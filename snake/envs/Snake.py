import pygame
import math
import numpy as np
import collections as coll
import random
import cv2
import time
import turtle


BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = [169, 169, 169]
WHITE = [255, 255, 255]
PINK = (255, 0, 127)
GREEN = (0, 204, 102)

def img_display(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# def loc_gen():
#     x = random.randint(0, (WIDTH-SCL)/SCL) * SCL
#     y = random.randint(0, (HEIGHT-SCL)/SCL) * SCL
#     return (x,y)

# Joint_FOOD = [loc_gen() for i in range(100000)]

class Food:
    def __init__(self, enviroment_width, enviroment_height, scale, snake):
        self.enviroment_width = enviroment_width
        self.enviroment_height = enviroment_height
        self.scl = scale
        self.x = random.randint(0, enviroment_width/self.scl) * self.scl
        self.y = random.randint(0, enviroment_height/self.scl) * self.scl
        self.picklocation(snake)
        self.eaten = False

    @property
    def food_obj(self):
        return pygame.Rect(self.x, self.y, self.scl, self.scl)

    def picklocation(self, snake):
        head = [snake.head_square]
        tail = snake.tail
        fullSnake = head + tail

        self.x = random.randint(
            0, (self.enviroment_width-self.scl)/self.scl) * self.scl
        self.y = random.randint(
            0, (self.enviroment_height-self.scl)/self.scl) * self.scl

        if self.food_obj.collidelist(fullSnake) > 0:
            self.picklocation(snake)
        else:
            self.eaten = False


class Snake(object):
    def __init__(self, enviroment_width, enviroment_height, scale, isBot):
        self.ENVWIDTH = enviroment_width
        self.ENVHEIGHT = enviroment_height
        self.x = enviroment_width/2
        self.y = enviroment_height/2
        self.xspeed = scale
        self.yspeed = 0
        self.scl = scale
        self.direction = 'RIGHT'

        self.isBot = isBot

        self.state_stamp = 0
        self.total_body = 0
        self.living_score = 0
        self.score = 0
        self.eat_score = 1
        self.death_score = -1
        self.tail = []
        self.head = pygame.rect.Rect(self.x, self.y, self.scl, self.scl)
        self.t = 0
        # self.starve_t = 10 * self.total_body
        self.last_meal = 0

    @property
    def starve_t(self):
        return 50 * (self.total_body + 1)

    @property
    def head_square(self):
        return pygame.Rect(self.x, self.y, self.scl, self.scl)
    
    # @property
    # def guider(self):
    #     return pygame.Rect(int(self.x+self.xspeed) + int(self.scl/2), int(self.y+self.yspeed) + int(self.scl/2), 1, 1)

    def keys(self):
        if not(self.isBot):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.direction != 'RIGHT':
                self.xspeed = self.scl * -1
                self.yspeed = 0
                self.direction = 'LEFT'
            else:
                pass
            if keys[pygame.K_RIGHT] and self.direction != 'LEFT':
                self.xspeed = self.scl
                self.yspeed = 0
                self.direction = 'RIGHT'
            else:
                pass
            if keys[pygame.K_DOWN] and self.direction != 'UP':
                self.xspeed = 0
                self.yspeed = self.scl
                self.direction = 'DOWN'
            else:
                pass
            if keys[pygame.K_UP] and self.direction != 'DOWN':
                self.xspeed = 0
                self.yspeed = self.scl * -1
                self.direction = 'UP'
            else:
                pass
        else:
            pass

    def botKeys(self, choice):
        if choice == 0 and self.direction != 'RIGHT':
            self.xspeed = self.scl * -1
            self.yspeed = 0
            self.direction = 'LEFT'
        if choice == 1 and self.direction != 'LEFT':
            self.xspeed = self.scl
            self.yspeed = 0
            self.direction = 'RIGHT'
        if choice == 2 and self.direction != 'UP':
            self.xspeed = 0
            self.yspeed = self.scl
            self.direction = 'DOWN'
        if choice == 3 and self.direction != 'DOWN':
            self.xspeed = 0
            self.yspeed = self.scl * -1
            self.direction = 'UP'
        if choice == 4:
            pass

    def isalive(self):

        if self.x > self.ENVWIDTH-self.scl or self.x < 0:
            self.score -= self.death_score
            return False
        elif self.y > self.ENVHEIGHT-self.scl or self.y < 0:
            self.score -= self.death_score
            return False
        elif abs(self.t - self.last_meal) > self.starve_t:
            return False
        elif len(self.tail) > 0:
            if self.head_square.collidelist(self.tail) != -1:
                self.score -= self.death_score
                return False
            else:
                self.score += self.living_score
                return True
        else:
            self.score += self.living_score
            return True

    def eat(self, food):
        if self.head_square.colliderect(food.food_obj) > 0:
            food.eaten = True
            self.total_body += 1
            self.score += self.eat_score
            self.last_meal = self.t
        else:
            pass

    def update(self):
        part = self.head_square
        self.tail.append(part)
        # self.rmx = self.tail[0].x
        # self.rmy = self.tail[0].y
        del self.tail[0]
        while len(self.tail) < self.total_body:
            part = self.head_square
            self.tail.append(part)
        while len(self.tail) > self.total_body:
            del self.tail[0]

        self.x += self.xspeed
        self.y += self.yspeed
        self.t += 1




class SnakeMain():
    def __init__(self, Width=400, Height=400, scl=20, ALLOWRENDER=False):
        self.W = Width
        self.H = Height
        self.scl = scl
        self.run = False
        self.ALLOWRENDER = ALLOWRENDER
        if ALLOWRENDER:
            pygame.init()
        # self.WINDOW = pygame.display.set_mode((self.W, self.H))
        self.WINDOW = pygame.Surface((self.W, self.H))
        self.snake = Snake(self.W, self.H, self.scl, True)
        self.food = Food(self.W, self.H, self.scl, self.snake)
        self.old_score = 0
        self.food.picklocation(self.snake)

    def observe(self):
        view = pygame.surfarray.array3d(self.WINDOW)

        view = view.transpose([1,0,2])

        img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
        # img_display(view)

        # arr = np.flip(np.array(pygame.surfarray.array3d(self.WINDOW)), (1, 2))
        # img = cv2.rotate(arr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return img_bgr

    def draw(self):
        self.WINDOW.fill((0, 0, 0))
        pygame.draw.rect(self.WINDOW, PINK, self.food.food_obj)
        pygame.draw.rect(self.WINDOW, GREEN, self.snake.head_square)
        for part in self.snake.tail:
            pygame.draw.rect(self.WINDOW, WHITE, part)
        
    def action(self, action):
        self.snake.botKeys(action)
        self.snake.update()

        self.snake.eat(self.food)

        self.draw()

        # guider
        # pygame.draw.circle(self.WINDOW, WHITE, (self.snake.guider.x, self.snake.guider.y), 4)

        if self.food.eaten == True:
            del self.food
            self.food = Food(self.W, self.H, self.scl, self.snake)
        
        if self.ALLOWRENDER:
            pygame.display.update()    

        self.snake.isalive()

    def evaluate(self):
        reward = (self.snake.score - self.old_score)
        self.old_score += reward
        return reward

    def is_done(self):
        if self.snake.isalive():
            return False
        else:
            # print('##################### Score: %s ########################'%(self.snake.score))
            pass
        return True

    def view(self):
        # Must be called before making actions
        del self.WINDOW
        self.WINDOW = pygame.display.set_mode((self.W, self.H))
        self.ALLOWRENDER = True
        # print('Score: %s'%(self.snake.score))

    def restartSnake(self):
        del self.snake
        self.snake = Snake(self.W, self.H, self.scl, True)
        self.food.picklocation(self.snake)

    def paused(self):
        if self.snake.isBot == False:
            P = True

            def text_objects(text, font):
                textSurface = font.render(text, True, (255, 255, 255))
                return textSurface, textSurface.get_rect()
            largeText = pygame.font.SysFont("comicsansms", 115)
            TextSurf, TextRect = text_objects("Paused", largeText)
            TextRect.center = ((self.W/2), (self.H/2))
            self.WINDOW.blit(TextSurf, TextRect)
            pygame.display.update()

            # do not mess with anything that says _PSLOT, it allows for game pausing
            _PSLOT = ['|']

            while P:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.run = False
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_p]:
                        _PSLOT.remove(_PSLOT[0])
                if len(_PSLOT) < 1:
                    P = False

                pygame.time.Clock().tick(100)
            # img_display(self.game_state)
        else:
            pass

    def restartOption(self):
        P = True

        def text_objects(text, font):
            textSurface = font.render(text, True, (255, 255, 255))
            return textSurface, textSurface.get_rect()
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = text_objects(
            "Your Died: Press R to Restart", largeText)
        TextRect.center = ((self.W/2), (self.H/2))
        self.WINDOW.blit(TextSurf, TextRect)
        pygame.display.update()

        # do not mess with anything that says _PSLOT, it allows for game pausing
        _PSLOT = ['|']

        while P:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.run = False
                    return False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    _PSLOT.remove(_PSLOT[0])
                    return True
            if len(_PSLOT) < 1:
                P = False

            pygame.time.Clock().tick(100)


# Game = SnakeMain()
# for i in range(100):
#     pygame.event.get()
#     Game.action(random.randint(0,5))
#     obs = Game.observe()
#     if i % 20 == 0:
#         print(i)
#         img_display(obs)
#     print(obs.shape)
#     reward = Game.evaluate()
#     done = Game.is_done()
#     # time.sleep(0.5)
#     if done:
#         pygame.quit()
#         del Game
#         Game = SnakeMain()
#         obs = Game.observe()