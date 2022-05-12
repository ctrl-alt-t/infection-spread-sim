import random
import math
import tkinter
import time

from sklearn import neighbors


class Population:
    """Contains all the People objects and their health status"""

    def __init__(self, grid_size, infected):
        """
        Constructor
        
        Parameters
        ----------
        grid_size : int
            Length of the side of the square grid that contains people.
        infected : int
            Number of people infected.
        """
        self.grid_size = grid_size
        self.infected = infected

        # 2d list of all people 
        self.people = [] 

    def create_people(self):
        """Creates the starting population based on a grid_size"""
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                person = Person()
                row.append(person)
            self.people.append(row)

    def initial_infection(self):
        """Initiates the infection based on the infected number"""
        initial_infected_people = random.sample(range(self.grid_size**2), self.infected)
        for grid_location in initial_infected_people:
            column = grid_location % self.grid_size
            row = grid_location // self.grid_size
            target_person = self.people[column][row]
            target_person.is_infected = True

    def get_stats(self):
        """
        Gets the total_infected, total_immune, total_dead of a population.

        Returns
        -------
        total_infected, total_immune, total_dead
            a tuple containing all relevant info of a population
        """
        total_infected = 0
        total_immune = 0
        total_dead = 0
        for group in self.people:
            for person in group:
                if person.was_infected:
                    total_infected+= 1
                if person.is_immune:
                    total_immune += 1
                if not person.is_alive:
                    total_dead += 1
        return total_infected, total_immune, total_dead

    def get_report(self):
        """
        Takes the population info from the get_stats functions and returns it as a formatted message.

        Returns
        -------
        msg : str
            Nicely formatted message containing all relevant population info.
        """
        total_infected, total_immune, total_dead = self.get_stats()
        size = self.grid_size ** 2
        return(f"""Simulation ended. Here are the stats:
        Infected: {total_infected}/{size}, {round(total_infected/size*100,2)}%.
        Immune: {total_immune}/{size}, {round(total_immune/size*100,2)}%.
        Dead: {total_dead}/{size}, {round(total_dead/size*100,2)}%.""")

class Virus:
    def __init__(self, risk, mortality, duration):
        """
        Constructor
        All inputs are converted to positive numbers and floored to 100 if larger value is provided
        
        Parameters
        ----------
        risk : int
            Chance of being infected in one day if you get in contact with the person.
        mortality : int
            Chance for a person to die if they get the disease.
        duration : int
            Duration of the infection in days. After that the person is immune.
        """
        self.risk = min(abs(risk), 100)
        self.mortality = min(abs(mortality), 100)
        self.duration = abs(duration)


class Person:
    """Models a person and their health status

    Attributes
    ----------
    is_infected : bool
        Persons infected status
    was_infected : bool
        Tracks if the person was infected. We assume you can't get infected twice.
    is_immune : bool
        If the persons gets infected and doesn't die they become immune.
    is_alive : bool
        Alive status. True by default.
    days_infected : int
        Days since person became infected. 0 by default.
    """

    def __init__(self):
        """Constructor
        Initializes persons health status
        """
        self.is_infected = False
        self.was_infected = False
        self.is_immune = False
        self.is_alive = True
        self.days_infected = 0

    def end_of_sickness(self, virus):
        """Person either gets well and becomes immune or they die"""
        if self.days_infected == virus.duration:
            self.is_infected = False
            chance = random.randint(1, 100)
            if chance <= virus.mortality:
                self.is_alive = False
            else:
                self.is_immune = True

    def virus_contact(self, virus):
        """Randomly infects a person based on infection rate"""
        if self.was_infected == False:
            chance = random.randint(1, 100)
            if chance <= virus.risk:
                self.is_infected = True
                self.was_infected = True


# Gets a person from a 2d list
def list_get(people_list, row, column):
    try:
        return people_list[row][column]
    except IndexError:
        return Person()  # returns a healthy person instead of an error at the edge of the grid


