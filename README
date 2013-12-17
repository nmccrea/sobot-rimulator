Thank you for using Robot Simulator! It is my sincere hope that this program will help you practice some of the basics of mobile robot control theory. The following is a brief manual for how to run and make use of the simulator.

This software and all accompanying materials are Copyright 2013 Nicholas Sloan Dowson McCrea. It is being released under the GNU General Public License, Version 3. Please see the accompanying LICENSE file for more information.



ACKNOWLEDGEMENTS:
=================

I would like to thank the following folks for inspiring the creation of Robot Simulator:

Dr. Magnus Egerstedt of The Georgia Institute of Technology, who's Coursera course "Control of Mobile Robots" was my first formal introduction to robotic control theory and was the inspiration for this software.

Jean-Pierre de la Croix of The Georgia Institute of Technology, who's robot simulator Sim.I.Am served as a design template for Robot Simulator.

All the visionary people at Coursera, who have provided an invaluable education service for those of us who previously have been without a practical option for continuing learning.



REQUIREMENTS:
=============

Robot Simulator is cross-platform compatible and should be able to run on Windows, Mac OSX, and Linux/Unix machines. In order to run, the following two items must be installed on your computer:
- Python 2.6.1 or higher
- PyGTK 2.7 or higher

To install Python: The latest Python interpreter can be found at http://www.python.org/download/.

To install PyGTK: The latest PyGTK distributions can found at http://www.pygtk.org/downloads.html.

Alternatively, both pieces of software should be available through package managers such as Apt-Get (for Linux/Unix) or Homebrew (for Mac - RECOMMENDED)



RUNNING THE SIMULATOR:
======================

To run the simulator, open a command prompt (terminal) and navigate to the folder where you downloaded the simulator. Then type:

$ python simulator.py



VIEW:
=====

The simulator window contains the following elements:
- Simulation Viewport
- Alert Text Panel
- Control Panel


Simulation Viewport:
--------------------

When the program starts, a randomized map is loaded.

A small blue and black circular object in the center of the viewport is the robot. The shape and capabilities of this robot are modeled after the Khepera III research robot. (See http://www.k-team.com/mobile-robotics-products/khepera-iii). The Khepera III is a differential-drive mobile robot. It is equipped with 9 infrared proximity sensors forming a "skirt", with which it can detect nearby obstacles.

A green circle indicates the location of the goal the robot will attempt to reach.

Red rectangles scattered throughout the map are obstacles - if the robot makes contact with an obstacle, a collision will occur and the simulation will end.

A grid is drawn onto the map to help you judge distances. Major gridlines are laid out every meter. Minor gridlines are laid out every 20 centimeters.


Alert Text Panel:
-----------------

When events such as a collision or successful arrival at the goal occur, it will be reported in the space between the simulation view port and the control panel. When the simulation beings, the alert text panel is blank.


Control Panel:
--------------

The control panel is divided into three rows.

The first row of buttons controls the simulation progress:

--  Pressing the "Play" button will cause the simulation to proceed until you stop it, or the robot reaches the goal or collides with an obstacle.

-- Pressing the "Stop" button will stop the simulation in its current state until you press Play.

-- Pressing the "Step" button will advance the simulation by one simulation cycle. The simulation will be stopped after this button is pressed.

-- Pressing the "Reset" button will clear all progress of the robot and reset the simulation.


The second row of buttons gives gives you control over the map:

-- Pressing the "Save Map" button will cause a save dialog to appear. The location to save maps is in the /maps folder of the simulator directory. Saving a map will NOT save the current state of the simulation. It only saves the location of the obstacles and the goal.

-- Pressing the "Load Map" button will cause a load dialog to appear. From here you can load previously saved maps. The simulation resets when a new map is loaded, so the robot will return to the center of the map.

-- Pressing the "Random Map" button will cause a randomized map to be generated on the fly. The simulation resets when a new random map is generated, so the robot will return to the center of the map.


The final row provides a more detailed visualization of what the robot is doing:

-- Pressing the "Show Invisibles" button causes extra information to be drawn to the simulation view that would not be visible in the real world. This includes the robots traverse path (where it has been so far), the robot's infrared sensors, the robot's current desired heading, and other information specific to the current control mode the robot is in:

    -  A green heading bar indicates that the robot is currently in Go to Goal mode.

    -  A red heading bar indicates that the robot is currently in Avoid Obstacles mode. This will be accompanied by a black envelope indicated the robot's detected surroundings.
    
    -  A blue heading bar indicates that the robot is currently in blended Go to Goal and Avoid Obstacles mode. This will be accompanied by two lesser heading bars each corresponding to the pure heading of Go to Goal mode and Avoid Obstacles mode, as well as the black envelope displayed by the Avoid Obstacles mode.
    
    -  An orange heading bar indicates that the robot is currently in Follow Wall mode. This will be accompanied by two black lines - one indicating the obstacle surface calculation that the robot is bearing on, and another indicating the stand-off distance to the obstacle.
  
  
PROGRAMMING THE ROBOT:
======================
- supervisor.py
- controllers
  - go_to_goal_controller.py
  - avoid_obstacles_controller.py
  - gtg_and_ao_controller.py
  - follow_wall_controller.py