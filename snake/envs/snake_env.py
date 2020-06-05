import gym
from gym import spaces
import numpy as np
from snake.envs.Snake import SnakeMain
import random
import pygame

WIDTH = 400
HEIGHT = 400
SCL = 20

# self.x = random.randint(
#             0, (self.enviroment_width-self.scl)/self.scl) * self.scl
#         self.y = random.randint(
#             0, (self.enviroment_height-self.scl)/self.scl) * self.scl

class SnakeEnv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.Game = SnakeMain(WIDTH, HEIGHT)
        # TODO spaces
        self.action_space = spaces.Discrete(5)
    # Example for using image as input:
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.Game.W, self.Game.H, 3), dtype=np.uint8)

    def reset(self):
        # pygame.quit()
        del self.Game
        self.Game = SnakeMain(WIDTH, HEIGHT)
        obs = self.Game.observe()
        return obs

    def step(self, action):
        # pygame.event.get()
        self.Game.action(action)
        obs = (self.Game.observe())
        reward = self.Game.evaluate()
        done = self.Game.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.Game.view()


class SnakeRender(gym.Wrapper):
    """Render env by calling its render method.

    Args:
        env (gym.Env): Env to wrap.
        **kwargs: Keyword arguments passed to the render method.
    """

    def __init__(self, env, **kwargs):
        super().__init__(env)
        pygame.init()
        del self.env.Game.WINDOW
        self.env.Game.WINDOW = pygame.display.set_mode((self.env.Game.W, self.env.Game.H))
        self._kwargs = kwargs

    def reset(self, **kwargs):
        pygame.quit()
        ret = self.env.reset(**kwargs)
        # self.env.render(**self._kwargs)
        return ret

    def step(self, action):
        pygame.event.get()
        pygame.display.update()
        ret = self.env.step(action)
        pygame.display.update()

        self.env.render(**self._kwargs)
        return ret