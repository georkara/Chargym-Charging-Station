import numpy as np
import os
import sys
import gym
import pathlib
from gym import spaces
from gym.utils import seeding
from scipy.io import loadmat, savemat
from Chargym_Charging_Station.utils import Energy_Calculations
from Chargym_Charging_Station.utils import Station_simulation
from Chargym_Charging_Station.utils import Init_Values
from Chargym_Charging_Station.utils import Simulate_RBC
from Chargym_Charging_Station.utils import Simulate_Actions
import time



class ChargingEnv(gym.Env):
    def __init__(self, price=1, solar=1,control_flag=1):
        # basic_model_parameters
        self.number_of_cars = 10
        self.number_of_days = 1
        self.price_flag = price
        self.solar_flag = solar
        self.done = 0
        self.control_mode = control_flag
        # EV_parameters
        EV_capacity = 30
        charging_effic = 0.91
        discharging_effic = 0.91
        charging_rate = 11
        discharging_rate = 11
        self.EV_Param = {'charging_effic': charging_effic, 'EV_capacity': EV_capacity,
                         'discharging_effic': discharging_effic, 'charging_rate': charging_rate,
                         'discharging_rate': discharging_rate}

        # Battery_parameters
        Battery_Capacity = 20
        Bcharging_effic = 0.91
        Bdischarging_effic = 0.91
        Bcharging_rate = 11
        Bdischarging_rate = 11
        self.Bat_Param = {'Battery_Capacity': Battery_Capacity, 'Bcharging_effic': Bcharging_effic,
                          'Bdischarging_effic': Bdischarging_effic, 'Bcharging_rate': Bcharging_rate,
                          'Bdischarging_rate': Bdischarging_rate}

        # Renewable_Energy
        PV_Surface = 2.279 * 1.134 * 20
        PV_effic = 0.21

        self.PV_Param = {'PV_Surface': PV_Surface, 'PV_effic': PV_effic}

        #self.current_folder = os.getcwd() + '\\utils\\Files\\'
        self.current_folder=os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))+ '\\Files\\'

        low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
        high = np.array([1000,0.3*1000,1000,1000,1000,0.3*1000,0.3*1000,0.3*1000,100,100], dtype=np.float32)
        self.action_space = spaces.Box(
            low=0,
            high=100, shape=(1,),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=low,
            high=high,
            dtype=np.float32
        )

        self.seed

    def step(self, actions):

        conditions=self.get_obs()

        if self.control_mode == 0:
            [reward,Grid,self.BOC] =Simulate_RBC.simulate_rbc(self,actions)
            self.Grid_evol.append(Grid)
        if self.control_mode == 1:
            [reward, Grid, self.BOC]=Simulate_Actions.simulate_clever_control(self,actions)
            self.Grid_evol.append(Grid)
        self.Cost_History.append(reward)
        self.timestep = self.timestep + 1
        if self.timestep == 24:
            self.done = 1
            self.timestep = 0
            Results = {'BOC': self.BOC, 'Grid_Final':self.Grid_evol,'Pdemand_final':self.Pdemand_evol,'Renewable':self.Energy['Renewable'],'Cost_History':self.Cost_History}
            savemat(self.current_folder +'\Results.mat',{'Results':Results})

        self.info={}
        return conditions,reward,self.done,self.info

    def reset(self,reset_flag=1):
        self.timestep = 0
        self.day = 1
        self.done = 0
        Consumed, Renewable, Price, Radiation = Energy_Calculations.Energy_Calculation(self)
        self.Energy = {'Consumed': Consumed, 'Renewable': Renewable,
                       'Price': Price, 'Radiation':Radiation}
        if reset_flag==0:
            [BOC, ArrivalT, DepartureT, evolution_of_cars, present_cars] = Init_Values.InitialValues_per_day(self)
            self.Invalues = {'BOC': BOC, 'ArrivalT': ArrivalT, 'evolution_of_cars': evolution_of_cars,
                             'DepartureT': DepartureT, 'present_cars': present_cars}
            savemat(self.current_folder + '\Initial_Values.mat',  self.Invalues)
        else:
            contents=loadmat(self.current_folder+'\Initial_Values.mat')
            self.Invalues = {'BOC': contents['BOC'], 'Arrival': contents['ArrivalT'][0],
                             'evolution_of_cars': contents['evolution_of_cars'], 'Departure': contents['DepartureT'][0],
                             'present_cars': contents['present_cars'], 'ArrivalT': [], 'DepartureT': []}
            for ii in range(self.number_of_cars):
                self.Invalues['ArrivalT'].append(self.Invalues['Arrival'][ii][0].tolist())
                self.Invalues['DepartureT'].append(self.Invalues['Departure'][ii][0].tolist())

        return self.get_obs()


    def get_obs(self):
        if self.timestep == 0:
            self.Grid_evol = []
            self.Battery_evol = []
            self.Pdemand_evol = []
            self.Cost_History = []
            self.BOC = self.Invalues["BOC"]

        [Battery, Pdemand, stay_new, leave, BOC] = Station_simulation(self)
        pointer = len(stay_new)
        if pointer == 0:
            pointer = 0.0000001
        self.Battery_evol.append(Battery / pointer / 20)
        self.Pdemand_evol.append(sum(Pdemand))
        self.Battery = Battery
        self.Pdemand = Pdemand
        self.stay_new = stay_new
        self.leave = leave
        self.BOC = BOC
        self.disturbances = self.Energy["Radiation"][0,self.timestep],self.Energy["Price"][0,self.timestep]*1000
        self.predictions = self.Energy["Radiation"][0,self.timestep+1:self.timestep+4],self.Energy["Price"][0,self.timestep+1:self.timestep+4]*1000
        self.states = self.Battery_evol[self.timestep]*100,self.Pdemand_evol[self.timestep]
        return np.array([self.disturbances[0],self.disturbances[1],self.predictions[0][0],self.predictions[0][1],self.predictions[0][2],
                         self.predictions[1][0],self.predictions[1][1],self.predictions[1][2],self.states[0],self.states[1]])

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def close(self):
        return 0
