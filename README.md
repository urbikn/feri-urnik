Urnik
============

> **OS Specific:** Linux  
> **Distributions:** Debian/Ubuntu  
> **Python Version:** 3.x  

A commandline utility to display FERIs scheduler offline.  
**Urnik** was my answer to FERIs WiseTimetable scheduling web application at the end of 2017.

## How it works ##

Urnik gets its information by downloading an .ics file from the scheduling [website](https://wise-tt.com/wtt_um_feri/). Then it parses the .ics file and writes it into a file named _urnik.txt_ in a table structure (look at the picture).  It also writes a second table that uses filters based on the users configuration ( which classes he/she is/isn't attending). In the end there are two tables, one for the entire class and one for the specific users settings.

The program uses the CLI to display its data via less.

![image of urnik in CLI](img/urnik.png "urnik showing general schedule for entire week")

## Requirements ##

Urnik requires three things to run:

 - [**Pip3**](https://pip.pypa.io/en/stable/quickstart/) - Python's package manager system,
 - [**Firefox**]() - A web browser (used with Selenium),
 - [**Python's Selenium**](https://selenium-python.readthedocs.io/) - An API with a suite of tools for automating web browser ( **auto installed** )
  - [**geckodriver**](https://github.com/mozilla/geckodriver) - Proxy for using W3C WebDriver compatible clients to interact with Gecko-based browsers ( **auto installed** )

## Installation ##

Download the zip or clone the project and change directory to unziped or cloned folder.
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

If you want to use the program with your information and not the default, then you need to change the the data in config/user_data.json by replacing:
- program ('program'),
- year ('leto'),
- course ('smer')

With the text from the main schedule website [WiseTimetable](https://wise-tt.com/wtt_um_feri/). **COPY THE ENTIRE TEXT AS IS, NOT JUST PART OF IT**
 

## Reporting bugs ##
If the application goes south on you, please use GitHubs issue trackers and I'll see what we can do:  
https://github.com/urbikn/feri-urnik/issues

or contact me via email at: urban@knuples.net
