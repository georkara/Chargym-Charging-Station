import numpy as np

def Simulate_Station(self):

    BOC = self.BOC
    Arrival=self.Invalues['ArrivalT']
    Departure=self.Invalues['DepartureT']
    present_cars=self.Invalues['present_cars']
    number_of_cars=self.number_of_cars
    day=self.day
    hour=self.timestep


    # calculation of which cars depart now
    leave=[]
    if hour < 24:
        for car in range(number_of_cars):
            Departure_car=Departure[car]
            if present_cars[car,hour] == 1 and (hour+1 in Departure_car):
                leave.append(car)

    # calculation of the hour each car is leaving
    Departure_hour = []
    for car in range(number_of_cars):
        if present_cars[car,hour] == 0:
            Departure_hour.append(0)
        else:
            for ii in range(len(Departure[car])):
                if hour<Departure[car][ii]:
                    Departure_hour.append(Departure[car][ii]-hour)
                    break

    # calculation of the BOC of each car
    Battery=[]
    for car in range(number_of_cars):
        Battery.append(self.BOC[car,hour])


    return leave,Departure_hour,Battery
