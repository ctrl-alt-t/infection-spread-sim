# Infection spreading simulation

This simulates an infection spreading in a population. Population is modeled as a grid.

Green cells are alive people who have never been infected, yellow cells are currently infected people, blue are immune people (assumption is that if a person doesn't die they get permanent immunity), red cells are dead people.

## How to run

Run `simulate_spread.py`.
Parameters for the simulation are entered in the terminal after which simulation starts and is shown in a new window.
When choosing how the infection spreads you can choose to look at 4 nearest neighbors (up, down, left, right) or 8 nearest neighbors (same as 4 + diagonals).

After the number of days to be simulated is added the simulation will start.
The simulation ends if the days simulated have reached the days given by the user or if nothing changed in the last 50 days.

## Parameters

![Parameters](/screenshots/infection_spread_input.png)

## Report

After the simulation has ended you are shown a report.

![Report](/screenshots/simulation_report.png)

## Simulation running

My potato pc can simulate 10000 people just fine.
![10000](/screenshots/10000_sim.gif)
