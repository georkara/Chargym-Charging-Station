import gym
import Chargym_Charging_Station

import gym
import numpy as np
import os
import argparse
from Solvers.RBC.RBC import RBC

from stable_baselines3 import DDPG, PPO
import time
import matplotlib.pyplot as plt



parser = argparse.ArgumentParser()
parser.add_argument("--env", default="ChargingEnv-v0")
parser.add_argument("--reset_flag", default=1, type=int)
args = parser.parse_args()
env = gym.make(args.env)
#Define which model to load
models_dir1="models/DDPG-1646748022"
model_path1=f"{models_dir1}/940000.zip"
model1 = DDPG.load(model_path1, env=env)

models_dir2="models/PPO-1646764100"
model_path2=f"{models_dir2}/940000.zip"
model2 = PPO.load(model_path2, env=env)

#How many evaluations
episodes=100
final_reward_DDPG=[0]*episodes
final_reward_PPO=[0]*episodes
final_reward_rbc=[0]*episodes
for ep in range(episodes):
    rewards_list_DDPG = []
    rewards_list_PPO = []
    rewards_list_rbc=[]
    #Note that reset_flag=0 means that the environment simulates/emulates a new day and reset_flag=1 means that simulates the same day.
    #This way, in order to compare two RL algorithms with the RBC we need to specify reset_flag=0 at the start of each episode (right before) the DDPG
    #and change to reset_flag=1 for the other two methods within the same episode. This way it will simulate the same day for all three approaches at each episode, 
    #but diverse days across episodes.
    
    ##########obs = env.reset(0)##########

    #DDPG
    obs=env.reset(reset_flag=0)
    done=False
    while not done:
        action, _states = model1.predict(obs)
        obs, reward_DDPG, done, info = env.step(action)
        rewards_list_DDPG.append(reward_DDPG)

    final_reward_DDPG[ep] = sum(rewards_list_DDPG)

    # PPO
    obs = env.reset(reset_flag=1)
    done = False
    while not done:
        action, _states = model2.predict(obs)
        obs, reward_PPO, done, info = env.step(action)
        rewards_list_PPO.append(reward_PPO)

    final_reward_PPO[ep] = sum(rewards_list_PPO)
    #RBC case
    ##########obs = env.reset(1)##########

    obs=env.reset(reset_flag=1)
    done=False
    while not done:
        # state = obs
        action_rbc = RBC.select_action(env.env, obs)
        obs, rewards_rbc, done, _ = env.step(action_rbc)
        # print(rewards)
        # obs = next_state_rbc
        rewards_list_rbc.append(rewards_rbc)
    final_reward_rbc[ep] = sum(rewards_list_rbc)
env.close

Mean_reward_DDPG=np.mean(final_reward_DDPG)
Mean_reward_PPO=np.mean(final_reward_PPO)
Mean_reward_RBC=np.mean(final_reward_rbc)

plt.rcParams.update({'font.size': 18})
plt.plot(final_reward_DDPG)
plt.plot(final_reward_PPO)
plt.plot(final_reward_rbc)
plt.xlabel('Evaluation episodes')
plt.ylabel('Reward')
plt.legend(['DDPG', 'PPO', 'RBC'])

plt.show()

a=1



