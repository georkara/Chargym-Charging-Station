import gym
import Chargym_Charging_Station
import argparse

import numpy
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise

#this is just to check if gym.make runs properly without errors

parser = argparse.ArgumentParser()
parser.add_argument("--env",
                        default="ChargingEnv-v0")  # OpenAI gym environment name #Pendulum-v1 RoboschoolHalfCheetah-v1
#parser.add_argument("--price", default=1, type=int)
#parser.add_argument("--solar", default=1, type=int)
#parser.add_argument("--control_flag", default=1, type=int)
args = parser.parse_args()
env = gym.make(args.env)

n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=numpy.zeros(n_actions), sigma=0.1 * numpy.ones(n_actions))

model = DDPG('MlpPolicy', env, action_noise = action_noise, verbose=1)
model.learn(total_timesteps=10000, log_interval=10)

obs = env.reset()
summation=[]
done=0
while done == 0:
    action, _state = model.predict(obs)
    print(action)
    obs, reward, done, info = env.step(action)
    summation.append(reward)

print(sum(summation))