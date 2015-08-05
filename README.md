# S4A embedded
Allows embedding for scratch v2 programms on arduinos boards.

Works with scratch v2 and SuperEasy-A4S blocks (**[see A4S documentation](http://thomaspreece.com/resources.php)**). For tone and noTone
use ImportBlock.sb2 in github repository.

Compiled with py2exe

**Needed**:

* **For running** : python, scratch v2 with custom blocks, arduino ide with artk lib
* **For compiling with py2exe** : wxPython (32 bit), py2exe

**Supported python versions**: python 2.7

**Tested on** : arduino UNO

# Featured

* GUI
* Translation : ".sb2" to customized ".ino"
* Embedded kernel based on ARTK (thanks to **[P. H. Schimpf](https://sites.google.com/site/pschimpf99/home/artk)**)
* A4S arduino blocks
* Non slave/master system (sorry A4S, we rulez)
* From 1 up to 5 threads

# Getting Started

### Installation

**Required**:

  * Python 2.7
  * Arduino IDE
  * Scratch v2

**Preparing Arduino IDE** :

* Create a directory called ARTK under your Arduino library directory
* Copy the directory called **artk** form the directory **utils** into it

**Preparing Scratch V2** :

* Open scratch v2 and use the import blocks tool to import **ImportBlocks.sb2** form the **utils** directory


### Usage
* Craft your own code in scratch v2 and circuit on your arduino
* Export it as a .sb2 file
* Open the GUI in the **ScratchInoConvertor/dist** directory and import your .sb2 file
* Start translation, it will open the Arduino IDE with your translated code (windows only)
* Upload it as it was a classic .ino program

### Modifying
* Feel free to enhance our work
* All sources are available in the **ScratchInoConvertor/src** directory

### Tests
Tests data are available in exemple.sb2 and ImportBlocks.sb2 files

# Translatable scratch v2 blocks
* Arduino's blocks
    * digitalWrite
    * digitalRead
    * analogRead
    * analogWrite
    * tone
    * noTone
    * servoWrite
* Classics blocks
    * doIf
    * doIfElse
    * readVariable
    * setVar:to
    * changeVar:by
    * ops : *,+,-,/,%
    * doRepeat
    * doUntil
    * wait:elapsed:from
    * doWaitUntil
    * boolean ops : &,=,|,<,>,not,low,high

### Context
This tool has been developped by some french students in computer engineering school for a final project.
