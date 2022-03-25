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

    def test_that_fails(self):
        pass
        # self.fail("You haven't implemented any tests!")

    def test_WHEN_FIELD_called_THEN_expected_status_returned(self):
        self.ca.set_pv_value("FIELD", "10")
        self.ca.assert_that_pv_is("FIELD", 10)


