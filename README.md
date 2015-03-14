# S4A embedded
Allows embedding for scratch v2 programms on arduinos boards.

Works with scratch v2 and SuperEasy-A4S blocks (**[see A4S intallation & documentation](http://thomaspreece.com/resources.php)**)

** Needed **: python, wxPython (32 bit), py2exe

** Supported python versions **: python 2.7

** Tested on ** : arduino UNO
 
# Features

* GUI
* Translation : ".sb2" to customized ".ino"
* Customized embedded kernel based on ARTK (thanks to **[P. H. Schimpf](https://sites.google.com/site/pschimpf99/home/artk)**)
* Non slave/master system (sorry A4S, we rulez)
* From 1 to 5 threads

# Getting Started

###Installation
* Install Arduino IDE
* Install Python 2.7
* TODO GUI installation guide
* TODO kernel's installation guide

###Usage
* Just launch ScratchInoConv.exe
* TODO images based doc

###Modifying
* Feel free to enhance our work
* All sources are available in the ** src ** directory

###Tests
Tests data are available in exemple.sb2 and ImportBlocks.sb2 files

#Translatable scratch v2 blocks
* Arduino's blocks
    * digitalWrite
    * digitalRead
    * analogRead
    * analogWrite
* Classics blocks
    * doIf
    * doIfElse
    * readVariable
    * setVar:to
    * changeVar:by
    * ops : *,+,-,/
    * doRepeat
    * doUntil
    * wait:elapsed:from
    * doWaitUntil
    * boolean ops : &,=,|,<,>,not,low,high

###Context
This tool has been developped by some french students in computer engineering school for a final project.