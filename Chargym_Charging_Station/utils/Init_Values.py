import numpy as np
from numpy import random
import scipy.io


def InitialValues_per_day(self):
    number_of_cars=self.number_of_cars
    ArrivalT=[]
    DepartureT=[]
    BOC=np.zeros([number_of_cars,25])
    present_cars=np.zeros([number_of_cars,25])
    #initial state stochastic creation

    for car in range(number_of_cars):
        present=0
        pointer=0
        Arrival_car=[]
        Departure_car=[]


        for hour in range(24):

            if present == 0:
                arrival=round(random.rand()-0.1)
                if arrival==1 and hour<=20:
                    ran = random.randint(20, 50)
                    BOC[car, hour] = ran / 100
                    pointer=pointer+1
                    Arrival_car.append(hour)
                    upper_limit=min(hour + 10, 25)
                    Departure_car.append(random.randint(hour+4,int(upper_limit)))



            if arrival == 1 and pointer > 0:
                if (hour < Departure_car[pointer-1]):
                    present = 1
                    present_cars[car,hour] = 1
                else:
                    present = 0
                    present_cars[car, hour] = 0
            else:
                present = 0
                present_cars[car, hour] = 0

        ArrivalT.append(Arrival_car)
        DepartureT.append(Departure_car)

    #information vector creator
    evolution_of_cars=np.zeros([24])
    for hour in range(24):
        evolution_of_cars[hour]=np.sum(present_cars[:,hour])

 

    return BOC, ArrivalT, DepartureT,evolution_of_cars,present_cars