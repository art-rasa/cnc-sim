#!/usr/bin/python3

# 
# Title: G-code interpreter program
# File: main.py
# Description: Main program
# Author: Arttu Räsänen (arttu.rasanen@protonmail.com
# Date: 2022-02-01
# 

import sys 
import pdb
from machineclient import MachineClient as MC

def main(args):
    pgm_data = dict()
    
    if (len(args) != 2):
        show_usage()
        return 1
    
    print("args:", args)
    
    try:
        with open(args[1]) as f:
            parse_file(f, pgm_data)
            
    except OSError as err:
        print("Error: {}.".format(err))
        return 1
    
    run_program(pgm_data)
    
    return 0


def run_program(pgm_data):
    """ Simulates a run of a simple CNC machine with a given program.
    Args:
      pgm_data (dict): Dictionary containing the G-code commands.
    Returns:
      (none)
    """
    machine = MC()
    print("Now running the G-code program #{} (total {} commands)."
        .format(pgm_data["pgm_num"], pgm_data["num_commands"]))
    print("")
    i_block = 1
    for block in pgm_data["commands"]:
        print("Executing code block #{} ({} command"
            .format(i_block, len(block)), end="")
        
        if (len(block) == 1):
            print("):")
        else:
            print("s):")
            
        print("-" * 50)
        
        for command in block:
            print(command)
            #machine.execute_command(command)
            execute_command(machine, command)
        
        print("-" * 50)
        print("")
        i_block = i_block + 1


def execute_command(machine, cmd_data):
    """ Executes a G-code command with the CNC machine.
    Args:
      machine (object): instance of the MachineClient class.
      cmd_data (dict): command and (optionally) its parameters with
        the following structure.
              cmd_data: {
                  "cmd": "<command>",
                  "params": ["par1", ..., "parN-1", "parN"]
              }
    Returns:
      (nothing)
    """
    G_COMMANDS = {
        "G00": machine.rapid_move,
        "G01": machine.lin_move,
        "G17": machine.set_plane_xy,
        "G18": machine.set_plane_zx,
        "G19": machine.set_plane_yz,
        "G20": machine.set_unit_inch,
        "G21": machine.set_unit_mm,
        "G28": machine.home,
        "G40": machine.set_cutter_comp_off,
        "G49": machine.cancel_tool_length_comp,
        "G54": machine.set_coord_system,
        "G55": machine.set_coord_system,
        "G56": machine.set_coord_system,
        "G57": machine.set_coord_system,
        "G58": machine.set_coord_system,
        "G59": machine.set_coord_system,
        "G80": machine.cancel_canned_cycle,
        "G90": machine.set_dist_mode_abs,
        "G91": machine.set_dist_mode_inc,
        "G93": machine.set_feed_rate_mode_invtime,
        "G94": machine.set_feed_rate_mode_upmin,
        "G95": machine.set_feed_rate_mode_uprev,
    }
    M_COMMANDS = {
        "M03": machine.set_spindle_mode_cw,
        "M04": machine.set_spindle_mode_ccw,
        "M05": machine.set_spindle_mode_halt,
        "M06": machine.manual_tool_change,
        "M07": machine.coolant_on,
        "M08": machine.coolant_on,
        "M09": machine.coolant_off,
        "M30": machine.program_end,
    }
    T_COMMAND = machine.change_tool
    S_COMMAND = machine.set_spindle_speed
    
    cmd = cmd_data["cmd"]
    par = cmd_data.get("params")
    cmd_num = cmd[1 : len(cmd)]
        
    if (cmd in G_COMMANDS):
        if ((int(cmd_num) >= 54) and (int(cmd_num) <= 59)):
            par = int(cmd_num) - 53
            
        G_COMMANDS[cmd](par)
        return
    
    if (cmd in M_COMMANDS):
        M_COMMANDS[cmd](par)
        return
    
    if (cmd[0] == "T"):
        tool_name = "TOOL #" + cmd_num
        T_COMMAND(tool_name)
        return
        
    if (cmd[0] == "S"):
        spindle_speed = int( cmd_num )
        S_COMMAND(spindle_speed)
        return
        

