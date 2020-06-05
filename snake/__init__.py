from gym.envs.registration import register

register(
    id='SelfSnake-v0',
    entry_point='snake.envs:SnakeEnv',
    max_episode_steps=1000,
)