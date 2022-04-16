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
            ├── Simulate_RBC.py
            └── Station_simulation3.py

          └── __init__.py

        └── Solvers
          ├── RBC
            └── RBC_controller.py
          ├── RL
            └── A2C.py
          └── main.py
          


- [Energy_Calculations.py](/Chargym_Charging_Station/utils/Energy_Calculations.py): more will be included.
- [Init_Values.py](/Chargym_Charging_Station/utils/Init_Values.py): more will be included.
- [Simulate_Actions.py](/Chargym_Charging_Station/utils/Simulate_Actions.py): more will be included.
- [Simulate_RBC.py](/Chargym_Charging_Station/utils/Simulate_RBC.py): more will be included.
- [Station_simulation.py](/Chargym_Charging_Station/utils/Station_simulation.py): more will be included.

- [Charging_Station_Enviroment.py](/Chargym_Charging_Station/envs/Charging_Station_Enviroment.py): more will be included.

- [main.py](/Solvers/main.py): This is to test the Chargym environment.

- [RBC_controller.py](Solvers/RBC/RBC_controller.py): RBC controller implementation.

- [A2C.py](Solvers/RL/A2C.py): This python file includes conventional RL implementations such as DDPG, A2C etc.



## Charging Station Environment Variables
- States (10 in total)
  - ```self.disturbances[0]```: solar radiation at current time step
  - ```self.disturbances[1]```: value of price at current time step
  - ```self.predictions[0][0]```: one hour ahead solar radiation prediction  
  - ```self.predictions[0][1]```: two hours ahead solar radiation prediction  
  - ```self.predictions[0][2]```: three hours ahead solar radiation prediction  
  - ```self.predictions[1][0]```: one hour ahead price prediction  
  - ```self.predictions[1][1]```: two hours ahead price prediction  
  - ```self.predictions[1][2]```: three hours ahead price prediction 
  - ```self.states[0]```: mean value of state of charge of battery at current time step
  - ```self.states[1]```: total value of power demand at current time step

States space: [0-1000, 0-300, 0-1000, 0-1000, 0-1000, 0-300, 0-300, 0-300, 0-100, 0-100]
- Actions (1 action)
  - ```action```: total charging rate of charging station at current time step (action space: [0-100])

## Reward function

The reward function is described in either [Simulate_RBC.py](/Chargym_Charging_Station/utils/Simulate_RBC.py) (for control_flag=0) or [Simulate_Actions.py](/Chargym_Charging_Station/utils/Simulate_Actions.py) (for case control_flag=1).
```RBC_Cost``` is the reward function, which is the multiplication of the amount of energy used from the power grid with the current price of KWh (RBC_Cost = Grid_final*self.Energy["Price"][0,hour]).

## How to run-Test example
Chargym is designed to work with different controller approaches as mentioned above, including RBC, MPC, RL or other intelligent controllers. 
The charging station environment and its interface is provided together with a Rule Based Controller (see __Chargym Description__). 
Also, we provide simple examples using well-known Reinforcement Learning approaches to present ready to run examples
that are easy for users and practictioners to use.

### Custom implementation
In case that the user wants to check his/her own controller than the provided ones, import Chargym and then
call the make method specifying the name of the model (__ChargingEnv-v0__) as in other gym environments. You can
place your custom algorithm in Folder ->  __Solvers__.

If you want to test the environment then run the file located in __Solvers__ named: [main.py](/Chargym_Charging_Station/Solvers/main.py)
```
import gym
import Chargym_Charging_Station
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

```

### Ready to Use Examples

__EXAMPLES WILL BE PRESENTED WITH FIGURES HERE__


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