def parse_file(f_obj, pgm_data):
    """ Reads a text file containing rows of G-code commands.
    Args:
      f_obj (file object): text file object returned from open().
      cmds (dict): G-code commands and their parameters are placed here.
    Returns:
      (none)
    """
    line_num = 0
    #pdb.set_trace()
    # Checking if valid data markers exist.
    if (not check_markers(f_obj)):
        return
    
    pgm_data["commands"] = list()
    pgm_data["num_commands"] = 0
    
    for txt_row in f_obj:
        txt_row = txt_row.strip()
        
        # Comment lines are skipped.
        if (is_comment(txt_row)):
            continue
        
        # Storing the program number.
        pgm_num = get_program_number(txt_row)
        if (pgm_num > 0):
            if (pgm_data.get("pgm_num") is not None):
                print("Error: multiple program numbers found.")
                return
                
            pgm_data["pgm_num"] = pgm_num
            continue
        
        # Getting all commands.
        get_commands(txt_row, pgm_data)
        
        

def get_commands(txt_row, pgm_data):
    """Gets all commands from the text row and stores them into a 
    dictionary given as a parameter.
    Args:
      txt_row (string): text line to scan for G-code commands.
      pgm_data (dict): commands (and their parameters) are stored here.
    """
    command_codes = ["G", "T", "S", "M"]
    parameter_codes = ["X", "Y", "Z", "F"]
    parts = txt_row.upper().split()
    i = 0
    gcode_seen = False
    codes = list()
    num_commands = 0
    
    while (i < len(parts)):
        # Line number, unused.
        if (parts[i][0] == "N"):
            i = i + 1
            continue
        
        # Adding parameters to the last command.
        if (gcode_seen):
            if (parts[i][0] in parameter_codes):
                if (codes[len(codes) - 1].get("params") is None):
                    codes[len(codes) - 1]["params"] = list()
                    
                codes[len(codes) - 1]["params"].append(parts[i])
                i = i + 1
                continue
            else:
                gcode_seen = False
        
        # Command
        if (parts[i][0] in command_codes):
            if (parts[i][0] == "G"):
                gcode_seen = True
            
            code = dict()
            code["cmd"] = parts[i]
            #code["params"] = list()
            codes.append(code)
            num_commands = num_commands + 1
            
        i = i + 1
    
    if (len(codes) > 0):
        pgm_data["commands"].append(codes)
        pgm_data["num_commands"] = pgm_data["num_commands"] + num_commands


def check_markers(f_obj):
    """ Scans the G-code for program data begin/end markers. 
    Valid G-code program file should have two such markers. 
    Args:
      f_obj(file object): G-code text file to check.
    Returns:
      True if valid number of data markers were found, False otherwise.
    """
    markers_seen = 0
    
    # Counting all data markers. Valid G-code should have two.
    for txt_row in f_obj:
        txt_row = txt_row.strip()
        
        if (is_marker(txt_row)):
            markers_seen += 1
    
    if (markers_seen != 2):
        print("Error: invalid number of data markers ({}, should have 2)"
              .format(markers_seen))
        #return False
    
    f_obj.seek(0)
    return (markers_seen == 2)

def is_marker(txt_row):
    """ Determines if the text line contains a program data marker, 
    which is just a single "%" character.
    Args:
      txt_row (string): text line to check.
    Returns:
      True if this text row is a program data marker, False if not.
    """
    if (len(txt_row) < 1):
        return False
    
    if (txt_row[0] == "%"):
        return True
    
    return False
        

def is_comment(txt_row):
    """ Tries to determine if the current line of text is a comment line.
    Args:
      txt_row (string): text line to check.
    Returns:
      True when the text line is considered a comment line, False if not.
    """
    if (len(txt_row) < 1):
        return True
        
    if ((txt_row[0] == '(') and (txt_row[len(txt_row) - 1] == ')')):
        return True
    else:
        return False
    

def get_program_number(txt_row):
    """ Checks if the current line of text contains a program 
    definition.
    Args:
      txt_row (string): text line to check.
    Returns:
      An integer number. If program number cannot be found, or is 
      invalid in some way, a large negative number is returned.
    """
    num = -9999
    len_txt = len(txt_row)
    
    if (len_txt < 2):
        return num
    
    if (txt_row[0] == "O"):
        numeric_part = txt_row[1:len_txt]
        try:
            conv_num = int(numeric_part)
            num = conv_num
        except ValueError:
            pass
    
    return num

def show_usage():
    print('Error: G-code file missing.')
    print('Usage: ./main.py <filename>')


if (__name__ == '__main__'):
    sys.exit(main(sys.argv))
