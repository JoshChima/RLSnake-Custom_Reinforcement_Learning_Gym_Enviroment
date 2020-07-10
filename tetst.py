import gym
import snake
import random
import time
from snake.envs.Snake import img_display
from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from stable_baselines.common.env_checker import check_env

env_name = "SelfSnake-v0"
env = gym.make(env_name)

# model = PPO2(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=1_000_000)
# model.save(f'PPO2_{env_name}')
# del model
model = PPO2.load(f"PPO2_{env_name}")
env.render()
obs = env.reset()
rounds = 5
score = 0
while rounds >= 0:
    action, _states = model.predict(obs, deterministic=False)
    obs, rewards, dones, info = env.step(action)
    time.sleep(0.1)
    if rewards > 0:
        score += rewards
        print(f'Round {rounds} Score: {score}', end='\r')
    if dones:
        obs = env.reset()
        rounds -= 1
        score = 0
