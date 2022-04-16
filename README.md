# Charging Station Environment
Chargym is an open source OpenAI Gym environment for the implementation of Reinforcement Learning (RL), Rule-based approaches (RB) and Intelligent Control (IC) for charging scheduling at an EV charging station with a defined number of charging spots and random EV arrivals and departures within day.


The Chargym interaction system is illustrated below:

![Ev Station](https://github.com/georkara/Chargym-Charging-Station/blob/main/Chargym_Charging_Station/images/Chargym_interaction_system.jpg)


## Chargym Description
The EV charging station is composed of: i) a set of 10 charging spots; ii) one photovoltaic (PV) generation system; iii) power grid connection offering energy at a certain price and  iv) the vehicle to grid operation (V2G), which adds a Vehicle to Charging Station functionality, allowing the usage of energy stored in EVs for charging other EVs, when necessary.

The station is connected with the grid absorbing electricity at a certain price, 
when the available amount of energy is inadequate. The station's available amount of energy 
(apart from the grid) is unfolded into two types:
1) Stored energy in the cars that can be utilized under the V2G operation.
2) Produced energy from the PV.

Note that the term _stored energy_ refers to storage that is formed from the available energy storage of EVs in a Vehicle to Charging Station perspective.
Therefore, the environment describes a case where the stored energy in EVs, can be utilized from the station (based on the control setpoints) to satisfy the demands of other EVs that have limited time until their departure time.
Note also that each parking/charging spot can be used as many times as possible within day if available/free (see __Assumption 6__ below).

The environment offers two operational options [ control_flag in class ```ChargingEnv``` in the file [Charging_Station_Enviroment.py](/Chargym_Charging_Station/envs/Charging_Station_Enviroment.py) ]. The first one is [Simulate_RBC.py](/Chargym_Charging_Station/utils/Simulate_RBC.py) (control_flag=0) while the second is [Simulate_Actions.py](/Chargym_Charging_Station/utils/Simulate_Actions.py) (control_flag=1).

The main objective of this problem is to minimize the cost for the electricity absorbed by the power grid
ensuring that all EVs reach the desired level of State of Charge (100% - see __Assumption 2__ below). Thus, a penalty factor is induced in case that an EV departs with less that 100% State of Charge (see __Assumption 3__ below).

## Charging Station Assumptions
_Assumption 1_: All EVs that arrive to the station are assumed to share the same characteristics related with their battery (type, capacity, charging/ discharging rate, charging/ discharging efficiency, battery efficiency).

_Assumption 2_: The desired State of Charge for every EV at departure time is 100%.

_Assumption 3_: If an EV departs with less than 100\% State of Charge, a penalty score is calculated. 

_Assumption 4_: There is no upper limit of supply from the power grid. This way, the grid can supply the Charging Station with any amount of requested energy.

_Assumption 5_: The maximum charging/discharging supply of each EV is dictated by charging/discharging rate of the station.

_Assumption 6_: Each charging spot, can be used more than once per day.


