import numpy as np
from Setup import * # import all back-end content
import matplotlib.pyplot as plt
"""
main simulation loop, graphing, cache files, printed output and Keplers validation 
RUN THIS ONE!! 
"""

# initialise time, percentage counter (progress) 
time = 0
progress = 0
no_planets = len(bodies)    # used for user feedback

# graphs here as dependant on both simulation parameters, as well as setup params (imported)
# here so graphs can be re-run from pkl

def orbits2D(): # 2D orbit graph
    fig=plt.figure(figsize=(3.5,2.6),dpi=200)
    ax=fig.add_subplot(1,1,1)
    ax.set_xlabel(r'$x$ (au)')
    ax.set_ylabel(r'$y$ (au)')
    for name in xpos:
        x = np.array(xpos[name]) /149597870700  # from NASA, converted to AU
        y= np.array(ypos[name]) /149597870700
        ax.plot(x, y, label = name, lw=0.4)
    ax.legend()
    #plt.savefig("2DorbitsV_3600_170y.svg")     # commented out unless explicitly needed
    plt.show()

def EnergyCons():
    fig=plt.figure(figsize=(3.5,2.6),dpi=200)
    ax=fig.add_subplot(1,1,1)
    ax.set_xlabel(r'$t$ (s)')
    ax.set_ylabel(r'$E$ (J)')
    ax.plot(timeLog, totalEnergy, label="Total Energy", lw=0.4)
    ax.legend()
   # plt.savefig("EnergyConsV_3600_170y.svg")
    plt.show()

def EnergyCons2():  # shows  components of kinetic and potential separately
    fig=plt.figure(figsize=(3.5,2.6),dpi=200)
    ax=fig.add_subplot(1,1,1)
    ax.set_xlabel(r'$t$ (s)')
    ax.set_ylabel(r'$E$ (J)')
    ax.plot(timeLog, kineticEnergy, label="Kinetic E", lw=0.4)
    ax.plot(timeLog, potentialEnergy, label="Potential E", lw=0.4)
    ax.legend()
   # plt.savefig("EnergyConsV_3600_170y.svg")
    plt.show()

def LinearMomCons():    
    fig=plt.figure(dpi=200)
    ax=fig.add_subplot(1,1,1)
    ax.set_xlabel(r'$t$ (s)')
    ax.set_ylabel(r'$\rho$ $(kg m s^{-1})$')
    ax.plot(timeLog, linearMom, label="Linear Momentum", lw=1)
    ax.legend()
   # plt.savefig("LinMomentumV_3600_170y.svg")
    plt.show()

def AngMomCons():
    fig=plt.figure(dpi=200)
    ax=fig.add_subplot(1,1,1)
    ax.set_xlabel(r'$t$ (s)')
    ax.set_ylabel(r' L $(kg m^{2} s^{-1})$')
    ax.plot(timeLog, angularMom, label="Angular Momentum", lw=0.4)
    ax.legend()
   # plt.savefig("AngMomentumV_3600_170y.svg")
    plt.show()
 
def orbits3D():     # purely for cool factor, not a practical graph
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    for name in xpos:
        # change units to astronomical units
        xx = np.array(xpos[name]) /149597870700
        yy= np.array(ypos[name]) /149597870700
        zz = np.array(zpos[name]) /149597870700
        ax.plot(xx, yy, zz, label = name, lw=0.4) 
    ax.set_xlabel(r'$x$ (au)')
    ax.set_ylabel(r'$y$ (au)')
    ax.set_zlabel(r'$z$ (au)')
    ax.legend()
    plt.show()

clear_terminal() # clears post setup
# string to print simulation settings back to user 
print(planets)
print(f"running the simulation for {no_planets} bodies, {years} years, with a time step of {deltaT} seconds. ")
print(f"(This will run for {iterations} iterations)")
if method == 1:
    print("You have chosen the Euler (forward) Method!\n")
elif method == 2:
    print("You have chosen the Euler-Cromer Method!\n")
elif method ==3:
    print("You have chosen the Verlet Method!\n")


rerun = input("Do you want to re-run the simulation ? (y/n):\n" # option to rerun or graph based on last cached data
              "(note if this is first run no data will be cached - cache is based on last run ONLY)\n").strip().lower()

