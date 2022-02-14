import numpy as np

def bulubas_seperate(self):

    BOC = self.BOC
    Arrival=self.Invalues['ArrivalT']
    Departure=self.Invalues['DepartureT']
    present_cars=self.Invalues['present_cars']
    number_of_cars=self.number_of_cars
    day=self.day
    hour=self.timestep


    # calculation of which cars depart the next two hours
    pointer=[]
    for car in range(number_of_cars):
        Departure_car=Departure[car]
        if present_cars[car,hour] and ((hour+1 in Departure_car) or (hour+2 in Departure_car)):
            if len(Departure_car) > 1:
                if Departure_car[-2] < hour and Departure_car[-1] == 25:
                    zero=0
                else:
                    pointer.append(car)
            else:
                if Departure_car[-1] == 25:
                    zero = 0
                else:
                    pointer.append(car)

    Pdemand=[]
    for ii in pointer:
        a=(1 - BOC[ii, hour])* 20
        Pdemand.append(min(10,a))

    Battery = 0
    pointer2 = []
    for car in range(number_of_cars):

        if present_cars[car, hour] == 1:
            a = (BOC[car, hour]) * 20
            Battery = min(a,10) + Battery
            pointer2.append(car)

    for ii in pointer:
        a=(BOC[ii, hour])* 20
        Battery=Battery-(min(10,a))



    leave = pointer
    stay=[]
    for xx in pointer2:
        if (xx in leave)==0:
            stay.append(xx)


    Battery = max(0,Battery)
    BOC_stay = []
    stay_new = []
    for ii in range(len(stay)):
        BOC_stay.append(BOC[stay[ii], hour])


    indd=sorted(range(len(BOC_stay)), key=lambda k: BOC_stay[k])
    for ii in range(len(stay)):
        stay_new.append(stay[indd[ii]])




    return Battery, Pdemand, stay_new, leave, BOC
