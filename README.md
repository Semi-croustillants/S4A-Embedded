# S4A embedded

Want to develop Arduino programs within scratch but also want to unplug it and plug it to any kind of power supply?

Works with scratch v2 and SuperEasy-A4S blocks (**[see A4S documentation](http://thomaspreece.com/resources.php)**). For tone, noTone and servo blocks
use ImportBlock.sb2 in github repository.

Windows stand alone executable compiled with py2exe.

**Known Issues**:
* **Problem parsing variables** : depending on which "_thread_" you created first and set your variables with, you might encounter some bugs during the translation into .ino file.
* **Unix System** : you have to "hack" the path settings when you want to launch our system within a unix based OS. Some fixes to come

**Needed**:

* **For running** : python, scratch v2 with custom blocks, arduino ide with artk lib
* **For compiling with py2exe** : wxPython (32 bit), py2exe

**Supported python versions**: python 2.7

**Tested on** : arduino UNO

# Featured

* GUI
* Translation : ".sb2" to customized ".ino"
* Embedded kernel based on ARTK (thanks to **[P. H. Schimpf](https://sites.google.com/site/pschimpf99/home/artk)**)
* Custom A4S arduino blocks
* Non slave/master system (sorry A4S and S4A, we rulez)
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

**COMING SOON : WINDOWS and UNIX usage
* Import ARTK source code in librairies folder (Usually in Documents/Arduino)
* Craft your own code in scratch v2 and circuit on your arduino
* Export it as a .sb2 file
* Open the GUI in the **ScratchInoConvertor/dist** directory and import your .sb2 file
* Start translation, it will open the Arduino IDE with your translated code
* Upload it as it was a classic .ino program

### Modifying
* Feel free to enhance our work
* All sources are available in the **ScratchInoConvertor/src** directory

### Tests
Tests data are available in exemple.sb2 and ImportBlocks.sb2 files

### What\'s Next?
* Working on a tutorial. Coming soon, the tutorial we presented during the Scratch AMS 2015 conv
* Working on a way to compil and upload programs without oppening arduino's IDE.
* Working on a way to use our system as an extension to add in scratch v2.

### Configuration file
When you start the GUI for the first time, two dialogs appears.
The first ask you to select the Arduino sketch folder and the
second ask you to select the Arduino IDE executable.
This informations are save in the root folder of the GUI in a file named
".config".
The structure of the configuration file is :
- Lines beginning with "#" are comments
- Other lines are in the form KEY=value
If you need to reinit configuration file, click on parameter menu and select
"Reinit config file". This action will remove the obsolete .config file
and ask you to select new informations

### Context
This tool has been developped by some french students in computer engineering school for a final project.

