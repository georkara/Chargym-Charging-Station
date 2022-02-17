import gym
import gym_Charging_Station
import argparse

#this is just to check if gym.make runs properly without errors

parser = argparse.ArgumentParser()
parser.add_argument("--env",
                        default="ChargingEnv-v0")  # OpenAI gym environment name #Pendulum-v1 RoboschoolHalfCheetah-v1
#parser.add_argument("--price", default=1, type=int)
#parser.add_argument("--solar", default=1, type=int)
#parser.add_argument("--control_flag", default=1, type=int)
args = parser.parse_args()
env = gym.make(args.env)

observation=env.reset()
done = 0
U_Control = 0
reward_summation =[]
while done == 0:
    [observation, reward, done, info] = env.step(U_Control)
    reward_summation.append(reward)

print("Cost of the episode is:" + str(sum(reward_summation)))