class Simulation:
    """Simulates passage of time and infections"""
    def __init__(self, simulation_duration):
        """
        Constructor
        
        Parameters
        ----------
        simulation_duration : int
            How many days is the program going to simulate
        """
        self.simulation_duration = simulation_duration

    def increase_day(self, virus, population):
        """
        Simulates another day of the infection for infected people.

        Parameters
        ----------
        virus : obj
            Model of our virus
        population : obj
            Population object that contains all the people
        """
        for row in population.people:
            for person in row:
                if person.is_infected and (person.days_infected < virus.duration):
                    person.days_infected += 1
                elif person.is_infected and (person.days_infected == virus.duration):
                    person.end_of_sickness(virus)

    def simulate_day_4_neighbors(self, virus, population):
        """
        Simulates another day for everyone.
        Calls the increase_day to hande the infected people.
        Checks the 4 neighbours (up, down, right, left) and tries to infect healthy people based on the virus attributes.

        Parameters
        ----------
        virus : obj
            Model of our virus
        population : obj
            Population object that contains all the people
        """
        self.increase_day(virus, population)
        for i in range(population.grid_size):
            for j in range(population.grid_size):
                person = population.people[i][j]
                neighbors = []
                neighbors.append(list_get(population.people, i-1, j).is_infected)
                neighbors.append(list_get(population.people, i+1, j).is_infected)
                neighbors.append(list_get(population.people, i, j-1).is_infected)
                neighbors.append(list_get(population.people, i, j+1).is_infected)
                if any(neighbors):
                    person.virus_contact(virus)

    def simulate_day_8_neighbors(self, virus, population):
        """
        Simulates another day for everyone.
        Calls the increase_day to hande the infected people.
        Checks the 8 neighbours (up, down, right, left, digonals) and tries to infect healthy people based on the virus attributes.

        Parameters
        ----------
        virus : obj
            Model of our virus
        population : obj
            Population object that contains all the people
        """
        self.increase_day(virus, population)
        for i in range(population.grid_size):
            for j in range(population.grid_size):
                person = population.people[i][j]
                neighbors = []
                neighbors.append(list_get(population.people, i-1, j).is_infected)
                neighbors.append(list_get(population.people, i+1, j).is_infected)
                neighbors.append(list_get(population.people, i, j-1).is_infected)
                neighbors.append(list_get(population.people, i, j+1).is_infected)
                neighbors.append(list_get(population.people, i-1, j-1).is_infected)
                neighbors.append(list_get(population.people, i+1, j-1).is_infected)
                neighbors.append(list_get(population.people, i-1, j+1).is_infected)
                neighbors.append(list_get(population.people, i+1, j+1).is_infected)

                if any(neighbors):
                    person.virus_contact(virus)

def graphics(population, canvas):
    """A helper function to update tkinter display"""
    square_dimension = 800//population.grid_size

    # Loop through all rows in the population and set where rectangles are drawn
    for i in range(population.grid_size):
        y = i * square_dimension
        for j in range(population.grid_size):
            person = population.people[i][j]
            x = j * square_dimension

            # check the state of the person and fill in square
            if person.is_alive == False:
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='red')
            elif person.is_infected:
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='yellow')
            elif person.is_immune:
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='blue')
            else:
                canvas.create_rectangle(x, y, x+square_dimension, y+square_dimension, fill='green')


def show_results(report):
    """Creates a new window and shows the report at the end of the simulation."""
    newWindow = tkinter.Toplevel(sim_window)
    newWindow.title("Report")
    newWindow.geometry("300x300")
    newWindow.attributes('-topmost',True)
    tkinter.Label(newWindow, text=report).pack()

print("Welcome to the infection spread simulator.")
print()
# population size needs to be a perfect square so that we can show it in square grid
number_of_neighbors = input("Use 4 neighbors or 8 neighbors to simulate contact with people: ")
population_size = int(input("How many people do you want to simulate (rounded to the nearest square): "))
grid_size = int(math.sqrt(population_size))
population_size = grid_size ** 2
print(f"Population size set at {population_size}")

infected_people = int(input("How many people are infected at the beginning: "))
population = Population(grid_size, infected_people)
population.create_people()
population.initial_infection()

risk = int(input("What is the chance of someone getting infected if they get into contact with infected person (% per day): "))
mortality = int(input("What is the mortality rate in %: "))
duration = int(input("What is the duration of the disease in days: "))
virus = Virus(risk, mortality, duration)

simulate_days = int(input("How many days do you want to simulate: "))
print("Legend:\nGreen = Alive and never infected\nYellow = Currently infected\nBlue = Immune\nRed = Dead\n")

# Creating tkinter window, canvas
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

sim_window = tkinter.Tk()
sim_window.attributes('-topmost',True)
sim_window.title("Epidemic simulator")
sim_canvas = tkinter.Canvas(sim_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="lightblue")
sim_canvas.pack(side=tkinter.LEFT)

simulation = Simulation(simulate_days)
graphics(population=population, canvas=sim_canvas)
sim_window.update()
sim_canvas.delete('all')

# Track the stats and if they dont change for 10 days consider the simulation over. The equilibrium is reached
stop = False
days_simulated = 0
combos = []

while days_simulated < simulation.simulation_duration and stop == False:
    time.sleep(0.02)
    if number_of_neighbors == 4:
        simulation.simulate_day_4_neighbors(virus, population)
    else:
        simulation.simulate_day_8_neighbors(virus, population)

    graphics(population=population, canvas=sim_canvas)
    combos.append(population.get_stats())

    # Update tkinter window to reflect graphics change
    sim_window.update()

    # If we are not at the end wipe the canvas so that it just doesnt keep on adding rectangles
    sim_canvas.delete('all')

    if combos.count(population.get_stats()) == 50:
        stop = True
    days_simulated += 1

# Show grid at the end and show the report
graphics(population=population, canvas=sim_canvas)
sim_window.update()

msg = f"Days simulated {days_simulated}\n\n" + population.get_report()
show_results(msg)
sim_window.mainloop()
