# top

[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![Commits: Conventional](https://img.shields.io/badge/Commits-Conventional-blue.svg)](https://www.conventionalcommits.org/en/v1.0.0/)

A Cross-Platform Python implementation of 'top' command using Psutil.

## What top Does

Top is able to get most of the top information with the restrictions that come with running it at the program level. Different statistics are shown based on the operating system that this project is run on. top work on MacOS, Linux, and Windows operating systems.

## How to Get Started With top

You can get started with top by cloning the repository and running the command ``` python src/top.py ``` in the base directory. Like the top command, this will run forever. You can exit out of the program by entering a keyboard interrupt or exiting your terminal altogether. You can also specify the amount of times you want the program to run by giving a second integer input. For example, you can run the program for one iteration by writing the command ```python src/top.py 1```.

## Running Gatorgrade Checks

This repository is able to be automatically assesed using GatorGrade. These checks can be run from the repository's base directory by running the command ```gatorgrade --config config/gatorgrade.yml``` in the base directory if you have gatorgrade installed.

These checks ensure that files are formatted correctly with proficient levels of polish and also run without crashing. They are very useful both during and after development.
