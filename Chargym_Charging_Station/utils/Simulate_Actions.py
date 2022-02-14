import numpy as np
import time



def simulate_clever_control(self,actions):
    hour=self.timestep
    Consumed=self.Energy['Consumed']
    Renewable=self.Energy['Renewable']

    Pdemand=self.Pdemand
    Grid_evol=self.Grid_evol
    Battery=self.Battery
    stay=self.stay_new
    leave=self.leave
    Departure=self.Invalues['DepartureT']
    BOC=self.BOC

    P_charging=np.zeros(self.number_of_cars)


    # Calculation of demand based on actions
    # Calculation of actions for the stay cars
    # ----------------------------------------------------------------------------

    for car in range(self.number_of_cars):
        max_charging_energy = min([10,(1-BOC[car,hour])*20])
        P_charging[car] = actions/100*max_charging_energy*int(car in stay)
    RES_avail = max([0,Renewable[0,hour] - Consumed[0,hour]])
    Grid_current_stay = max([sum(P_charging) - RES_avail, 0])

    for ii in range(len(stay)):
        BOC[stay[ii], hour + 1] = BOC[stay[ii],hour] + P_charging[stay[ii]]/20

    if range(len(stay)) == 0:
        Battery = 0
    else:
        Battery = 0
        for ii in range(len(stay)):
            Battery = Battery + min([10,BOC[stay[ii],hour+1]*20])

    # Calculation of actions for the leave cars
    # ----------------------------------------------------------------------------

    RES_avail = max([0, RES_avail - sum(P_charging)])
    Grid_current_leave = max([0, sum(Pdemand) - RES_avail - Battery])
    Battery_Consumption = max([0, sum(Pdemand) - RES_avail ])
    Battery_Consumption = min ([Battery_Consumption,Battery])

    # Calculation of new BOCs
    for ii in range(len(leave)):
        if (Departure[leave[ii]] == hour + 1):
            BOC[leave[ii], hour + 1] = 1
        else:
            BOC[leave[ii], hour + 1] = BOC[leave[ii], hour] + Pdemand[ii] / 20

    if (sum(Pdemand) - RES_avail) >=0:
        for ii in range(len(stay)):
            aa = BOC[stay[ii], hour+1] * 20
            bb = Battery_Consumption / (len(stay) - (ii))
            change = min([10, aa, bb])
            Battery_Consumption = Battery_Consumption - change
            aa = BOC[stay[ii], hour+1] - change / 20
            BOC[stay[ii], hour + 1] = max([0, aa])
            #BOC[stay[ii], hour + 1] = max([BOC[stay[ii], hour+1] - Battery_Consumption / len(stay) / 20, 0])
    else:
        Battery_Consumption = sum(Pdemand) - RES_avail
        for ii in range(len(stay) - 1, -1, -1):
            aa = (1 - BOC[stay[ii], hour+1]) * 20
            bb = (-Battery_Consumption) / (len(stay) - (ii))
            change = min([10, aa, bb])
            Battery_Consumption = Battery_Consumption + change
            BOC[stay[ii], hour + 1] = BOC[stay[ii], hour+1] + change / 20


    Grid_final = Grid_current_leave + Grid_current_stay
    RBC_Cost = Grid_final*self.Energy["Price"][0,hour]


    return RBC_Cost,Grid_final,BOC
