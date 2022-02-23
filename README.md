# G-code interpreter

Simple interpreter program for G-code. It reads a text file given as a 
command-line argument containing G-code commands. The commands are then 
executed with a simulated CNC machine. 

Each line of the G-code file is executed as a "block". Each block may 
contain one or more G-code commands. In addition, some commands may have
one or more parameters. Parameters instruct the machine how it should 
run that particular command. The actions taken by the simulated CNC 
machine are printed into standard output.

Command descriptions taken from: 
[LinuxCNC.org](http://linuxcnc.org/docs/html/index.html)

## Requirements

- [Python 3.x](https://www.python.org/downloads/) runtime environment

## Running the program

```shell
$ python ./main.py <file.gcode>
```

