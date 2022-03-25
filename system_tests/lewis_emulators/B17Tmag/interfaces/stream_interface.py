from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class B17TmagStreamInterface(StreamInterface):
    commands = {
        # TODO: Commands and methods are currently not complete
        # Get commands
        CmdBuilder("getField").escape("ouput").eos().build(),
        # CmdBuilder("getHeater").escape("heater").eos().build(),
        # CmdBuilder("getPersist").escape("persistent").eos().build(),
        # CmdBuilder("getPersistMode").escape("persistmode").eos().build(),
        # CmdBuilder("getReady").escape("ready").eos().build(),
        # CmdBuilder("getSensA").escape("sensA").eos().build(),
        # CmdBuilder("getSensB").escape("senBb").eos().build(),
        # CmdBuilder("getSet1").escape("setpoint1").eos().build(),
        # CmdBuilder("getSet2").escape("setpoint2").eos().build(),
        # CmdBuilder("getNeedlePosition").escape("nv").eos().build(),
        # CmdBuilder("getPressure").escape("pressure").eos().build(),
        # CmdBuilder("getAttoAngle").escape("attoangle").eos().build(),
        # CmdBuilder("getHeLevel").escape("helevel").eos().build(),
    
        # Set commands
        # CmdBuilder("setField").escape("setfield").arg("[0-9]{1}").eos().build(),
        # CmdBuilder("setPersistMode").escape("setpersistmode").arg("(ON|OFF)").eos().build(),
        # CmdBuilder("setPersistMode").escape("setpersistmode").arg("^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$").eos().build(), # matches 123 123.456 .456 123. numbers
        # CmdBuilder("setSet1").escape("set1").eos().build(),
        # CmdBuilder("setSet2").escape("set2").eos().build(),
        # CmdBuilder("setPressure").escape("setpressur").eos().build(),
        # CmdBuilder("setNeedlePosition").escape("setposition").eos().build(),
        # CmdBuilder("setAttoAngle").escape("setangle").eos().build(),
        # CmdBuilder("setMacroStatus").escape("getstatus").eos().build(),
    }

    in_terminator = "\r\n"
    out_terminator = "\n"

    def __init__(self):
        super(B17TmagStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        # self.commands = {
        #     CmdBuilder(self.catch_all).arg("^#9.*$").build()  # Catch-all command for debugging
        # }

    def getField(self):
        print("getField called")
        device_in = self._device.output
        return f"OK:{device_in}"

    def getHeater(self):
        print("getHeater called")
        device_in = self._device.heater
        return f"heater:OK:{device_in}"

    def getPersist(self):
        print("getPersist called")
        device_in = self._device.persist
        return f"persist:OK:{device_in}"

    def getPersistMode(self):
        pass

    def getReady(self):
        pass

    def getSensA(self):
        pass

    def getSensB(self):
        pass

    def getSet1(self):
        pass

    def getSet2(self):
        pass

    def getPressure(self):
        pass

    def getNeedlePosition(self):
        pass

    def getAttoAngle(self):
        pass

    def getHeLevel(self):
        pass


    def setField(self):
        pass

    def setPersistMode(self):
        pass

    def setSet1(self):
        pass

    def setSet2(self):
        pass

    def setPressure(self):
        pass

    def setNeedlePosition(self):
        pass

    def setAttoAngle(self):
        pass

    def setMacroStatus(self):
        pass


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
