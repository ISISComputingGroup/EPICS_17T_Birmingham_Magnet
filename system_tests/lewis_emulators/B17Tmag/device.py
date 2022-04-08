from lewis.devices import StateMachineDevice
from lewis.core import approaches
from .states import DefaultState
from collections import OrderedDict


class SimulatedB17Tmag(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        # When the device is in an error state it can respond with junk
        self.is_giving_errors = False
        self.out_error = "}{<7f>w"
        self.out_terminator_in_error = ""
        self.output = "10T,20A"
        self.heater = 0
        self.persist = "10fT,20A"
        self.persistmode = "OFF"
        self.ready = "OFF"
        self.sensA = 0.0
        self.sensB = 0.0
        self.setpoint1 = 0
        self.setpoint2 = 0
        self.nv_pos = 0
        self.pressure = 0.0
        self.attoangle = 0.00
        self.helevel = 0.0
        self.macrostatus = 0.0

        

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

