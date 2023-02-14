import numpy as np
import time



def simulate_clever_control(self,actions):
    hour=self.timestep
    Consumed=self.Energy['Consumed']
    Renewable=self.Energy['Renewable']
    present_cars = self.Invalues['present_cars']
    #print(present_cars[:,hour])

    leave=self.leave
    BOC=self.BOC

    P_charging=np.zeros(self.number_of_cars)
    # Calculation of demand based on actions
    # Calculation of actions for cars
    # ----------------------------------------------------------------------------
    for car in range(self.number_of_cars):
        if actions[car] >=0:
            max_charging_energy = min([10,(1-BOC[car,hour])*self.EV_Param['EV_capacity']])
        else:
            max_charging_energy = min([10, BOC[car, hour] * self.EV_Param['EV_capacity']])
        # in case action=[-100,100] P_charging[car] = actions[car]/100*max_charging_energy otherwise if action=[-1,1] P_charging[car] = 100*actions[car]/100*max_charging_energy

        #P_charging[car] = actions[car]/100*max_charging_energy
        #P_charging[car] = 100 * actions[car] / 100 * max_charging_energy
        if present_cars[car, hour] == 1:
            P_charging[car] = 100*actions[car]/100*max_charging_energy
        else:
            P_charging[car] = 0

    # Calculation of next state of Battery based on actions
    # ----------------------------------------------------------------------------
    for car in range(self.number_of_cars):
        if present_cars[car,hour] == 1:
            BOC[car,hour+1] = BOC[car,hour] + P_charging[car]/self.EV_Param['EV_capacity']



    # Calculation of energy utilization from the PV
    # Calculation of energy coming from Grid
    # ----------------------------------------------------------------------------
    RES_avail = max([0,Renewable[0,hour] - Consumed[0,hour]])
    Total_charging = sum(P_charging)

    # First Cost index
    # ----------------------------------------------------------------------------
    Grid_final = max([Total_charging - RES_avail, 0])
    Cost_1 = Grid_final*self.Energy["Price"][0,hour]

    # Second Cost index
    # Penalty of wasted RES energy
    # This is not used in this environment version
    # ----------------------------------------------------------------------------
    # RES_avail = max([RES_avail-Total_charging, 0])
    # Cost_2 = -RES_avail * (self.Energy["Price"][0, hour]/2)

    #Third Cost index
    #Penalty of not fully charging the cars that leave
    # ----------------------------------------------------------------------------
    Cost_EV =[]
    for ii in range(len(leave)):
        Cost_EV.append(((1-BOC[leave[ii], hour+1])*2)**2)
    Cost_3 = sum(Cost_EV)



    Cost = Cost_1 + Cost_3

    return Cost,Grid_final,RES_avail,Cost_3,BOC
