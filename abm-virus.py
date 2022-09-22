#!"C:\Users\carro\anaconda3\envs\CA4024\python.exe"
"""
Script which outlines an ABM which models the spread of a virus through a community.
"""

import os
import sys
# sys.path.append('C:/Users/carro/Documents/College_YR4_Code/CA4024_BCCM/PyCX')
import pycxsimulator
from pylab import *
import pandas as pd

# Size of grid
height = 1000
width = 1000

# Number of agents
pop = 5000

# Number of agents initially infected
infected_init = 2500
# Probability of being susceptible to the virus
susceptible_prob = 0.95
# Probability of becoming immune to the virus after having it
immunity_prob = 0.5
# Probability of dying while infected
death_prob = 0.05

# Lower bound of moving agents
movers_lower = 50
# Upper bound of moving agents
movers_upper = 500
# Magnitude of movement of agents
mag = 5
# Radius for collision detection
cd = 2
cdsq = cd ** 2

# Initialise parameters to track
deaths = 0
cases = infected_init
immune = 0

deaths_df = []
cases_df = []
immune_df = []

# Output path
path_out = './data/sim4'


class agent:
    pass


def initialise():
    global time, agents, deaths, cases, immune

    time = 0

    # Initialise agent pop
    agents = []
    for i in range(pop - infected_init):
        ag = agent()
        ag.state = 's' if random() < susceptible_prob else 'im'
        if ag.state == 'im':
            immune += 1
        # -1 indicates that the agent is not currently infected
        ag.infected_time = -1
        ag.x = uniform(0, width)
        ag.y = uniform(0, height)
        agents.append(ag)

    # Initialise infected agent pop
    for i in range(infected_init):
        ag = agent()
        ag.state = 'in'
        # Random infection time left
        ag.infected_time = randint(1, 14)
        ag.x = uniform(0, width)
        ag.y = uniform(0, height)
        agents.append(ag)

    # Initialising statistics
    deaths_df.append([time, deaths])
    cases_df.append([time, cases])
    immune_df.append([time, immune])


def observe():
    global time, agents
    cla()

    # Plotting infected
    infected = [ag for ag in agents if ag.state == 'in']
    if len(infected) > 0:
        x = [ag.x for ag in infected]
        y = [ag.y for ag in infected]
        plot(x, y, 'r.')

    # Plotting immune
    immune = [ag for ag in agents if ag.state == 'im']
    if len(immune) > 0:
        x = [ag.x for ag in immune]
        y = [ag.y for ag in immune]
        plot(x, y, 'g.')

    # Plotting susceptible
    susceptible = [ag for ag in agents if ag.state == 's']
    if len(susceptible) > 0:
        x = [ag.x for ag in susceptible]
        y = [ag.y for ag in susceptible]
        plot(x, y, 'k.')

    axis('image')
    axis([0, width, 0, height])


def update_one_agent():
    global agents, cases

    if len(agents) == 0:
        return

    ag = choice(agents)

    # Simulating random movement
    ag.x += uniform(-mag, mag)
    ag.y += uniform(-mag, mag)
    ag.x = 1000 if ag.x > 1000 else 0 if ag.x < 0 else ag.x
    ag.y = 1000 if ag.y > 1000 else 0 if ag.y < 0 else ag.y

    # Detecting collisions
    neighbours = [nb for nb in agents if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    # If current agent is infected, all neighbours become infected unless immune
    if ag.state == 'in':
        for nb in neighbours:
            if nb.state == 's':
                nb.state = 'in'
                nb.infected_time = 0
                cases += 1

    # If current agent is susceptible, it will become infected if any neighbours are infected
    elif ag.state == 's':
        infected_neighbours = [ag for ag in neighbours if ag.state == 'in']
        if len(infected_neighbours) > 0:
            ag.state = 'in'
            ag.infected_time = 0
            cases += 1

    # If current agent is immune, pass
    else:
        pass


def update():
    global time, agents, cases, deaths, immune

    time += 1

    # Increase infected agents time infected
    infected = [ag for ag in agents if ag.state == 'in']
    for ag in infected:
        ag.infected_time += 1

    # Change agents who have been infected for 14 days to either immune/susceptible
    recovered = [ag for ag in agents if ag.infected_time == 14]
    # Subtract number of recovered from current cases
    cases -= len(recovered)
    for ag in recovered:
        # Random chance of death after infection
        if random() < death_prob:
            agents.remove(ag)
            # Add to deaths total
            deaths += 1
        ag.infected_time = -1

        # Change to immune with certain probability
        if random() < immunity_prob:
            ag.state = 'im'
            # Add to immune total
            immune += 1
        else:
            ag.state = 's'

    # Choose a random number of agents which will move
    movers = randint(movers_lower, movers_upper)
    for i in range(movers):
        update_one_agent()

    # Collecting statistics
    deaths_df.append([time, deaths])
    cases_df.append([time, cases])
    immune_df.append([time, immune])


pycxsimulator.GUI().start(func=[initialise, observe, update])

pd.DataFrame.from_records(deaths_df, columns=['time', 'deaths']).to_csv(os.path.join(path_out, 'deaths.csv'), index=False)
pd.DataFrame.from_records(cases_df, columns=['time', 'cases']).to_csv(os.path.join(path_out, 'cases.csv'), index=False)
pd.DataFrame.from_records(immune_df, columns=['time', 'immune']).to_csv(os.path.join(path_out, 'immune.csv'), index=False)
