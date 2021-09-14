import gym
from random import seed
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import PPO
from ros_social_gym import RosSocialEnv

env = DummyVecEnv([lambda: RosSocialEnv(1, 20, "config/gym_gen/launch.launch")])
model = PPO("MlpPolicy", env, verbose=0)

count = 0
upper = 1000
while(count < upper):
  model.learn(total_timesteps=2000)
  # Save the agent
  model.save("data/ppo_" + str(count))
  count += 1