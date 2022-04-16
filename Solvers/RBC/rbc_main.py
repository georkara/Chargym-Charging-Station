import gym
import numpy as np
import Chargym_Charging_Station

import os
from RBC import RBC
import argparse

import time
models_dir = f"models/DDPG-{int(time.time())}"
logdir = f"logs/DDPG-{int(time.time())}"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

parser = argparse.ArgumentParser()
parser.add_argument("--env", default="ChargingEnv-v0")
parser.add_argument("--reset_flag", default=1, type=int)
args = parser.parse_args()
env = gym.make(args.env)

done=False
state = env.reset(reset_flag=0)
rewards_list = []
while not done:
    action = RBC.select_action(env.env,state)
    next_state, rewards, done, _ = env.step(action)
    #print(rewards)
    state = next_state
    rewards_list.append(rewards)

final_reward=sum(rewards_list)
print(final_reward)
