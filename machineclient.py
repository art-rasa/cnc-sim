# 
# Title: G-code interpreter program
# File: machineclient.py
# Description: Provides a class that simulates a simplified CNC machine.
# Author: Arttu Räsänen (arttu.rasanen@protonmail.com
# Date: 2022-02-01
# 

# Constant value definitions for parameters.
UNDEFINED = 0
PLANE_XY = 1
PLANE_ZX = 2
PLANE_YZ = 3
PLANE_UV = 4
PLANE_WU = 5
PLANE_VW = 6
SPINDLE_MODE_CW = 7
SPINDLE_MODE_CCW = 8
SPINDLE_MODE_HALT = 9
MOTION_MODE_RAPID = 10
MOTION_MODE_LINEAR = 11
UNIT_MM = 12
UNIT_INCH = 13
DIST_MODE_ABS = 14
DIST_MODE_INC = 15
FEED_MODE_INVTIME = 16
FEED_MODE_UPMIN = 17
FEED_MODE_UPREV = 18

# Descriptive texts for the parameters.
NAMES = [
"UNDEFINED",
"X/Y", "X/Z", "Y/Z", "U/V", "W/U", "V/W",
"CLOCKWISE", "COUNTER-CLOCKWISE", "HALT",
"RAPID", "LINEAR",
"MILLIMETRES", "INCHES",
"ABSOLUTE","INCREMENTAL",
"INVERSE TIME", "UNITS/MIN", "UNITS/REV"
]

