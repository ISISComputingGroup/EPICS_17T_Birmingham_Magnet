from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class B17TmagStreamInterface(StreamInterface):
    commands = {
        # TODO: Commands and methods are currently not complete
        # Get commands
        CmdBuilder("getField").escape("output").eos().build(),
        CmdBuilder("getHeater").escape("heater").eos().build(),
        CmdBuilder("getPersist").escape("persistent").eos().build(),
        CmdBuilder("getPersistMode").escape("persistmode").eos().build(),
        CmdBuilder("getReady").escape("ready").eos().build(),
        CmdBuilder("getSensA").escape("sensA").eos().build(),
        CmdBuilder("getSensB").escape("sensB").eos().build(),
        CmdBuilder("getSet1").escape("setpoint1").eos().build(),
        CmdBuilder("getSet2").escape("setpoint2").eos().build(),
        CmdBuilder("getNeedlePosition").escape("nv").eos().build(),
        CmdBuilder("getPressure").escape("pressure").eos().build(),
        CmdBuilder("getAttoAngle").escape("attoangle").eos().build(),
        # CmdBuilder("getHeLevel").escape("helevel").eos().build(),
        CmdBuilder("getMacroStatus").escape("getstatus").eos().build(),
    
        # Set commands
        CmdBuilder("setField").escape("setfield:").arg("[0-9]{1,3}").eos().build(),
        CmdBuilder("setPersistMode").escape("setpersistmode").arg("ON|OFF$").eos().build(),
        # CmdBuilder("setPersistMode").escape("setpersistmode").arg("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$").eos().build(), # matches 123 123.456 .456 123. numbers
        CmdBuilder("setSet1").escape("set1").arg("[0-9]{1,2}").eos().build(),
        CmdBuilder("setSet2").escape("set2").arg("[0-9]{1,2}").eos().build(),
        CmdBuilder("setPressure").escape("setpressur").arg("[0-9]{1,2}.[0-9]{2}").eos().build(),
        CmdBuilder("setNeedlePosition").escape("setposition").arg("[0-9]{1,2}.[0-9]{2}").eos().build(),
        CmdBuilder("setAttoAngle").escape("setangle").arg("[0-2]?[0-9]{1,2}.[0-9]{2}|3[0-5][0-9].[0-9]{2}|360.00").eos().build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\n"

    def __init__(self):
        super(B17TmagStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        # self.commands = {
        #     CmdBuilder(self.catch_all).arg("^#9.*$").build()  # Catch-all command for debugging
        # }

    # Get commands

    def getField(self):
        """

        """
        print("getField called")
        device_in = f"{self._device.field_T}T,{self._device.curr_A}A"
        return f"OK:{device_in}" 

    def getHeater(self):
        """
        
        """
        print("getHeater called")
        device_in = self._device.heater
        return f"heater:OK:{device_in}"

    def getPersist(self):
        """
        
        """
        print("getPersist called")
        device_in = self._device.persistent
        return f"persist:OK:{device_in}"

    def getPersistMode(self):
        """
        
        """
        print("getPersistMode called")
        device_in = self._device.persistmode
        return f"persistmode:OK:{device_in}"

    def getReady(self):
        """
        
        """
        print("getReady called")
        device_in = self._device.ready
        return f"ready:OK:{device_in}"

    def getSensA(self):
        """
        
        """
        print("getSensA called")
        device_in = self._device.sensA
        return f"sensA:OK:{device_in}"

    def getSensB(self):
        """
        
        """
        print("getSensB called")
        device_in = self._device.sensB
        return f"sensB:OK:{device_in}"

    def getSet1(self):
        """
        
        """
        print("getSet1 called")
        device_in = self._device.setpoint1
        return f"setpoint1:OK:{device_in}"

    def getSet2(self):
        """
        
        """
        print("getSet2 called")
        device_in = self._device.setpoint2
        return f"setpoint2:OK:{device_in}"

    def getPressure(self):
        """
        
        """
        print("getPressure called")
        device_in = self._device.pressure
        return f"pressure:OK:{device_in}"

    def getNeedlePosition(self):
        """
        
        """
        print("getNeedlePosition called")
        device_in = self._device.nv
        return f"nv:OK:{device_in}"

    def getAttoAngle(self):
        """
        
        """
        print("getAttoAngle called")
        device_in = self._device.attoangle
        return f"attoangle:OK:{device_in}"

    def getHeLevel(self):
        """
        
        """
        ### convert to percentage of 243 (divide returned value by 243 then mul.tiply by 100)
        print("getHeLevel called")
        device_in = self._device.helevel
        helevel = (device_in/243)*100
        return f"helevel:OK:{helevel}"

    def getMacroStatus(self):
        """
        If MACRO:STAT:READ is true, can get macro status. Otherwise, Macro Status shoul;d be disabled.
        """
        print("getMacroStatus called")
        device_in = self._device.macrostatus
        return f"getstatus:OK:{device_in}"

    # Set commands

    def setField(self, command):
        """
        
        """
        print("Setting Field")
        self._device.field_T = command
        return f"OK:Field set to {command}"

    def setPersistMode(self, command):
        """
        
        """
        print(f"Setting persist mode from {self._device.persistmode} to: {command}")
        self._device.persistmode = command
        return f"OK:Persist mode set to {command}"

    def setSet1(self, command):
        """
        
        """
        print(f"Setting setpoint1 from {self._device.setpoint2} to: {command}")
        self._device.setpoint1 = command
        return f"OK:Setpoint1 set to {command}"

    def setSet2(self, command):
        """
        
        """
        print(f"Setting setpoint2 from {self._device.setpoint2} to: {command}")
        self._device.setpoint2 = command
        return f"OK:Setpoint2 set to {command}"

    def setPressure(self, command):
        """
        
        """
        print(f"Setting pressure from {self._device.pressure} to: {command}")
        self._device.pressure = command
        return f"OK:Pressure set to {command}"

    def setNeedlePosition(self, command):
        """
        
        """
        print(f"Setting needle position from {self._device.nv} to: {command}")
        self._device.nv_pos = command
        return f"OK:Needle position set to {command}"

    def setAttoAngle(self, command):
        """
        
        """
        print(f"Setting atto angle from {self._device.attoangle} to: {command}")
        self._device.attoangle = command
        return f"OK:Atto angle set to {command}"

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