if rerun == "y":
    for i in range(iterations): # main simulation loop

        timeLog.append(time)    # add time to empty list to graph
        
        total_momentum = np.array([0.0, 0.0, 0.0])  # initialise total momentum to 0 for each loop, just in case :)

        for particle in bodies:                                   # grav accel updated for all bodies first
            particle.updateGravaccel(bodies)

        if method == 3:                                           # method update loops 
            particle.updateVerlet(bodies, deltaT)      # verlet already takes body input, no need for loop
        for particle in bodies:

            if method == 1:
                particle.updateE(deltaT)
            elif method == 2:
                particle.updateEC(deltaT)
            
            xpos[particle.name].append(particle.position[0])        # updates xyz dictionaries to plot orbits
            ypos[particle.name].append(particle.position[1])
            zpos[particle.name].append(particle.position[2])
            
        time += deltaT                                                                 # incriments time step 
        
        linear_momentum = sum(particle.linearMomentum() for particle in bodies)     # sums vector momentums     
        linearMom.append(np.linalg.norm(linear_momentum))                                     # appends norm of vector totals
    # 
        angularMomentum = np.sum([np.float64(particle.angularMomentum()) for particle in bodies], axis=0)   # same procedure for angular 
        angularMom.append(np.float64(np.linalg.norm(angularMomentum)))

        kinetic_energy = np.float64(0.0)           # energies intialised to 0
        potential_energy =np.float64(0.0)
        total_energy = np.float64(0.0)
        kinetic_energy = sum(body.kineticEnergy() for body in bodies)   # sums Kinetic for each body, then appends to list 
        kineticEnergy.append(kinetic_energy)

        potential_energy = sum(0.5 * body.potentialEnergy(bodies) for body in bodies)       # sums Kinetic for each body, then appends to list, halved to avoid double interactions, i.e. 1 on 2 AND 2 on 1
        potentialEnergy.append(potential_energy)
        for p in bodies:    
            total_energy += np.float64(p.kineticEnergy() + 0.5 * p.potentialEnergy(bodies))    # total energy is kinetic + potential
        totalEnergy.append(np.float64(total_energy))

        tenpercent = (iterations) / 10                                                                                       # calculate 10%
        
        if i % tenpercent < 1:                                                                                                    # if roughly 10% has passed, increase counter by 10 and print %
            print(f"{progress}%")
            progress += 10
        if i % 1000 == 0:                                                                                                           # take other data readings every 1000 iteration for output txt file
            timeLogS.append(time)
            totalEnergyS.append(np.float64(total_energy))
            linearMomS.append(np.linalg.norm(linear_momentum))
            angularMomS.append(np.float64(np.linalg.norm(angularMomentum)))
    print("The simulation has finished")        
    print("Storing data please wait....")                                                                       
    data_store = {                              # dictionary of all important graphing data defined
        "timeLog" : timeLog,
        "linearMom" : linearMom,
        "angularMom" : angularMom, 
        "totalEnergy" : totalEnergy,
        "kineticEnergy": kineticEnergy,
        "potentialEnergy" : potentialEnergy,
        "xpos" : xpos,
        "ypos" : ypos,
        "zpos" : zpos  }
    save_pickle(data_store)              # dumped to pkl file
    
    print("Kepler's law orbits:\n")    # keplers printed to terminal for quick validation of method
    orbit_list = Kepler_three()
    for j in range(len(orbit_list)):
        print(orbit_list[j])

elif rerun == "n":                          # if simulation isnt run, load pkl cached data from prev run
    print("Using cached data (from last full run) if available")
    loaded_data = load_pickle()                 # var re-assinged as same names, but from file
    timeLog = loaded_data["timeLog"]
    linearMom = loaded_data["linearMom"]
    angularMom =loaded_data["angularMom"]
    totalEnergy = loaded_data["totalEnergy"]
    kineticEnergy = loaded_data["kineticEnergy"]
    potentialEnergy = loaded_data["potentialEnergy"]
    xpos = loaded_data["xpos"]
    ypos = loaded_data["ypos"]
    zpos = loaded_data["zpos"]

else:
    print("Invalid input! Please enter 'y' or 'n'.")
    
graphs = input("would you like to produce graphs relating to the simulation data? (y/n):\n").strip().lower()    # graphs produced on request
if graphs == "y":   # graphs as defined top 
    orbits2D()
    orbits3D()
    EnergyCons()
    EnergyCons2()
    LinearMomCons()
    AngMomCons()
elif graphs == "n":
    print("no graphs will be printed")
else:
    print("Invalid input! Please enter 'y' or 'n'.")


with open(r'final_project\output.txt', 'w') as f:   # handles writing to text output file
    for j in range(len(timeLogS)):
        f.write(f" time {timeLogS[j]} \n system total energy {totalEnergyS[j]} \n total linear momentum {linearMomS[j]} \n and total angular momentum {angularMomS[j]}\n \n")   # total energies, momentum and ang. momentum printed every 1000 iteration to file
    print("\n", file = f)
    print("system totals", file = f)
    linearMom.sort()    # lists sorted to take max and min values for linear, ang momentum and energy
    print(f"Minimum linear momentum: {linearMom[0]} \n Maximum linear momentum: {linearMom[-1]} \n", file = f )
    print("\n", file = f)
    totalEnergy.sort()
    print(f"Minimum total Energy: {totalEnergy[0]} \n Maximum total Energy: {totalEnergy[-1]} \n", file = f )
    print("\n", file = f)
    angularMom.sort()
    print(f"Minimum angular momentum: {angularMom[0]} \n Maximum angular momentum: {angularMom[-1]} \n", file = f )



