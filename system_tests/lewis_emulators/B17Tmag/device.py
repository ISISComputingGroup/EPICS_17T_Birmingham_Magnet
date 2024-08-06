from collections import OrderedDict

from lewis.core.logging import has_log
from lewis.devices import StateMachineDevice

from .states import DefaultState


@has_log
class SimulatedB17Tmag(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.log.info("INITIALIZING DATA")
        self.re_initialise()

    def _get_state_handlers(self):
        return {"default": DefaultState()}

    def _get_initial_state(self):
        return "default"

    def _get_transition_handlers(self):
        return OrderedDict([])

    def re_initialise(self):
        """
        Setting values device is initially set with when it is first turned on
        Values are set based on those set in the manual for Birmingham 17T magnet.
        """
        self.log.info("reinitializing")
        self.connected = True

        self.field_T = 1.000000  # Output of the power supply in Tesla (T) and Amps (A)
        self.curr_A = 10.000000
        self.voltage = 1.253000  # Voltage measured across the terminals of the main power supply
        self.heater = 0  # Main coil heater status
        self.ramprate = 1.234000  # Current ramp rate
        self.units = 0  # Current ramp rate units
        self.psustatus = "Unable to communicate with PSU. Please check interface and mains cables. Initialisation failed."
        self.pausestatus = "OFF"  # Power supply pause status
        self.tblstatus = "1.000000fT,10.000000A"  # Ignore table status. If ON, ramp rates set by the user with the ‘ramp rate’ command are limited by the table stored in the configuration file; if OFF, ramp rates follow the table and the ‘set rate’ command is ignored.
        self.ready = (
            True  # Indicates if the power supply software is busy completing its current task
        )
        self.sensA = 0.000  # Current Temp Heat Exchanger
        self.sensB = 0.000  # Current Temp Probe
        self.setpoint1 = 0.000  # Current Setpoint Heat Exchanger
        self.setpoint2 = 0.000  # Current Setpoint Probe
        self.L1pid = "50.0,20.0,0.0"  # Heat Exchanger P,I,D
        self.L2pid = "45.0,23.0,0.0"  # Analog Output P,I,D
        self.L1power = 0.00  # Heater Power %
        self.L1range = 1  # Heater Power Range
        self.L2power = 0.00  # Probe Heater Power %
        self.L2range = 2  # Probe Power Range
        self.L1mout = 23.00  # Sensor A manual output %
        self.L2mout = 33.00  # Sensor B manual output %
        self.L1ctrl = "1,1"  # Control loop 1 parameters
        self.L2ctrl = "2,1"  # Control loop 2 parameters
        self.zone = "ON"  # If ON, PID and control loop parameters are automatically changed with the setpoint following tables stored in the configuration file. If OFF allows the user to set arbitrary power output
        self.tcstatus = (
            "Sensor A: Temperature stable... Sensor B: Temperature stable..."  # VTI control status
        )
        self.nv = 0.608696  # Needle Valve position mm
        self.nv_pressure = 17.623276  # Needle Valve Pressure (Actual Pressure)
        self.nv_pressure_sp = 13.796360  # Needle Valve Pressure Target (Setpoint)
        self.valvestatus = "Idle"  # Needle valve status
        self.helevel = 453.00  # current helium level in mm
        self.nlevel = 121.00  # current nitrogen level in mm
        self.hefrequency = 1  # He level gauge reading frequency 1
        self.persistmode = (
            False  # Check the persistence mode, if ON, heater is switched off at field
        )
        self.attoangle = 117.999200  # attocube positioner angle (degrees)
