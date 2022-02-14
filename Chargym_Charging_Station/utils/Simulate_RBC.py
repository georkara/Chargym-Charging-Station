import numpy as np
import time



def simulate_rbc(self,actions):
    hour=self.timestep
    Consumed=self.Energy['Consumed']
    Renewable=self.Energy['Renewable']

    Pdemand=self.Pdemand
    Battery=self.Battery
    stay=self.stay_new
    leave=self.leave
    Departure=self.Invalues['DepartureT']
    BOC=self.BOC

    Grid_evol_final=[]
    Pdemand_final=[]

    # excess of renewable# Calculation of  Energy   to  charge and calculation  of   how much   to take from cars
    if Consumed[0,hour] - Renewable[0,hour] <= 0:
        if (sum(Pdemand) >= Renewable[0,hour] - Consumed[0,hour]):
            aa=sum(Pdemand) - Renewable[0,hour] + Consumed[0,hour]
            Battery_Consumption = min([aa,Battery,  10 * len(stay)])
            Grid_current=sum(Pdemand) - Renewable[0,hour] + Consumed[0,hour] - Battery_Consumption
        else:
            Battery_Consumption = sum(Pdemand) - Renewable[0,hour] + Consumed[0,hour]
            # charging   of     the   stay cars...
            Grid_current=0
        for ii in range(len(leave)):
            if ((hour + 1 in Departure[leave[ii]])):
                BOC[leave[ii], hour + 1] = 1
            else:
                BOC[leave[ii], hour + 1] = BOC[leave[ii], hour] + Pdemand[ii] / 20
        if (Battery_Consumption >= 0):
            for ii in range(len(stay)):
                aa= BOC[stay[ii],hour]*20
                bb=Battery_Consumption / (len(stay) - (ii))
                change = min([10,aa,bb])
                Battery_Consumption = Battery_Consumption - change
                aa= BOC[stay[ii], hour] - change / 20
                BOC[stay[ii], hour + 1] = max([0,aa])
        else:
            for ii in range (len(stay)-1,-1,-1):
                aa=(1 - BOC[stay[ii], hour]) * 20
                bb=(-Battery_Consumption) / (len(stay) - (ii))
                change = min([10,aa,bb])
                Battery_Consumption = Battery_Consumption + change
                BOC[stay[ii], hour + 1] = BOC[stay[ii], hour] + change / 20

    else:
        Battery_Consumption = min([sum(Pdemand), Battery, 10 * len(stay)])
        Grid_current = sum(Pdemand) - Battery_Consumption

        #Calculation of new BOCs
        for ii in range(0,len(leave)):
            if (Departure(leave(ii))==hour+1):
                BOC[leave(ii),hour+1] = 1
            else:
                BOC[leave(ii),hour+1]=BOC[leave(leave(ii),hour)]+Pdemand(ii)/20
        for ii in range(len(stay)):
            BOC[stay[ii], hour + 1] = max([BOC(stay[ii], hour) - Battery_Consumption / len(stay) / 20 ,0])

    RBC_Cost = Grid_current*self.Energy["Price"][0,hour]

    return RBC_Cost,Grid_current,BOC






















