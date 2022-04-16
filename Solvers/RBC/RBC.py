import numpy as np


class RBC:

    def select_action(self, states):
        action=[0,0,0,0,0,0,0,0,0,0]
        for car in range(self.number_of_cars):
            #the departure hour for every spot is placed on the last 10 positions in states vector(10 spots)
            #have in mind that departure time is normalized in [0,1] so if T_leave is within the next 3 hours then
            #action[car]=1, else action[car]=solar_radiation or action[car]={mean value of solar radiation and the predicted one hour radiation}
            if states[18+car]==0:
                action[car]=0
            elif states[18+car]>0 and states[18+car]<0.16667:
                action[car]=1
            else:
                #solar ratiation is states[0] and the predictions on ratiation are states[2],states[3],states[4]

                #this case describes that if T_leave> 3 hours, then scenario 1: action is equal to the radiation
                #scenario 2: action is equal to the mean value of current radiation and its next hour prediction

                # scenario 1, current value of radiation
                #action[car]=states[0]

                # scenario 2, mean value of current radiation and one hour ahead
                action[car]=(states[0] + states[2]) / 2


        return action
