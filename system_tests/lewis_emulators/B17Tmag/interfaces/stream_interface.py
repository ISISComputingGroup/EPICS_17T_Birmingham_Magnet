from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class B17TmagStreamInterface(StreamInterface):
    commands = {
        # TODO: Commands and methods are currently not complete
        # Get commands
        # had to remove .eos().build() to fix emulator
        CmdBuilder("getField").escape("output").build(),
        CmdBuilder("getHeater").escape("heater").build(),
        CmdBuilder("getPersist").escape("persistent").build(),
        CmdBuilder("getPersistMode").escape("persistmode").build(),
        CmdBuilder("getReady").escape("ready").build(),
        CmdBuilder("getSensA").escape("sensA").build(),
        CmdBuilder("getSensB").escape("sensB").build(),
        CmdBuilder("getSet1").escape("setpoint1").build(),
        CmdBuilder("getSet2").escape("setpoint2").build(),
        CmdBuilder("getNeedlePosition").escape("nv").build(),
        CmdBuilder("getPressure").escape("pressure").build(),
        CmdBuilder("getAttoAngle").escape("attoangle").build(),
        CmdBuilder("getHeLevel").escape("helevel").build(),
        CmdBuilder("getMacroStatus").escape("getstatus").build(),
    
        # # Set commands?:apple|banana
         CmdBuilder("abort").escape("abort").eos().build(),
        CmdBuilder("setField").escape("setfield:").arg("[0-9]{1,3}").eos().build(),
        # CmdBuilder("setPersistMode").escape("setpersistmode").arg("^.{3}$|^.{3}$").eos().build(),
        CmdBuilder("setPersistMode").escape("setpersistmode").arg("ON|OFF").eos().build(),
        # CmdBuilder("setSet1").escape("set1").arg("[0-9]{1,2}.[0-9].[0-9]+").eos().build(),
        CmdBuilder("setSet1").escape("set1").float().eos().build(),
        # CmdBuilder("setSet2").escape("set2").arg("[0-9]{1,2}.[0-9].[0-9]+").eos().build(),
        CmdBuilder("setSet2").escape("set2").float().eos().build(),
        # CmdBuilder("setPressure").escape("setpressure ").arg("[0-9]{0,2}.[0-9]+").eos().build(),
        CmdBuilder("setPressure").escape("setpressure ").float().eos().build(),
        # CmdBuilder("setNeedlePosition").escape("setposition ").arg("[0-9]{1,2}.[0-9]+").eos().build(),
        CmdBuilder("setNeedlePosition").escape("setposition ").float().eos().build(),
        CmdBuilder("setAttoAngle").escape("setangle").arg("[0-2]?[0-9]{1,2}.[0-9]+|3[0-5][0-9].[0-9]+|360.[0-9]+").eos().build(),
        # CmdBuilder("setAttoAngle").escape("setangle").arg("[+-]?[0-9]+\.[0-9]+").eos().build(),
    }
    
    in_terminator = "\n"
    out_terminator = "\n"

    def __init__(self):
        super().__init__()

    # Get commands
    def getField(self):
        """
        Gets the current FIELD value from the device. The FIELD type returned is Tesla.
        """
        print("getField called")
        device_in = f"{self._device.field_T}T,{self._device.curr_A}A"
        return f"{device_in}" 

    def getHeater(self):
        """
        Gets the heater value from the device. 
        The heater value will be one of 4 possible values: 
        - 0:ON
        - 1:OFF
        - 2:OFF AT FIELD
        - 3:NO MATCH
        """
        print("getHeater called")
        device_in = self._device.heater
        return f"heater:OK:{device_in}"

    def getPersist(self):
        """
        Gets the current field and current of the magnet at present from the device. 
        The field is returned in Telsa and the current is returned in Amps.
        """
        print("getPersist called")
        device_in = self._device.persistent
        # return f"persistent:OK:{device_in}"
        return f"{device_in}"

    def getPersistMode(self):
        """
        Retreive whetehr or not the magnet is in persistent mode or not.
        The mode can either be 'ON' or 'OFF'
        """
        print("getPersistMode called")
        device_in = self._device.persistmode
        return device_in

    def getReady(self):
        """
        Retrieve whether or not the magent is stable and at field.
        The two possible modes that be returned from the device are 'ON' or 'OFF'
        """
        print("getReady called")
        device_in = self._device.ready
        return f"ready:OK:{device_in}"

    def getSensA(self):
        """
        Get the temperature at sensor A in Kelvin from the device
        """
        print("getSensA called")
        device_in = self._device.sensA
        return f"sensA:OK:{device_in}"

    def abort(self):
        """
        abort
        """
        print("Abort ran")
        return f"abort:OK:"
        

    def getSensB(self):
        """
        Get the temperature at sensor B in Kelvin from the device
        """
        print("getSensB called")
        device_in = self._device.sensB
        return f"sensB:OK:{device_in}"

    def getSet1(self):
        """
        Get the temperature for setpoint 1 in Kelvin from the device
        """
        print("getSet1 called")
        device_in = self._device.setpoint1
        return f"{device_in}"

    def getSet2(self):
        """
        Get the temperature for setpoint 2 in Kelvin from the device
        """
        print("getSet2 called")
        device_in = self._device.setpoint2
        return f"{device_in}"

    def getPressure(self):
        """
        Get the current pressure target and current actual pressure in mbar from the device
        """
        print("getPressure called")
        pressure_readback_value = self._device.pressure
        needlevalve_pressure = self._device.needle_valve_pressure
        return f"pressure:OK:{pressure_readback_value},{needlevalve_pressure}" # comma needed?
        # return pressure_readback_value, needlevalve_pressure

    def getNeedlePosition(self):
        """
        Get the position of the needle valve from the device in mm
        """
        print("getNeedlePosition called")
        device_in = self._device.nv
        return f"nv:OK:{device_in}"

    def getAttoAngle(self):
        """
        Get the angle of the attocube in degrees from the device
        """
        print("getAttoAngle called")
        device_in = self._device.attoangle
        return f"attoangle:OK:{device_in}"

    def getHeLevel(self):
        """
        Get the current level of helium as a percentage of 243 from the device.
        """
        ### converted to percentage of 243 
        # (device divides returned value by 243 then multiplies by 100)
        print("getHeLevel called")
        device_in = self._device.helevel
        # helevel = (device_in/243)*100
        # return f"helevel:OK:{device_in}"
        return f"{device_in}"

    def getMacroStatus(self):
        """
        If MACRO:STAT:READ is true, can get macro status. 
        Otherwise, Macro Status should be disabled.
        """
        print("getMacroStatus called")
        device_in = self._device.macrostatus
        # return f"getstatus:OK:{device_in}"
        return f"{device_in}"

    # Set commands

    def setField(self, command):
        """
        Sets the new target FIELD value to the device. The FIELD type returned is Tesla.
        The protocol function will run abort before sending the new field value.
        """
        print("Setting Field")
        self._device.field_T = command
        return f"setfield:{command}"

    def setPersistMode(self, command):
        """
        Sets the persist mode to either 'ON' or 'OFF' on the device
        """
        print(f"Setting persist mode from {self._device.persistmode} to: {command}")
        self._device.persistmode = command
        return f"{command}"

    def setSet1(self, command):
        """
        Set the temperature for setpoint 1 in Kelvin on the device
        """
        print(f"Setting setpoint1 from {self._device.setpoint2} to: {command}")
        self._device.setpoint1 = command
        return f"set1:{command}"

    def setSet2(self, command):
        """
        Set the temperature for setpoint 2 in Kelvin on the device
        """
        print(f"Setting setpoint2 from {self._device.setpoint2} to: {command}")
        self._device.setpoint2 = command
        return f"set2:{command}"

    def setPressure(self, command):
        """
        Get the pressure target in mbar on the device
        """
        print(f"Setting pressure from {self._device.pressure} to: {command}")
        self._device.pressure = command
        return f"setpressure:{command}"

    def setNeedlePosition(self, command):
        """
        Set the position of the needle valve on the device in mm
        """
        print(f"Setting needle position from {self._device.nv} to: {command}")
        self._device.nv_pos = command
        return f"setposition:{command}"

    def setAttoAngle(self, command):
        """
        Set the angle of the attocube in degrees on the device
        """
        print(f"Setting atto angle from {self._device.attoangle} to: {command}")
        self._device.attoangle = command
        return f"setangle:{command}"

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def catch_all(self, command):
        pass