## Installation-Requirements
In order to install, download the zip file or use git.
Open project, choose system interpreter (_we recommend an environment with Python version 3.7 or above_ because the provided examples are based on Stable-Baselines3
[SB3](https://github.com/DLR-RM/stable-baselines3). But if you want you can use other implementations too.) and follow the command:

```console
cd Chargym-Charging-Station
pip install -e .
pip install stable-baselines3[extra]
```


[__No need to install requirements__]Refer to [requirements.txt](requirements.txt) for a list of Python library dependencies. You may install the required libraries by executing the following command:
 ```console
 pip install -r requirements.txt
 ```





## Files


    Chargym-Charging-Station

        ├── README.md

        ├── setup.py

        ├── Chargym_Charging_Station
          ├── envs
            ├── __init__.py
            └── Charging_Station_Enviroment.py

          ├── Files
            ├── Initial_Values.mat
            ├── Results.mat
            └── Weather.mat

          ├── images
            └── Chargym_interaction_system.jpg

          ├── utils
            ├── Energy_Calculations.py
            ├── Init_Values.py
            ├── Simulate_Actions3.py
            └── Simulate_Station3.py

          └── __init__.py

        └── Solvers
          ├── RBC
            ├── RBC.py
            └── rbc_main.py
          ├── RL
            ├── DDPG_train.py
            └── PPO_train.py
          ├── check_env.py
          └── evaluate_trained_models.py
          


- [Charging_Station_Enviroment.py](/Chargym_Charging_Station/envs/Charging_Station_Enviroment.py): Describes the general Electrical Vecicles Charging Station universe.

- [Energy_Calculations.py](/Chargym_Charging_Station/utils/Energy_Calculations.py): more will be included.
- [Init_Values.py](/Chargym_Charging_Station/utils/Init_Values.py): more will be included.
- [Simulate_Actions3.py](/Chargym_Charging_Station/utils/Simulate_Actions3.py): more will be included.
- [Simulate_Station3.py](/Chargym_Charging_Station/utils/Simulate_Station3.py): more will be included.

- [RBC.py](Solvers/RBC/RBC.py): This implements the Rule Based Controller described in Equation 6 in the original paper. The controller checks each charging spot and collects the Departure timeplan of each connected EV. If an EV is going to depart during the next three hours, then the station is charging in full capacity this specific EV. On the other hand, if an EV does not depart during the next three hours, the station checks the current availability of the solar energy and charges the EV, based on that availability. The three hour time-limit, is selected based on the EV Charging Station attributes, since the EVs utilize 30kWh batteries, and the maximum charging ability of the station is 10kW. Thus, an EV needs three hours to charge from 0 to 100% SoC.
- [rbc_main.py](Solvers/RBC/rbc_main.py): This is used if you want to use solely the Rule Based Controller.

- [DDPG_train.py](Solvers/RL/DDPG_train.py): This python file includes conventional DDPG implementation. __Note that when you run this script 2 additional folders will be created including log files and the trained model at different stages. The later will be used in order to evaluate the trained algorithm during the evaluation phase__.
- [PPO_train.py](Solvers/RL/PPO_train.py): This python file includes conventional PPO implementation. __Note that when you run this script 2 additional folders will be created including log files and the trained model at different stages as in DDPG case. Logs and models have the corresponding tag 'PPO-'. The trained model will be used in order to evaluate the PPO algorithm during the evaluation phase__.

- [check_main.py](/Solvers/check_main.py): This is to check the Chargym environment.
- [evaluate_trained_models.py](/Solvers/evaluate_trained_models.py): This is to evaluate the trained models (DDPG,PPO and RBC).Indicatevely in paper we used the trained models at 940000 so as at lines 23 and 27 the corresponding .zip files are loaded.



## Charging Station Environment Variables
- States (28 in total)
  - ```self.disturbances[0]```: solar radiation at current time step
  - ```self.disturbances[1]```: value of price at current time step
  - ```self.predictions[0][0]```: one hour ahead solar radiation prediction  
  - ```self.predictions[0][1]```: two hours ahead solar radiation prediction  
  - ```self.predictions[0][2]```: three hours ahead solar radiation prediction  
  - ```self.predictions[0][3]```: one hour ahead price prediction  
  - ```self.predictions[0][4]```: two hours ahead price prediction  
  - ```self.predictions[0][5]```: three hours ahead price prediction 
  - ```self.states[0] - self.states[9]```: state of charge of the EV at i<sub>th</sub>  charging spot at current time step
  - ```self.states[10] - self.states[19]```: the number of hours until departure for the EV at i<sub>th</sub> charging spot

States space: [0-1000, 0-300, 0-1000, 0-1000, 0-1000, 0-300, 0-300, 0-300, 0-100, 0-100]

__Note that all states are normalized between 0 and 1__.
- Actions (1 action per charging spot, 10 in total)
  - ```actions```: One action per spot defining the charging or discharging rate of each vehicle spot. These 10 action set-points are defined as continuous variables, which are constrained in the interval __[-1,1]__.

## Reward function

The reward function is described in [Simulate_Actions3.py](/Chargym_Charging_Station/utils/Simulate_Actions3.py).
The main objective of the EVCS's controller / agent is to adopt a scheduling policy towards minimizing the cost for the electricity absorbed by the power grid. The reward function observed at each timestep _t_ is the electricity bill being payed by EVCS to the utility company (named ```Cost_1``` in line 46 which is Grid_final*self.Energy["Price"][0,hour]). However, an additional term is incorporated in order to present a more realistic and complete description ensuring that the controller will exploit effectively the available resources as well as fulfil the defined requirements. The second term considers penalizing situations involving EVs that are not completely charged (named ```Cost_3``` in line 60). The penalty factor named ```Cost_2``` that tries to describe a penalty on wasted RES energy is not considered in this version. Feel free to introduce such an extension if you want.


## How to run-Test example
Chargym is designed to work with different controller approaches as mentioned above, including RBC, MPC, RL or other intelligent controllers. 
The charging station environment and its interface is provided together with a Rule Based Controller as described above. 
Also, we provide simple examples using well-known Reinforcement Learning approaches to present ready to run examples
that are easy for users and practictioners to use.

### Custom implementation
In case that the user wants to check his/her own controller than the provided ones, import Chargym and then
call the make method specifying the name of the model (__ChargingEnv-v0__) as in other gym environments. You can
place your custom algorithm in Folder ->  __Solvers__.

If you want to check the environment then run the file located in __Solvers__ named: [check_main.py](/Chargym_Charging_Station/Solvers/check_main.py)
```
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


```

### Ready to Use Examples

If you want to train either DDPG or PPO using Chargym:
1. __You have to specify by hand the reset_flag in [Charging_Station_Enviroment.py](/Chargym_Charging_Station/envs/Charging_Station_Enviroment.py) line 89 if you want to emulate different days(reset_flag=0) or the same simulated day (reset_flag=1) across episodes__.
2. __then run [DDPG_train.py](Solvers/RL/DDPG_train.py) and [PPO_train.py](Solvers/RL/PPO_train.py)__.

If you want to evaluate the trained models:
1. __You have to modify by hand [Charging_Station_Enviroment.py](/Chargym_Charging_Station/envs/Charging_Station_Enviroment.py) in line 89 to:__
``` def reset(self, reset_flag) ``` __removing the value of reset_flag__.
2. __then run [evaluate_trained_models.py](/Solvers/evaluate_trained_models.py) and you will get the comparison performance between DDPG, PPO and RBC__. 


# Citation
If you find this useful for your research, please use the following:
```
Chargym: An EV Charging Station Model for Controller Benchmarking

```

## Link
If you are interested in ongoing or future working projects of ConvCAO research group in various fields,
please visit: [ConvCAO Page](https://convcao.com/).

## License
The MIT License (MIT) Copyright (c) 2022, ConvCAO research group, CERTH, Greece

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

