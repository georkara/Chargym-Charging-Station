import gym
import Chargym_Charging_Station
import argparse

#this is just to check if gym.make runs properly without errors

parser = argparse.ArgumentParser()
parser.add_argument("--env",
                        default="ChargingEnv-v0")  # OpenAI gym environment name #Pendulum-v1 RoboschoolHalfCheetah-v1
## parser.add_argument("--price", default=1, type=int)
## parser.add_argument("--solar", default=1, type=int)
## parser.add_argument("--reset_flag", default=1, type=int)

# Note that you need to specify the flags (price, solar and reset_flag within Charging_Station_Environment.py)
args = parser.parse_args()
env = gym.make(args.env)
