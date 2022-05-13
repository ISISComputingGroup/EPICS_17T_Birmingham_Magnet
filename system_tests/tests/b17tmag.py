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
        # self.pressure_value = 1000
        # self.set_loop_status = 1
        # self.default_initial_value = 0
        # self.default_id_prefix = 1111
        # self.low_pressure = 50
        # self.lewis, self.ioc = get_running_lewis_and_ioc(DEVICE_A_PREFIX, DEVICE_A_PREFIX)
        # self.ca = ChannelAccess(default_timeout=20, default_wait_time=0.0, device_prefix=DEVICE_A_PREFIX)
        # self.lewis.backdoor_run_function_on_device("re_initialise")
        self.lewis, self.ioc = get_running_lewis_and_ioc("b17Tmag", DEVICE_PREFIX)
        self.ca = ChannelAccess(default_timeout=20, default_wait_time=0.0, device_prefix=DEVICE_PREFIX)
        self.lewis.backdoor_run_function_on_device("re_initialise")

    # def test_that_fails(self):
    #     pass
        # self.fail("You haven't implemented any tests!")

    # def test_WHEN_FIELD_called_THEN_expected_status_returned(self):
    #     self.ca.set_pv_value("FIELD", "10")
    #     self.ca.assert_that_pv_is("FIELD", 10)

    # # Test get heater
    # def test_WHEN_get_heater_called_THEN_expected_status_returned(self):
    #     self.ca.assert_that_pv_is("HEATER", 0)

    # # test error occurs when sending value higher than 3
    # def test_WHEN_set_heater_to_4_THEN_error_occurs(self):
    #     self._device.heater = 4
    #     self.ca.assert_fails_to_set_pv("HEATER", 4)

    # # Test persist error called with correct readback value
    # def test_WHEN_get_persist_called_THEN_expected_status_returned(self):
    #     self.ca.assert_that_pv_is("PERSIST", "10fT,20A")

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
        self.ca.set_pv_value("HE:LEVEL_RAW", input)
        self.ca.assert_that_pv_is("HE:LEVEL.VAL", expected)


    @parameterized.expand([
        ("MACROSTATREADENABLED", 0),
        ("MACROSTATREADDISABLED", 1)
    ])
    def test_WHEN_macro_read_set_THEN_macro_stat_scan_rate_toggled_appropriately(self, _, value):
        self.ca.set_pv_value("MACRO:STAT:READ", value)
        self.ca.assert_that_pv_is("MACRO:STAT.DISA", value)

    