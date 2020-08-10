# Sobot Rimulator

A robot programming tool inspired by [Sim.I.Am](http://jpdelacroix.com/software/simiam.html) by [JP de la Croix](http://jpdelacroix.com/)

![Screenshot](documentation/screenshot.png)

## Documentation

Detailed documentation can be found in the [Manual](documentation/Manual.txt).

I also wrote about this project for the Toptal Engineering Blog! Read more about the underlying principles of autonomous mobile robotics [here](https://www.toptal.com/robotics/programming-a-robot-an-introductory-tutorial).


## Requirements

Sobot Rimulator requires Python 3. Its main dependencies are Gtk 3 and PyGObject, which are used for the UI.

If you are using Conda, you can install these from Conda Forge:

```
conda create -n sobot-rimulator -c conda-forge python=3 gtk3 pygobject
conda activate sobot-rimulator
```

## To Run

From the command line, navigate to the project's root directory. Then type:

```
python simulator.py
```
