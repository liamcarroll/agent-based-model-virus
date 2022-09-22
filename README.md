# Agent-based Model in Python Simulating Virus Spread

The model which I intend to build will simulate the spread of a virus through a community. The community will consist of a user-specified population of agents who move and
encounter other agents in a stochastic manner. Initially, there will be a user-defined population of ‘infected’ agents and at each time step, a randomly selected cohort of agents
will move and encounter other agents. The number of agents which move on each iteration is bounded by two parameters and a random value in this range is selected on each iteration. If an agent comes into contact with an agent who is infected (i.e. the agents are within a certain collision distance; another user-specified parameter), they themselves will
become infected for a period of time. Currently, this period is set to 14 time steps but this is
another parameter of the model which can be altered for experimental purposes.

There are a number of probabilities which will be associated with the model:
- **Susceptible probability:** The probability that an agent is susceptible to the virus. Upon initialisation, some agents will be immune to the virus.
- **Immunity probability:** The probability that an agent becomes immune to the virus after having been infected. In general, once infected, most agents become immune
to a virus once they recover. However, this is not always the case.
- **Death probability:** The probability that an agent who becomes infected dies from the virus.

Again, these probabilities are defined by the user so different configurations of these
probabilities can be tested.

## Running a simulation

To run a simulation, follow the below steps:

1. Alter the parameters if desired in the *abm-virus.py* file. The CSV files which produce the time-based graphs of output results are produced after each simulation. The directory in which these CSV files are stored can be altered using the *path_out* variable in the *abm-virus.py* file.

2. Simply run:
```
python abm-virus.py
```
while in the current directory.