class MachineClient:
    # Selected plane (XY, ZX, YZ, UV, WU, VW)
    _plane = UNDEFINED
    # Current position of the cutter.
    _pos = {"x": 0.0, "y": 0.0, "z": 0.0}
    # Selected tool name.
    _tool_name = ""
    # Spindle state.
    _spindle_params = {"is_active": False, "speed": 0, "mode": UNDEFINED}
    # Feed rate settings.
    _feed_rate_params = {"rate": 0, "mode": UNDEFINED}
    # Coolant state.
    _coolant_on = False
    # Unit of measure (mm, inch).
    _unit = UNDEFINED
    # Distance mode (absolute, incremental)
    _dist_mode = UNDEFINED
    # Motion mode (linear, rapid).
    _motion_mode = UNDEFINED
    
    
    def __init__(self):
        """ Displays a message on MachineClient construction. """
        self.statusprint("CNC machine initializing.")
        
        
    def __del__(self):
        """ Displays a message on MachineClient deletion. """
        self.statusprint("CNC machine shutting down.")
        
        
    def rapid_move(self, params):
        """ Switches the machine into rapid movement mode and optionally
        performs a rapid move.
        Args:
          params (dict): coordinates of the movement.
        """
        self._motion_mode = MOTION_MODE_RAPID
        
        if (params is None):
            self.statusprint("Setting motion mode to {}".format(NAMES[self._motion_mode]))
            return
        
        new_x = self._pos["x"]
        new_y = self._pos["y"]
        new_z = self._pos["z"]
        
        for par in params:
            if (par[0] == "X"):
                new_x = float(par[1 : len(par)])
            if (par[0] == "Y"):
                new_y = float(par[1 : len(par)])
            if (par[0] == "Z"):
                new_z = float(par[1 : len(par)])
        
        self.move(new_x, new_y, new_z)
        
        
    def lin_move(self, params):
        """ Switches the machine into linear movement mode and 
        optionally performs a linear move with the current feed rate.
        Args:
          params (dict): coordinates of the movement.
        """
        self._motion_mode = MOTION_MODE_LINEAR
        
        if (params is None):
            self.statusprint("Setting motion mode to {}".format(NAMES[self._motion_mode]))
            return
        
        new_x = self._pos["x"]
        new_y = self._pos["y"]
        new_z = self._pos["z"]
        
        for par in params:
            if (par[0] == "F"):
                self.set_feed_rate( float(par[1 : len(par)]) )
            if (par[0] == "X"):
                new_x = float(par[1 : len(par)])
            if (par[0] == "Y"):
                new_y = float(par[1 : len(par)])
            if (par[0] == "Z"):
                new_z = float(par[1 : len(par)])
        
        self.move(new_x, new_y, new_z)
        
    def set_plane_xy(self, dummy={}):
        """ Sets the plane to X/Y mode.
        Args:
          dummy (dict) unused
        """
        self._plane = PLANE_XY
        self.statusprint("Plane set to {}".format(NAMES[self._plane]))
    
    
    def set_plane_zx(self, dummy={}):
        """ Sets the plane to Z/X mode.
        Args:
          dummy (dict) unused
        """
        self._plane = PLANE_ZX
        self.statusprint("Plane set to {}".format(NAMES[self._plane]))
    
    
    def set_plane_yz(self, dummy={}):
        """ Sets the plane to Y/Z mode.
        Args:
          dummy (dict) unused
        """
        self._plane = PLANE_YZ
        self.statusprint("Plane set to {}".format(NAMES[self._plane]))
        
        
    def set_unit_mm(self, dummy={}):
        """ Sets the machine to use millimetres as its unit of measure.
        Args:
          dummy (dict) unused
        """
        self._unit = UNIT_MM
        self.statusprint("Unit of measure set to {}"
            .format(NAMES[self._unit]))
    
    
    def set_unit_inch(self, dummy={}):
        """ Sets the machine to use inches as its unit of measure.
        Args:
          dummy (dict) unused
        """
        self._unit = UNIT_INCH
        self.statusprint("Unit of measure set to {}"
            .format(NAMES[self._unit]))
    
    
    def set_cutter_comp_off(self, dummy={}):
        """ Sets the machine to disable cutter compensation.
        Args:
          dummy (dict) unused
        """
        self.statusprint("Cutter compensation turned OFF")
        #No implementation
        
        
    def cancel_tool_length_comp(self, dummy={}):
        """ Sets the machine to disable tool length compensation.
        Args:
          dummy (dict) unused
        """
        self.statusprint("Tool length compensation CANCELED")
        #No implementation
        
        
    def cancel_canned_cycle(self, dummy={}):
        """ Sets the machine to cancel canned cycle.
        Args:
          dummy (dict) unused
        """
        self.statusprint("Canned cycles CANCELED")
        #No implementation
        
        
    def set_feed_rate_mode_upmin(self, dummy={}):
        """ Sets the machine to use unit/minute feed rate mode.
        Args:
          dummy (dict) unused
        """
        self._feed_rate_params["mode"] = FEED_MODE_UPMIN
        self.statusprint("Feed rate mode set to {}"
            .format(NAMES[self._feed_rate_params["mode"]]))
        
        
    def set_feed_rate_mode_invtime(self, dummy={}):
        """ Sets the machine to use inverse time feed rate mode.
        Args:
          dummy (dict) unused
        """
        self._feed_rate_params["mode"] = FEED_MODE_INVTIME
        self.statusprint("Feed rate mode set to {}"
            .format(NAMES[self._feed_rate_params["mode"]]))
        
    
    def set_feed_rate_mode_uprev(self, dummy={}):
        """ Sets the machine to use unit/revolution feed rate mode.
        Args:
          dummy (dict) unused
        """
        self._feed_rate_params["mode"] = FEED_MODE_UPREV
        self.statusprint("Feed rate mode set to UNITS/REVOLUTION"
            .format(self._feed_rate_params["mode"]))
        
        
    def home(self, params):
        """ Moves machine to home position. 
        According to http://linuxcnc.org/docs/html/gcode/g-code.html#gcode:g28-g28.1
        
         G28 axes - makes a rapid move to the position specified by axes 
         including any offsets, then will make a rapid move to the 
         absolute position of the values in parameters 5161-5166 for all 
         axes specified. Any axis not specified will not move.  
        
        In this toy code it is assumed that parameters 5161-5166 are 
        programmed to contain the home position (x=0.0; y=0.0; z=0.0) 
        Only the specified axes will move into their home positions.
        """
        # Moving the specified axes (if any).
        if (self._motion_mode == DIST_MODE_INC):
            for par in params:
                amount = float( par[1 : len(par)] )
                if (par[0] == "X"):
                    self.move_x(self._pos["x"] + amount)
                if (par[0] == "Y"):
                    self.move_y(self._pos["y"] + amount)
                if (par[0] == "Z"):
                    self.move_z(self._pos["z"] + amount)
                    
        elif (self._motion_mode == DIST_MODE_ABS):
            for par in params:
                amount = float( par[1 : len(par)] )
                if (par[0] == "X"):
                    self.move_x(amount)
                if (par[0] == "Y"):
                    self.move_y(amount)
                if (par[0] == "Z"):
                    self.move_z(amount)
        
        # Homing.
        self.statusprint("Moving selected axes to home.")
        for par in params:
            if (par[0] == "Z"):
                self.move_z(0.0)
            if (par[0] == "X"):
                self.move_x(0.0)
            if (par[0] == "Y"):
                self.move_y(0.0)
    
    
    def move(self, x, y, z):
        """ Uses linear movement to move spindle to given XYZ coordinates.
        Args:
        x (float): X axis absolute value [mm]
        y (float): Y axis absolute value [mm]
        z (float): Z axis absolute value [mm]
        """
        if (self._dist_mode == DIST_MODE_INC):
            new_x = self._pos["x"] + x
            new_y = self._pos["y"] + y
            new_z = self._pos["z"] + z
            
        elif (self._dist_mode == DIST_MODE_ABS):
            new_x = x
            new_y = y
            new_z = z
            
        else:
            self.statusprint("move(): Error, distance mode not set.")
            return
        
        self.statusprint("Moving to X={:.3f} Y={:.3f} Z={:.3f} [{}]."
            .format(new_x, new_y, new_z, NAMES[self._unit]))
        
        if (self._motion_mode == MOTION_MODE_LINEAR):
            rate = self._feed_rate_params["rate"]
            mode = self._feed_rate_params["mode"]
            self.statusprint("Using feed rate F={:.3f} {}".format(rate, NAMES[mode]))
            
        if (new_z >= self._pos["z"]):
            # Mill bit must raise before changing position.
            if (abs(new_z - self._pos["z"]) >= 0.001):
                self.move_z(new_z)
            if (abs(new_x - self._pos["x"]) >= 0.001):
                self.move_x(new_x)
            if (abs(new_y - self._pos["y"]) >= 0.001):
                self.move_y(new_y)
            
        else:
            # Head must move into position before lowering the mill bit.
            if (abs(new_x - self._pos["x"]) >= 0.001):
                self.move_x(new_x)
            if (abs(new_y - self._pos["y"]) >= 0.001):
                self.move_y(new_y)
            if (abs(new_z - self._pos["z"]) >= 0.001):
                self.move_z(new_z)


    def move_x(self, value):
        """ Moves spindle to given X coordinate. Keeps current Y and Z
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """        
        self.statusprint("Moving X to {:.3f} [{}]."
            .format(value, NAMES[self._unit]))
        self._pos["x"] = value


    def move_y(self, value):
        """ Moves spindle to given Y coordinate. Keeps current X and Z
        unchanged.
        Args:
        value(float): Axis absolute value [mm]
        """
        self.statusprint("Moving Y to {:.3f} [{}]."
            .format(value, NAMES[self._unit]))
        self._pos["y"] = value
        
        
    def move_z(self, value):
        """ Moves spindle to given Z coordinate. Keeps current X and Y
        unchanged.
        Args:
        value (float): Axis absolute value [mm]
        """
        self.statusprint("Moving Z to {:.3f} [{}]."
            .format(value, NAMES[self._unit]))
        self._pos["z"] = value
    
    
    def set_feed_rate(self, value):
        """ Sets spindle feed rate.
        Args:
        value (float): Feed rate [mm/s]
        """
        if (self._feed_rate_params["mode"] == UNDEFINED):
            self.statusprint("set_feed_rate(): Error, unknown feed rate mode.")
            return
        
        # "Official" CNC feed rate is units/min
        elif (self._feed_rate_params["mode"] == FEED_MODE_UPMIN):
            self._feed_rate_params["rate"] = value * 60.0
        
        # TODO: other feed rate modes?
        else:
            self.statusprint("set_feed_rate(): Error, feed rate mode not implemented.")
            return
            
        
    def set_spindle_speed(self, value):
        """ Sets spindle rotational speed.
        Args:
        value (int): Spindle speed [rpm]
        """
        if (value < 0):
            self.statusprint("set_spindle_speed(): Error, speed must be non-negative.")
            return
        
        self._spindle_params["speed"] = value
        self.statusprint("Using spindle speed {} [rpm].".format(value))


    def set_spindle_mode_cw(self, dummy={}):
        """ Sets spinde mode to clockwise.
        Args:
          dummy (dict): unused
        """
        self._spindle_params["mode"] = SPINDLE_MODE_CW
        self._spindle_params["state"] = True
        
        self.statusprint("Setting spindle mode to {}"
            .format(NAMES[self._spindle_params["mode"]]))

    
    def set_spindle_mode_ccw(self, dummy={}):
        """ Sets spinde mode to counter-clockwise.
        Args:
          dummy (dict): unused
        """
        self._spindle_params["mode"] = SPINDLE_MODE_CCW
        self._spindle_params["state"] = True
        
        self.statusprint("Setting spindle mode to {}"
            .format(NAMES[self._spindle_params["mode"]]))

        
    def set_spindle_mode_halt(self, dummy={}):
        """ Sets spinde mode to halt.
        Args:
          dummy (dict): unused
        """
        self._spindle_params["mode"] = SPINDLE_MODE_HALT
        self._spindle_params["state"] = False
        
        self.statusprint("Setting spindle mode to {}"
            .format(NAMES[self._spindle_params["mode"]]))

        
    def set_dist_mode_abs(self, dummy={}):
        """ Sets distance mode to absolute.
        Args:
          dummy (dict): unused
        """
        self._dist_mode = DIST_MODE_ABS
        self.statusprint("Setting distance mode to {}"
            .format(NAMES[self._dist_mode]))
        
        
    def set_dist_mode_inc(self, dummy={}):
        """ Sets distance mode to incremental.
        Args:
          dummy (dict): unused
        """
        self._dist_mode = DIST_MODE_INC
        self.statusprint("Setting distance mode to {}"
            .format(NAMES[self._dist_mode]))
        
        
    def set_coord_system(self, num):
        """ Sets coordinate system. 
        Args:
          num (int) number of the coordinate system to use.
        """
        self.statusprint("Selecting coordinate system #{}".format(num))
        # not implemented.
        
        
    def change_tool(self, tool_name):
        """ Change tool with given name.
        Args:
        tool_name (str): Tool name.
        """
        self._tool_name = tool_name
        self.statusprint("Changing tool '{:s}'.".format(self._tool_name))
        

    def manual_tool_change(self, dummy={}):
        """ Prints a request for a manual tool change.
        Args:
          dummy (dict): unused
        """
        self.statusprint("Manual tool change to '{}' requested".format(self._tool_name))
        
        
    def coolant_on(self, dummy={}):
        """ Turns spindle coolant on. 
        Args:
          dummy (dict): unused
        """
        self.statusprint("Coolant turned on.")
        _coolant_on = True
    
    
    def coolant_off(self, dummy={}):
        """ Turns spindle coolant off. 
        Args:
          dummy (dict): unused
        """
        self.statusprint("Coolant turned off.")
        _coolant_on = False


    def program_end(self, dummy={}):
        """ Ends the program. 
        According to http://linuxcnc.org/docs/html/gcode/m-code.html#mcode:m2-m30
        this command has the following effects:
            1. Change from Auto mode to MDI mode.
            2. Origin offsets are set to the default (like G54).
            3. Selected plane is set to XY plane (like G17).
            4. Distance mode is set to absolute mode (like G90).
            5. Feed rate mode is set to units per minute (like G94).
            6. Feed and speed overrides are set to ON (like M48).
            7. Cutter compensation is turned off (like G40).
            8. The spindle is stopped (like M5).
            9. The current motion mode is set to feed (like G1).
           10. Coolant is turned off (like M9).
        Args:
          dummy (dict): unused
        """
        self.statusprint("Program end reached.")
        # not implemented...            # 1
        self.set_coord_system(1)        # 2
        self.set_plane_xy()             # 3
        self.set_dist_mode_abs()        # 4
        self.set_feed_rate_mode_upmin() # 5
        # not implemented...            # 6
        # not implemented...            # 7
        self.set_spindle_mode_halt()    # 8
        self.lin_move(None)             # 9
        self.coolant_off()              # 10
        
    
    def statusprint(self, message):
        """ Prints machine status messages to standard output.
        Args:
          message (str): message to print.
        """
        print(4*"-" + "> ", end="")
        print(message)















