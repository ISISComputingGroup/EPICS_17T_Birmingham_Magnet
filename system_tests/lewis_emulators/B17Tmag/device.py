from lewis.devices import StateMachineDevice
from lewis.core import approaches
from .states import DefaultState
from collections import OrderedDict


class SimulatedB17Tmag(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.re_initialise()
        # When the device is in an error state it can respond with junk
        self.is_giving_errors = False
        self.out_error = "}{<7f>w"
        self.out_terminator_in_error = ""
  


        # self.output = "1.000000T,10.000000A"
        # self.heater = 0
        # self.persist = "10fT,20A"
        # self.persistmode = "OFF" 
        # self.ready = "OFF" 
        # self.sensA = 0.00
        # self.sensB = 0.00
        # self.setpoint1 = 0.00
        # self.setpoint2 = 0.00
        # self.nv_pos = 0.00
        # self.pressure = 0.00
        # self.attoangle = 0.00
        # self.helevel = 0.00
        self.macrostatus = self.device_status()

        
    def device_status(self):
        """
        Returns the status of the device. 
        This inludes all device state parameters
        """


        device_status_string = f"output {self.target}; voltage {self.voltage}; heater {self.heater}; ramprate {self.ramprate}; units {self.units}; target {self.target}; persistent {self.persistent}; psustatus {self.psustatus}; pausestatus {self.pausestatus}; tblstatus {self.tblstatus}; ready {self.ready}; sensA {self.sensA}; sensB {self.sensB}; setpoint1 {self.setpoint1}; setpoint2 {self.setpoint2}; L1pid {self.L1pid}; L2pid {self.L2pid}; L1power {self.L1power}; L1range {self.L1range}; L2power {self.L2power}; L2range {self.L2range}; L1mout {self.L1mout}; L2mout {self.L2mout}; L1ctrl {self.L1ctrl}; L2ctrl {self.L2ctrl}; zone {self.zone}; tcstatus {self.tcstatus}; nv {self.nv}; pressure {self.pressure}; valvestatus{self.valvestatus}; helevel{self.helevel}; nlevel{self.nlevel}; hefrequency{self.hefrequency}; persistmode{self.persistmode};  attoangle{self.attoangle};"

        return device_status_string

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    
    def re_initialise(self):
        """
        Setting values device is initially set with when it is first turned on
        Values are set based on those set in the manual for Birmingham 17T magnet.
        """

        self.field_T = 1.000000 # Output of the power supply in Tesla (T) and Amps (A)
        self.curr_A = 10.000000
        self.voltage = 1.253000 # Voltage measured across the terminals of the main power supply
        self.heater = 0 # Main coil heater status
        self.ramprate = 1.234000 # Current ramp rate
        self.units = 0 # Current ramp rate units
        self.target = "1.000000T,10.000000A" # Current target
        self.persistent = "0.000000T,0.000000A" # Current persistent field value in Tesla (T) and Amps (A)
        self.psustatus = "Unable to communicate with PSU. Please check interface and mains cables. Initialisation failed."
        self.pausestatus = "OFF" #Power supply pause status
        self.tblstatus = "1.000000T,10.000000A" # Ignore table status. If ON, ramp rates set by the user with the ‘ramp rate’ command are limited by the table stored in the configuration file; if OFF, ramp rates follow the table and the ‘set rate’ command is ignored.
        self.ready = "ON" # Indicates if the power supply software is busy completing its current task
        self.sensA = 0.000 # Current Temp Heat Exchanger
        self.sensB = 0.000 # Current Temp Probe
        self.setpoint1 = 0.000 # Current Setpoint Heat Exchanger
        self.setpoint2 = 0.000 # Current Setpoint Probe
        self.L1pid = "50.0,20.0,0.0" # Heat Exchanger P,I,D
        self.L2pid = "45.0,23.0,0.0" # Analog Output P,I,D
        self.L1power = 0.00 # Heater Power %
        self.L1range = 1 # Heater Power Range
        self.L2power = 0.00 # Probe Heater Power %
        self.L2range = 2 # Probe Power Range
        self.L1mout = 23.00 # Sensor A manual output %
        self.L2mout = 33.00 # Sensor B manual output %
        self.L1ctrl = "1,1" # Control loop 1 parameters
        self.L2ctrl = "2,1" # Control loop 2 parameters
        self.zone = "ON" # If ON, PID and control loop parameters are automatically changed with the setpoint following tables stored in the configuration file. If OFF allows the user to set arbitrary power output
        self.tcstatus = "Sensor A: Temperature stable... Sensor B: Temperature stable..." # VTI control status
        self.nv = 0.608696 # Needle Valve position mm
        self.pressure = "17.623276,13.796360" # Needle Valve Pressure Target, Actual Pressure
        self.valvestatus  = "Idle" # Needle valve status
        self.helevel = 453.00 # current helium level in mm
        self.nlevel = 121.00 # current nitrogen level in mm
        self.hefrequency = 1 # He level gauge reading frequency
        self.persistmode = "ON" # Check the persistence mode, if ON, heater is switched off at field
        self.attoangle = 117.999200 # attocube positioner angle (degrees)
