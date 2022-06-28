import unittest
from time import sleep

from utils.test_modes import TestModes
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.testing import get_running_lewis_and_ioc, assert_log_messages, skip_if_recsim, unstable_test
from parameterized import parameterized



DEVICE_PREFIX = "B17TMAG_01"

EMULATOR_DEVICE = "B17Tmag"

IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("B17TMAG"),
        "emulator": EMULATOR_DEVICE,
        "emulator_id": "b17Tmag",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class B17TmagTests(unittest.TestCase):
    """
    Tests for the B17Tmag IOC.
    """
    def setUp(self):
        self.lewis, self.ioc = get_running_lewis_and_ioc("b17Tmag", DEVICE_PREFIX)
        self.ca = ChannelAccess(default_timeout=20, default_wait_time=0.0, device_prefix=DEVICE_PREFIX)
        self.lewis.backdoor_run_function_on_device("re_initialise")

    # @parameterized.expand([
    #     ("EM_PRESSURE", "EM_PRESSURE",  0, "Stop", 1),
    #     ("MX_PRESSURE", "MX_PRESSURE", 13, 1000, 1000)
    # ])
    # def test_WHEN_pv_set_THEN_pv_and_buffer_readback_correctly(self, _, pv_record, buffer_location, setpoint_value, buffer_value):
    #     self.ca.set_pv_value("{}:SP".format(pv_record), setpoint_value)
    #     self.ca.assert_that_pv_is(pv_record, setpoint_value)
    #     self.ca.assert_that_pv_is("STATUS_ARRAY.[{}]".format(buffer_location), buffer_value)


    @parameterized.expand([
        ("FIELD", "FIELD", 10),
        ("MODE_PERSIST", "MODE:PERSIST:SP", "ON"),
        ("ATTO_POS", "ATTO:POS:SP", 200),
        ("NV_POS", "NV:POS:SP", 10),
        ("NV_PRESSURE", "NV:PRESSURE:SP", 60),
        ("TEMP_SET1", "TEMP:SET1:SP", 20),
        ("TEMP_SET2", "TEMP:SET2:SP", 22)
    ])
    def test_When_PV_set_THEN_pv_readback_correctly(self, _, pv_record, setpoint_value):
        self.ca.set_pv_value("{}".format(pv_record), setpoint_value)
        self.ca.assert_that_pv_is(pv_record, setpoint_value)

    @parameterized.expand([
    ("Positive_Large_Int", 1234, 503.6734693877551),
    ("Positive_Small_Int", 50, 20.408163265306122),
    ("Negative_Small_Int", -10, -4.081632653061225),
    ])
    def test_WHEN_helevel_raw_set_THEN_helevel_readback_percentage(self, _, input, expected):
    #     # self.helevel = input
    #     self.ca.set_pv_value("HE:LEVEL_RAW", input)
    #     self.ca.assert_that_pv_is("HE:LEVEL", expected)
        self.lewis.backdoor_set_on_device("helevel", input)
        self.ca.assert_that_pv_is("HE:LEVEL", expected)



    @parameterized.expand([
        ("MACROSTATREADENABLED", 0),
        ("MACROSTATREADDISABLED", 1)
    ])
    def test_WHEN_macro_read_set_THEN_macro_stat_scan_rate_toggled_appropriately(self, _, value):
        self.ca.set_pv_value("MACRO:STAT:READ", value)
        self.ca.assert_that_pv_is("MACRO:STAT.DISA", value)

    # Test setting of Mode:PERSIST:SP and reading of MODE:PERSIST
    # def test_WHEN_mode_persist_set_THEN_mode_persist_readback_correctly(self):
    #     self.ca.set_pv_value("MODE:PERSIST:SP", "ON")
    #     self.ca.assert_that_pv_is("MODE:PERSIST", "ON")

    def test_WHEN_macro_set_THEN_macro_readback_correctly(self):
        self.ca.set_pv_value("HE:LEVEL_RAW", 50)
        self.ca.assert_that_pv_is("output1.000000fT,10.000000A;voltage1.253;heater0;ramprate1.234;units0;target1.000000fT,10.000000A;persistent0.0T,0.0A;psustatusUnabletocommunicatewithPSU.Pleasecheckinterfaceandmainscables.Initialisationfailed.;pausestatusOFF;tblstatus1.000000fT,10.000000A;readyON;sensA0.0;sensB0.0;setpoint10.0;setpoint20.0;L1pid50.0,20.0,0.0;L2pid45.0,23.0,0.0;L1power0.0;L1range1;L2power0.0;L2range2;L1mout23.0;L2mout33.0;L1ctrl1,1;L2ctrl2,1;zoneON;tcstatusSensorA:Temperaturestable...SensorB:Temperaturestable...;nv0.608696;pressure17.623276,13.796360;valvestatusIdle;helevel0;nlevel121.0;hefrequency1;persistmodeOFF;attoangle117.9992;")