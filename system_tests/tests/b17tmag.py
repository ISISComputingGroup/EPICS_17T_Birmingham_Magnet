import contextlib
import time
import unittest
from time import sleep

from utils.test_modes import TestModes
from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.testing import get_running_lewis_and_ioc, assert_log_messages, skip_if_recsim, unstable_test, parameterized_list
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

READ_PVS = [
    "FIELD",
    "CURR",
    "MODE:PERSIST",
    "ATTO:POS",
    "NV:POS",
    "NV:PRESSURE",
    "TEMP:SET1",
    "TEMP:SET2",
    "HE:LEVEL",
    "TEMP:A",
    "TEMP:B",
    "READY",
]


class B17TmagTests(unittest.TestCase):
    """
    Tests for the B17Tmag IOC.
    """
    def setUp(self):
        self.lewis, self.ioc = get_running_lewis_and_ioc("b17Tmag", DEVICE_PREFIX)
        self.ca = ChannelAccess(default_timeout=5, default_wait_time=0.0, device_prefix=DEVICE_PREFIX)
        self.lewis.backdoor_run_function_on_device("re_initialise")
        self.ca.set_pv_value("MACRO:STAT:READ", 1)

    @parameterized.expand(parameterized_list([
        ("FIELD", [1.2345, 17]),
        ("MODE:PERSIST", ["ON", "OFF"]),
        ("ATTO:POS", [200, 98.765]),
        ("NV:POS", [0, 12.345]),
        ("NV:PRESSURE", [0, 12.345]),
        ("TEMP:SET1", [0, 12.345]),
        ("TEMP:SET2", [0, 12.345]),
        ("TEMP:HEATEX", [0, 12.345]),
        ("TEMP:PROBE", [0, 12.345]),
    ]))
    def test_When_setpoint_set_THEN_pv_readback_updates(self, _, pv_record, values):
        for value in values:
            self.ca.assert_setting_setpoint_sets_readback(value, pv_record)

    @parameterized.expand(parameterized_list([
        ("field_T", "FIELD", [1.2345, 17]),
        ("curr_A", "CURR", [1.2345, 100]),
        ("sensA", "TEMP:A",  [1.2345, 100]),
        ("sensB", "TEMP:B", [1.2345, 100]),
        ("setpoint1", "TEMP:SET1", [1.2345, 100]),
        ("setpoint1", "TEMP:HEATEX", [1.2345, 100]),
        ("setpoint2", "TEMP:SET2", [1.2345, 100]),
        ("setpoint2", "TEMP:PROBE", [1.2345, 100]),
        ("nv_pressure", "NV:PRESSURE", [1.2345, 100]),
        ("nv_pressure_sp", "NV:PRESSURE:SP:RBV", [1.2345, 100]),
        ("nv", "NV:POS", [1.2345, 100]),
    ]))
    @skip_if_recsim("Requires lewis backdoor")
    def test_WHEN_backdoor_property_set_THEN_readback_updates(self, _, backdoor_name, pv_name, values):
        for value in values:
            self.lewis.backdoor_set_and_assert_set(backdoor_name, value)
            self.ca.assert_that_pv_is_number(pv_name, value, tolerance=0.0001)

    @skip_if_recsim("requires lewis backdoor")
    def test_WHEN_heater_set_via_backdoor_THEN_pv_updates(self):
        self.lewis.backdoor_set_on_device("heater", 0)
        self.ca.assert_that_pv_is("HEATER", "ON")
        self.lewis.backdoor_set_on_device("heater", 1)
        self.ca.assert_that_pv_is("HEATER", "OFF")
        self.lewis.backdoor_set_on_device("heater", 2)
        self.ca.assert_that_pv_is("HEATER", "OFF AT FIELD")
        self.lewis.backdoor_set_on_device("heater", 3)
        self.ca.assert_that_pv_is("HEATER", "NO MATCH")

    @skip_if_recsim("requires lewis backdoor")
    def test_WHEN_ready_set_via_backdoor_THEN_pv_updates(self):
        self.lewis.backdoor_set_on_device("ready", True)
        self.ca.assert_that_pv_is("READY", "ON")
        self.lewis.backdoor_set_on_device("ready", False)
        self.ca.assert_that_pv_is("READY", "OFF")

    @parameterized.expand([
        ("Positive_Large_Int", 1234, 507.819),
        ("Positive_Small_Int", 50, 20.576),
        ("Negative_Small_Int", -10, -4.115),
    ])
    @skip_if_recsim("Requires emulator backdoor")
    def test_WHEN_helevel_raw_set_THEN_helevel_readback_percentage(self, _, input, expected):
        self.lewis.backdoor_set_on_device("helevel", input)
        self.ca.assert_that_pv_is_number("HE:LEVEL", expected, tolerance=0.001)

    @parameterized.expand([
        ("MACROSTATREADENABLED", 0),
        ("MACROSTATREADDISABLED", 1)
    ])
    def test_WHEN_macro_read_set_THEN_macro_stat_scan_rate_toggled_appropriately(self, _, value):
        self.ca.set_pv_value("MACRO:STAT:READ", value)
        self.ca.assert_that_pv_is("MACRO:STAT.DISA", value)

    @skip_if_recsim("Requires emulator backdoor")
    def test_WHEN_macro_set_THEN_macro_readback_correctly(self):
        self.lewis.backdoor_set_and_assert_set("helevel", 50.0)
        self.ca.assert_that_pv_is("MACRO:STAT", "output1.0T,10.0A;voltage1.253;heater0;ramprate1.234;units0;target1.0T,10.0A;persistent0.0T,0.0A;psustatusUnabletocommunicatewithPSU.Pleasecheckinterfaceandmainscables.Initialisationfailed.;pausestatusOFF;tblstatus1.000000fT,10.000000A;readyON;sensA0.0;sensB0.0;setpoint10.0;setpoint20.0;L1pid50.0,20.0,0.0;L2pid45.0,23.0,0.0;L1power0.0;L1range1;L2power0.0;L2range2;L1mout23.0;L2mout33.0;L1ctrl1,1;L2ctrl2,1;zoneON;tcstatusSensorA:Temperaturestable...SensorB:Temperaturestable...;nv0.608696;pressure17.623276,13.79636;valvestatusIdle;helevel453.0;nlevel121.0;hefrequency1;persistmodeOFF;attoangle117.9992;")

    @contextlib.contextmanager
    def _disconnect_device(self):
        self.lewis.backdoor_set_on_device("connected", False)
        try:
            yield
        finally:
            self.lewis.backdoor_set_on_device("connected", True)

    @parameterized.expand(parameterized_list(READ_PVS))
    @skip_if_recsim("Requires emulator backdoor")
    def test_WHEN_device_disconnected_THEN_all_pvs_in_alarm(self, _, pv):
        self.ca.assert_that_pv_alarm_is(pv, self.ca.Alarms.NONE)

        with self._disconnect_device():
            self.ca.assert_that_pv_alarm_is(pv, self.ca.Alarms.INVALID, timeout=30)

        self.ca.assert_that_pv_alarm_is(pv, self.ca.Alarms.NONE, timeout=30)
