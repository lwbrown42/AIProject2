import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import math

def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax, type, numQuit):

    #########################
    # Setup for the plot    #
    #########################
    if type == 0:
        fig = plt.figure()
        ax = fig.gca(projection = '3d')
        x = np.arange(xmin, xmax, .05)
        y = np.arange(ymin, ymax, .05)
        X, Y = np.meshgrid(x,y)
        zs = np.array([math_function(x,y) for x,y in zip(np.ravel(X), np.ravel(Y))])
        Z = zs.reshape(X.shape)
        
        ax.set_xlabel("x axis")
        ax.set_ylabel("y axis")
        ax.set_zlabel("z axis")

    ###############################
    # Do the actual hill climbing #
    ###############################
    xCoord = random.uniform(xmin, xmax)
    yCoord = random.uniform(ymin, ymax)

    current = function_to_optimize(xCoord, yCoord)

    noMove = 0

    xValues = [xCoord]
    yValues = [yCoord]
    zValues = [current]
    
    while noMove < numQuit:
        #check our directions
        xPlus = function_to_optimize(xCoord+step_size, yCoord)
        xMinus = function_to_optimize(xCoord-step_size, yCoord)
        yPlus = function_to_optimize(xCoord, yCoord+step_size)
        yMinus = function_to_optimize(xCoord, yCoord-step_size)
          
        moveMade = False
  
        xValues.append(xCoord)
        yValues.append(yCoord)
        zValues.append(current)

        newPath = random.randint(1,4)

        # pick a path at random and go!
        if newPath == 1:
            if xPlus < current and (xCoord + step_size) <= xmax:
                current = xPlus
                xCoord += step_size
                noMove = 0
                moveMade = True
        elif newPath == 2:
             if xMinus < current and (xCoord - step_size) >= xmin:
                current = xMinus
                xCoord -= step_size
                noMove = 0
                moveMade = True
        elif newPath == 3:
            if yPlus < current and (yCoord + step_size) <= ymax:
                current = yPlus
                yCoord += step_size
                noMove = 0
                moveMade = True
        elif newPath == 4:
            if yMinus < current and (yCoord + step_size) >= ymin:
                current = yMinus
                yCoord += step_size
                noMove = 0
                moveMade = True
        if moveMade == False:
            noMove += 1

    if type == 0:

        plt.plot(xValues, yValues, zValues, "ro")
        ax.plot_surface(X,Y,Z)
        plt.show()

    return xCoord, yCoord, current

def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax, numQuit):

    resultsList = []

    for i in range(num_restarts):
        resultsList.append(hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax, 1, numQuit))

    return min(resultsList)

def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax, cooldown):
    
    xCoord = random.uniform(xmin, xmax)
    yCoord = random.uniform(ymin, ymax)

    current = function_to_optimize(xCoord, yCoord)
    temp = max_temp

    best = current

    while temp > 0.000001:
        temp = temp*cooldown

        # come up with new random spot
        newX = random.uniform(xmin, xmax)
        newY = random.uniform(ymin, ymax)
        
        # check if it's better
        newFitness = function_to_optimize(xCoord, yCoord)

        probability = math.exp((newFitness - current)/temp) 
 
        if best > newFitness:
            best = newFitness
        elif probability > random.random():
            best = newFitness

    return best
    

def math_function(x, y):

    r = (x**2 + y**2) ** (.5)

    z = (math.sin(x**2 + (3 * y**2 )/(.1 + r**2))) + (x**2 + (5 * y**2)) * (math.exp(1 - r**2)/2)

    return z

def main():

    x,y,z = hill_climb(math_function, .05, -2.5, 2.5, -2.5, 2.5, 0, 10)
    print("Hill Climbing Results - x = ", x, " y = ", y, " z = ", z)

    x,y,z = hill_climb_random_restart(math_function, .05, 10000,  -2.5, 2.5, -2.5, 2.5, 10)
    print("Hill Climbing w/ Restarts Results - x = ", x, " y = ", y, " z = ", z)

    z = simulated_annealing(math_function, .05, 1000, -2.5, 2.5, -2.5, 2.5, .999)
    print("Simulated Annealing Results: z = ", z)

main()
