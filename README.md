﻿# Charging Station Environment
Chargym is an open source OpenAI Gym environment for the implementation of Reinforcement Learning (RL), Rule-based approaches (RB) and Intelligent Control (IC) for charging scheduling at an EV charging station with a defined number of charging spots and random EV arrivals and departures within day.


The charging station interaction system will be placed here

![Ev Station](https://github.com/georkara/Chargym-Charging-Station/blob/Chargym-Charging-Station/Chargym_Charging_Station/images/Chargym_interaction_system.jpg)


## Chargym Description
The EV charging station is composed of one PV and 10 charging spots. 
The station is connected with the grid absorbing electricity at a certain price, 
when the available amount of energy is inadequate. The station's available amount of energy 
(apart from the grid) is unfolded into two types:
1) Stored energy (_aggregated battery_ consisted of the stayed EVs) and
2) Produced energy from the PV.

Note that the term _aggregated battery_
refers to a virtual battery storage that is formed from the available energy storage of EVs in a Vehicle to Charging Station perspective.
Therefore, the environment describes a case where the stored energy in EVs, that are not going
to departure in the near future, can be utilized from the station to satisfy the demands of other EVs that 
have limited time until their departure time. This time interval is specified by default to be 2 hours. 
Note that the user can modify this time interval/window.
The EVs are identified between two profiles based on their departure time.
If an EV has to leave the station within the next 2 hours, then it is classified as “leave”.
Otherwise, it gets the label “stay”. This property allows the charging station to use the energy stored in the
“stay” vehicles to satisfy the demands of the classified as “leave” ones as mentioned above. 
Note also that each parking/charging spot can be used as many times as possible within day if available/free.

The environment offers two operational options [ control_flag in class ```ChargingEnv``` in the file [Charging_Station_Enviroment.py](/gym_Charging_Station/Files/Charging_Station_Enviroment.py) ]. The first one is [Simulate_RBC.py](/gym_Charging_Station/Simulate_RBC.py) (control_flag=0) while the second is [Simulate_Actions.py](/gym_Charging_Station/Simulate_Actions.py) (control_flag=1).

The main objective of this problem is to minimize the cost for the electricity absorbed by the power grid
ensuring that all EVs reach the desired level of State of Charge (100% - see __Assumption 3__ below).

## Charging Station Assumptions
_Assumption 1_: All EVs that arrive to the station are assumed to share the same characteristics related
with their battery (type, capacity, charging/discharging rate, charging/discharging efficiency, battery efficiency).

_Assumption 2_: All EVs that are going to departure the next 2 hours will be charged (giving them priority
to the available energy (PV generated and Vehicle to Charging Station stored energy(Virtual Battery))).

_Assumption 3_: The desired State of Charge for every EV at departure time is 100%. 

_Assumption 4_: There is no upper limit of supply from the power grid. This way, the grid can supply the Charging
Station with any amount of requested energy.

_Assumption 5_: The maximum charging supply of each EV is dictated by charging/discharging rate of the station.

## Installation-Requirements
In order to install, download the zip file or use git.
Open project, choose system interpreter and follow the command:

```console
cd Chargym-Charging-Station
pip install -e .
```


Refer to [requirements.txt](requirements.txt) for a list of Python library dependencies. You may install the required libraries by executing the following command:
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
            ├── Simulate_Actions.py
            ├── Simulate_RBC.py
            └── Station_simulation.py

          └── __init__.py

        └── Solvers
          └── main.py



- [Energy_Calculations.py](/Chargym_Charging_Station/utils/Energy_Calculations.py): more will be included.
- [Init_Values.py](/Chargym_Charging_Station/utils/Init_Values.py): more will be included.
- [Simulate_Actions.py](/Chargym_Charging_Station/utils/Simulate_Actions.py): more will be included.
- [Simulate_RBC.py](/Chargym_Charging_Station/utils/Simulate_RBC.py): more will be included.
- [Station_simulation.py](/Chargym_Charging_Station/utils/Station_simulation.py): more will be included.

- [Charging_Station_Enviroment.py](/Chargym_Charging_Station/envs/Charging_Station_Enviroment.py): more will be included.

- [main.py](/Chargym-Charging-Station/Solvers/main.py): more will be included.


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

The reward function is described in either [Simulate_RBC.py](/gym_Charging_Station/Simulate_RBC.py) (for control_flag=0) or [Simulate_Actions.py](/gym_Charging_Station/Simulate_Actions.py) (for case control_flag=1).
```RBC_Cost``` is the reward function, which is the multiplication of the amount of energy used from the power grid with the current price of KWh (RBC_Cost = Grid_final*self.Energy["Price"][0,hour]).

## How to run-Test example
Chargym is designed to work with different controller approaches as mentioned above, including RBC, MPC, RL or other intelligent controllers. 
The charging station environment and its interface is provided together with a Rule Based Controller (see __Chargym Description__). 
Also, we provide simple examples using well-known Reinforcement Learning approaches to present ready to run examples
that are easy for users and practictioners to use.

### Custom implementation
In case that the user wants to check his/her own controller than the provided ones, import Chargym and then
call the make method specifying the name of the model (__ChargingEnv-v0__) as in other gym environment.
```
import gym
import Chargym_Charging_Station
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--env", default="ChargingEnv-v0") 
args = parser.parse_args()
env = gym.make(args.env)

```

### Ready to Use Examples

__EXAMPLES WILL BE PRESENTED WITH FIGURES HERE__


# Citation
If you find this useful for your research, please use the following:
```
Chargym: An EV Charging Station Model Library for Controller Benchmarking

```

## Link
If you are interested in ongoing or future working projects of ConvCAO research group in various fields,
please visit: [ConvCAO Page](https://convcao.com/).

## License
The MIT License (MIT) Copyright (c) 2022, ConvCAO research group, CERTH, Greece

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

