Urnik
============

> **OS Specific:** Linux  
> **Python Version:** 3.x  

**Urnik** was my answer to FERIs shitty WiseTimetable scheduling web application at the end of 2017.

Urnik gets its information by downloading an .ics file from the site and then starts extracting and writing readable text into a file named _urnik.txt_ in a table structure. It also writes a second table that uses filters based on the user's configuration ( which classes he is/isn't attending). In the end there are two tables, one for the entire class and one for the specific user.

## Requirements ##

Urnik requires three things to run:

 - [**Pip3**](https://pip.pypa.io/en/stable/quickstart/) - Python's package manager system,
 - [**Firefox**]() - A web browser (used with Selenium),
 - [**Python's Selenium**](https://selenium-python.readthedocs.io/) - An API with a suite of tools for automating web browser ( will be downloaded during the installation process if it doesn't exist )
 

## Installation ##

To install this program first check, if you have all the needed requirements, then download or clone this repository - to clone type into the command line
``` bash
git clone https://github.com/urbikn/feri-urnik
```

In the folder there is a shell script called **setup**. This script will set up all the needed things to make the program work and you can start it like:
``` bash
bash setup
```
or
``` bash
./setup
```
After the script finishes you can use the application via the command **urnik**. To see the command function type in the terminal
``` bash
urnik -h
```

## Usage ##

If you want to use the program with your information

## Reporting bugs ##
If the application goes south on you, please use GitHubs issue trackers and I'll see what we can do:  
https://github.com/urbikn/feri-urnik/issues

or contact me via email at: urban@knuples.net

