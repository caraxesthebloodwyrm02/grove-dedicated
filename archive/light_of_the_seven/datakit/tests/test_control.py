import unittest
from core.control import ControlPlane, Transistor

class TestTransistor(unittest.TestCase):
    def test_toggle(self):
        t = Transistor(name="TEST_SWITCH", state=False)
        self.assertFalse(t.state)
        t.toggle()
        self.assertTrue(t.state)
        t.toggle()
        self.assertFalse(t.state)

class TestControlPlane(unittest.TestCase):
    def setUp(self):
        self.cp = ControlPlane()

    def test_default_flags(self):
        """Ensure standard flags are present."""
        self.assertIsNotNone(self.cp.get("ENABLE_EXPERIMENTAL"))
        self.assertFalse(self.cp.is_enabled("ENABLE_EXPERIMENTAL"))
        
        self.assertIsNotNone(self.cp.get("MODE_LOCOMOTIVE"))

    def test_dynamic_registration(self):
        """Test registering a new transistor."""
        t_new = Transistor(name="TEST_FEATURE", state=True)
        self.cp.register(t_new)
        
        self.assertTrue(self.cp.is_enabled("TEST_FEATURE"))
        
        # Test overwriting warning (logic check, not log check)
        t_overwrite = Transistor(name="TEST_FEATURE", state=False)
        self.cp.register(t_overwrite)
        self.assertFalse(self.cp.is_enabled("TEST_FEATURE"))

    def test_set_state(self):
        self.cp.set_state("ENABLE_EXPERIMENTAL", True)
        self.assertTrue(self.cp.is_enabled("ENABLE_EXPERIMENTAL"))
        
        # Setting unknown flag should not crash
        self.cp.set_state("UNKNOWN_FLAG", True)

if __name__ == "__main__":
    unittest.main()
