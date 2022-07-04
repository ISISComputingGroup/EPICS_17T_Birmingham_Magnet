from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class B17TmagStreamInterface(StreamInterface):
    commands = {
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
        CmdBuilder("getHeLevel").escape("helevel").eos().build(),
        CmdBuilder("getMacroStatus").escape("getstatus").eos().build(),

        # Set commands
        CmdBuilder("abort").escape("abort").eos().build(),
        CmdBuilder("setField").escape("setfield ").float().eos().build(),
        CmdBuilder("setPersistMode").escape("setpersist ").arg("ON|OFF").eos().build(),
        CmdBuilder("setSet1").escape("set1 ").float().eos().build(),
        CmdBuilder("setSet2").escape("set2 ").float().eos().build(),
        CmdBuilder("setPressure").escape("setpressure ").float().eos().build(),
        CmdBuilder("setNeedlePosition").escape("setposition ").float().eos().build(),
        CmdBuilder("setAttoAngle").escape("setangle").float().eos().build(),
    }
    
    in_terminator = "\n"
    out_terminator = "\n"

    # Get commands
    @conditional_reply("connected")
    def getField(self):
        """
        Gets the current FIELD value from the device. The FIELD type returned is Tesla.
        """
        return f"output:OK:{self._device.field_T}T,{self._device.curr_A}A"

    @conditional_reply("connected")
    def getHeater(self):
        """
        Gets the heater value from the device. 
        The heater value will be one of 4 possible values: 
        - 0:ON
        - 1:OFF
        - 2:OFF AT FIELD
        - 3:NO MATCH
        """
        return f"heater:OK:{self._device.heater}"

    @conditional_reply("connected")
    def getPersist(self):
        """
        Gets the current field and current of the magnet at present from the device. 
        The field is returned in Telsa and the current is returned in Amps.
        """
        if self._device.persistmode:
            return f"persistent:OK:{self._device.field_T}T,{self._device.curr_A}A"
        else:
            return "persistent:OK:0.00T,0.00A"

    @conditional_reply("connected")
    def getPersistMode(self):
        """
        Retreive whetehr or not the magnet is in persistent mode or not.
        The mode can either be 'ON' or 'OFF'
        """
        return f"persistmode:OK:{'ON' if self._device.persistmode else 'OFF'}"

    @conditional_reply("connected")
    def getReady(self):
        """
        Retrieve whether or not the magent is stable and at field.
        The two possible modes that be returned from the device are 'ON' or 'OFF'
        """
        return f'ready:OK:{"ON" if self._device.ready else "OFF"}'

    @conditional_reply("connected")
    def getSensA(self):
        """
        Get the temperature at sensor A in Kelvin from the device
        """
        return f"sensA:OK:{self._device.sensA}"

    @conditional_reply("connected")
    def abort(self):
        """
        abort
        """
        return f"abort:OK:"

    @conditional_reply("connected")
    def getSensB(self):
        """
        Get the temperature at sensor B in Kelvin from the device
        """
        return f"sensB:OK:{self._device.sensB}"

    @conditional_reply("connected")
    def getSet1(self):
        """
        Get the temperature for setpoint 1 in Kelvin from the device
        """
        return f"setpoint1:OK:{self._device.setpoint1}"

    @conditional_reply("connected")
    def getSet2(self):
        """
        Get the temperature for setpoint 2 in Kelvin from the device
        """
        return f"setpoint2:OK:{self._device.setpoint2}"

    @conditional_reply("connected")
    def getPressure(self):
        """
        Get the current pressure target and current actual pressure in mbar from the device
        """
        return f"pressure:OK:{self._device.nv_pressure},{self._device.nv_pressure_sp}"

    @conditional_reply("connected")
    def getNeedlePosition(self):
        """
        Get the position of the needle valve from the device in mm
        """
        return f"nv:OK:{self._device.nv}"

    @conditional_reply("connected")
    def getAttoAngle(self):
        """
        Get the angle of the attocube in degrees from the device
        """
        return f"attoangle:OK:{self._device.attoangle}"

    @conditional_reply("connected")
    def getHeLevel(self):
        """
        Get the current level of helium as a percentage of 243 from the device.
        """
        return f"helevel:OK:{self._device.helevel}"

    @conditional_reply("connected")
    def getMacroStatus(self):
        """
        If MACRO:STAT:READ is true, can get macro status. 
        Otherwise, Macro Status should be disabled.
        """
        device_status_string_list = [
            f"output {self._device.field_T}T,{self._device.curr_A}A;",
            f"voltage {self._device.voltage};",
            f"heater {self._device.heater};",
            f"ramprate {self._device.ramprate};",
            f"units {self._device.units};",
            f"target {self._device.field_T}T,{self._device.curr_A}A;",
            f"persistent {self._device.field_T if self._device.persistmode else 0.0}T,"
            f"{self._device.curr_A if self._device.persistmode else 0.0}A;",
            f"psustatus {self._device.psustatus};",
            f"pausestatus {self._device.pausestatus};",
            f"tblstatus {self._device.tblstatus};",
            f"ready {'ON' if self._device.ready else 'OFF'};",
            f"sensA {self._device.sensA};",
            f"sensB {self._device.sensB};",
            f"setpoint1 {self._device.setpoint1};",
            f"setpoint2 {self._device.setpoint2};",
            f"L1pid {self._device.L1pid};",
            f"L2pid {self._device.L2pid};",
            f"L1power {self._device.L1power};",
            f"L1range {self._device.L1range};",
            f"L2power {self._device.L2power};",
            f"L2range {self._device.L2range};",
            f"L1mout {self._device.L1mout};",
            f"L2mout {self._device.L2mout};",
            f"L1ctrl {self._device.L1ctrl};",
            f"L2ctrl {self._device.L2ctrl};",
            f"zone {self._device.zone};",
            f"tcstatus {self._device.tcstatus};",
            f"nv {self._device.nv};",
            f"pressure {self._device.nv_pressure},{self._device.nv_pressure_sp};",
            f"valvestatus {self._device.valvestatus};",
            f"helevel {self._device.helevel};",
            f"nlevel {self._device.nlevel};",
            f"hefrequency {self._device.hefrequency};",
            f"persistmode {'ON' if self._device.persistmode else 'OFF'};",
            f"attoangle {self._device.attoangle};"
        ]

        return f"getstatus:OK:{''.join(device_status_string_list)}"

    # Set commands
    @conditional_reply("connected")
    def setField(self, command):
        """
        Sets the new target FIELD value to the device. The FIELD type returned is Tesla.
        The protocol function will run abort before sending the new field value.
        """
        self._device.field_T = command
        return f"setfield:{command}"

    @conditional_reply("connected")
    def setPersistMode(self, command):
        """
        Sets the persist mode to either 'ON' or 'OFF' on the device
        """
        assert command in ["ON", "OFF"]
        self._device.persistmode = command == "ON"
        return f"setpersist:OK:{command}"

    @conditional_reply("connected")
    def setSet1(self, command):
        """
        Set the temperature for setpoint 1 in Kelvin on the device
        """
        self._device.setpoint1 = command
        return f"set1:{command}"

    @conditional_reply("connected")
    def setSet2(self, command):
        """
        Set the temperature for setpoint 2 in Kelvin on the device
        """
        self._device.setpoint2 = command
        return f"set2:{command}"

    @conditional_reply("connected")
    def setPressure(self, command):
        """
        Get the pressure target in mbar on the device
        """
        self._device.nv_pressure = command
        self._device.nv_pressure_sp = command
        return f"setpressure:{command}"

    @conditional_reply("connected")
    def setNeedlePosition(self, command):
        """
        Set the position of the needle valve on the device in mm
        """
        self._device.nv = command
        return f"setposition:{command}"

    @conditional_reply("connected")
    def setAttoAngle(self, command):
        """
        Set the angle of the attocube in degrees on the device
        """
        assert 0 <= command < 361, f"Invalid attocube angle {command}"
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
