# top

[![build](../../actions/workflows/build.yml/badge.svg)](../../actions/)
[![Language: Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
[![Commits: Conventional](https://img.shields.io/badge/Commits-Conventional-blue.svg)](https://www.conventionalcommits.org/en/v1.0.0/)

A Cross-Platform Python implementation of 'top' command using Psutil.

## What top Does

Top is able to get most of the top information with the
restrictions that come with running it at the program level.
Different statistics are shown based on
the operating system that this project is run on.
top works on MacOS, Linux, and Windows operating systems.

## How to Get Started With top

### PIPY Installation

You can install top through running this command in your terminal:

``` pipx install ostop ```

Once this command finishes running, you can then run commands in
these two different formats:

``` ostop ```

The command with no extra parameters will make the program run
in an infinite loop forever until you close your terminal or
use a Keyboard Interrupt.

``` ostop <integer value> ```

The command with an integer value will make the program run
for the number of iterations/seconds you specify.


### Local Installation

You can get started with top by cloning the repository and running this command:

``` python src/top.py ```

in the base directory. Like the top command, this will run forever.
You can exit out of the program by entering a keyboardinterrupt or exiting
your terminal altogether.You can also specify the amount of times you want
the program to run by giving a second integer input. For example, you can
run the program for one iteration by writing this command:

``` python src/top.py 1 ```

## Running GatorGrade Checks

This repository is able to be automatically assessed using GatorGrade.
These checks can be run from the repository's base directory by running this command:

```gatorgrade --config config/gatorgrade.yml```

in the base directory if you have GatorGrade installed.
If you do not have GatorGrade installed yet on your local machine, you can install
it by using this command:

```pip install gatorgrade```

These checks ensure that files are formatted correctly with proficient levels of
polish and also run without crashing. GatorGrade checks are useful both
during and after development.
