import os
from FourRooms import FourRooms
import numpy as np
import random 

#CONSTANTS
EPOCHS      = 5000
E_GREEDY    = 0.6  
DEC_RATE    = 0.8  
DISCOUNT    = 0.4

# Q table
Q = np.zeros((169, 4, 4))
# R table
R = np.zeros((169, 4, 4))

def main():

    # Create FourRooms Object
    fourRoomsObj = FourRooms('multi')

    # This will try to draw a zero
    actSeq = [FourRooms.LEFT, FourRooms.LEFT, FourRooms.LEFT,
              FourRooms.UP, FourRooms.UP, FourRooms.UP,
              FourRooms.RIGHT, FourRooms.RIGHT, FourRooms.RIGHT,
              FourRooms.DOWN, FourRooms.DOWN, FourRooms.DOWN]

    aTypes = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

    print('....Starting Simulation for agent....')
    print('....Agent starts at',fourRoomsObj.getPosition() )
    


    for act in actSeq:
        gridType, newPos, packagesRemaining, isTerminal = fourRoomsObj.takeAction(act)

        if isTerminal:
            break

    for k in range(EPOCHS):
        
        fourRoomsObj.newEpoch()

        prevPos = fourRoomsObj.getPosition()
        
        visited = np.array([np.array([[0,0,0,0] for i in range(4)]) for i in range(169)])

        E = E_GREEDY
        packleft = 3

        print("Training... Epoch ", k, "/", EPOCHS,"")
        while not fourRoomsObj.isTerminal():
            index = prevPos[0] + prevPos[1]*13
            

            if random.random() < E:
                action = random.randint(0,3)
                visited[index][packleft][action] += 1 
                CellType, newPos, numpack, terminal =fourRoomsObj.takeAction(action)
            else:

                choices = []
                action = 0
                for i in range(4):

                    if Q[index][packleft][i] == max(Q[index][packleft]):
                        choices.append(i)
                        
                action = choices[random.randint(0,len(choices)-1)]
                visited[index][packleft][action] += 1
                
                CellType, newPos, numpack, terminal = fourRoomsObj.takeAction(action)
          
            index = prevPos[0] + prevPos[1]*13
            
            #if action hit a wall
            if prevPos == fourRoomsObj.getPosition():
                R[index][packleft][action] -= 2
            
            #if action hit the package
            elif (CellType == 1 or CellType == 2 or CellType == 3):
                if CellType == (4 - packleft):
                    
                    R[index][packleft][action] = 1000
                    R[fourRoomsObj.getPosition()[1]*13 + fourRoomsObj.getPosition()[0]][packleft] = [0,0,0,0]
                else:
                    R[index][packleft][action] -= 5

            index = prevPos[0] + prevPos[1]*13

            l_rate = 1/(1 + visited[index][packleft][action])

            Q[index][packleft][action] +=  l_rate*(R[index][packleft][action] + DISCOUNT*(max(Q[fourRoomsObj.getPosition()[0] + fourRoomsObj.getPosition()[1]*13][packleft])) - Q[index][packleft][action]) - visited[index][packleft][action]
            

            prevPos = fourRoomsObj.getPosition()

            if CellType > 0:
                #E = E_GREEDY
                packleft -= 1
            else:
                E *= DEC_RATE
            #update learning rate

    print()
    print('....Training done.....')
    print('....Showing path......')
    fourRoomsObj.showPath(-1)


if __name__ == "__main__":
    main()

