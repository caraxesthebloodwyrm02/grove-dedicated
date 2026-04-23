"""
Test suite for Light of the Seven platform integration.

This test suite validates the integration with IBM Watson and NVIDIA CUDA,
ensuring the educational garden's platform bridges work correctly.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path for package imports (go up from tests/ to repo root, then into src/)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from light_of_the_seven.integration import (
    CUDA_AVAILABLE,
    IBM_AVAILABLE,
    IBMWatsonIntegration,
    LightOfTheSevenIntegration,
    NVIDIACUDAIntegration,
    check_environment,
)


class TestLightOfTheSevenIntegration(unittest.TestCase):
    """Test the main integration class."""

    def setUp(self):
        """Set up test fixtures."""
        self.integration = LightOfTheSevenIntegration()

    def test_initialization(self):
        """Test integration initializes correctly."""
        self.assertIsNotNone(self.integration.base_path)
        self.assertIsInstance(self.integration.branches, dict)

    def test_branch_discovery(self):
        """Test that branches are discovered correctly."""
        expected_branches = ["foundations", "cognitive_architecture", "ai_framework", "hardware"]
        for branch in expected_branches:
            if branch in self.integration.branches:
                self.assertIsInstance(self.integration.branches[branch], Path)

    def test_get_branch_info(self):
        """Test branch information retrieval."""
        info = self.integration.get_branch_info()
        self.assertIsInstance(info, dict)

        for _branch_name, branch_info in info.items():
            self.assertIn("path", branch_info)
            self.assertIn("subdirectories", branch_info)
            self.assertIn("readme_exists", branch_info)
            self.assertIsInstance(branch_info["subdirectories"], list)

    def test_demonstrate_directional_derivative(self):
        """Test directional derivative demonstration."""
        result = self.integration.demonstrate_directional_derivative()
        self.assertIsInstance(result, str)
        self.assertIn("Foundations_of_Computation", result)
        self.assertIn("Cognitive_Architecture", result)
        self.assertIn("AI_Framework", result)
        self.assertIn("Hardware_Domain", result)


class TestIBMWatsonIntegration(unittest.TestCase):
    """Test IBM Watson integration."""

    def test_initialization_without_credentials(self):
        """Test initialization without credentials."""
        if not IBM_AVAILABLE:
            self.skipTest("IBM Watson SDK not available")

        integration = IBMWatsonIntegration()
        self.assertIsNone(integration.client)

    def test_initialization_with_credentials(self):
        """Test initialization with credentials."""
        if not IBM_AVAILABLE:
            self.skipTest("IBM Watson SDK not available")

        integration = IBMWatsonIntegration(api_key="test_key", url="https://test.url")
        self.assertEqual(integration.api_key, "test_key")
        self.assertEqual(integration.url, "https://test.url")

    def test_connect_without_credentials(self):
        """Test connection fails without credentials."""
        if not IBM_AVAILABLE:
            self.skipTest("IBM Watson SDK not available")

        integration = IBMWatsonIntegration()
        result = integration.connect()
        self.assertFalse(result)

    def test_list_foundation_models_no_client(self):
        """Test listing models without client."""
        if not IBM_AVAILABLE:
            self.skipTest("IBM Watson SDK not available")

        integration = IBMWatsonIntegration()
        models = integration.list_foundation_models()
        self.assertEqual(models, [])


class TestNVIDIACUDAIntegration(unittest.TestCase):
    """Test NVIDIA CUDA integration."""

    def setUp(self):
        """Set up test fixtures."""
        self.integration = NVIDIACUDAIntegration()

    def test_initialization(self):
        """Test CUDA integration initializes correctly."""
        self.assertIsInstance(self.integration.cuda_available, bool)
        self.assertIsInstance(self.integration.torch_cuda_available, bool)

    def test_get_device_info(self):
        """Test device information retrieval."""
        info = self.integration.get_device_info()
        self.assertIsInstance(info, dict)
        self.assertIn("cupy_available", info)
        self.assertIn("torch_available", info)
        self.assertIn("torch_cuda_available", info)

    def test_demonstrate_saxpy_cpu_fallback(self):
        """Test SAXPY demonstration with CPU fallback."""
        result = self.integration.demonstrate_saxpy(n=1000)

        self.assertIsInstance(result, dict)
        self.assertIn("device", result)
        self.assertIn("time_seconds", result)
        self.assertIn("vector_size", result)
        self.assertIn("result_sample", result)

        self.assertEqual(result["vector_size"], 1000)
        self.assertIsInstance(result["time_seconds"], float)
        self.assertGreater(result["time_seconds"], 0)

    @unittest.skipUnless(CUDA_AVAILABLE, "CUDA not available")
    def test_demonstrate_saxpy_cuda(self):
        """Test SAXPY demonstration with CUDA."""
        result = self.integration.demonstrate_saxpy(n=100000)

        self.assertEqual(result["device"], "cuda")
        self.assertEqual(result["vector_size"], 100000)
        self.assertIsInstance(result["result_sample"], list)
        self.assertEqual(len(result["result_sample"]), 5)


class TestEnvironmentCheck(unittest.TestCase):
    """Test environment checking functionality."""

    def test_check_environment(self):
        """Test environment check returns correct structure."""
        env = check_environment()

        self.assertIsInstance(env, dict)
        self.assertIn("ibm_watson", env)
        self.assertIn("nvidia_cuda", env)
        self.assertIn("pytorch", env)
        self.assertIn("pytorch_cuda", env)

        for _key, value in env.items():
            self.assertIsInstance(value, bool)


class TestIntegrationScenarios(unittest.TestCase):
    """Test real-world integration scenarios."""

    def test_educational_path_walkthrough(self):
        """Test walking through the educational path."""
        integration = LightOfTheSevenIntegration()

        # Verify we can access branch information
        branch_info = integration.get_branch_info()
        self.assertGreater(len(branch_info), 0)

        # Verify directional derivative concept
        derivative = integration.demonstrate_directional_derivative()
        self.assertIn("1.", derivative)
        self.assertIn("2.", derivative)
        self.assertIn("3.", derivative)
        self.assertIn("4.", derivative)

    def test_platform_availability_reporting(self):
        """Test platform availability reporting."""
        env = check_environment()

        # At minimum, numpy should work (CPU fallback)
        # Other platforms are optional
        self.assertIsInstance(env["ibm_watson"], bool)
        self.assertIsInstance(env["nvidia_cuda"], bool)

    def test_cuda_integration_graceful_degradation(self):
        """Test CUDA integration degrades gracefully without GPU."""
        cuda_integration = NVIDIACUDAIntegration()

        # Should work even without CUDA
        device_info = cuda_integration.get_device_info()
        self.assertIsInstance(device_info, dict)

        # SAXPY should fall back to CPU
        saxpy_result = cuda_integration.demonstrate_saxpy(n=100)
        self.assertIn("device", saxpy_result)
        self.assertIn(saxpy_result["device"], ["cpu", "cuda"])


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("Light of the Seven - Platform Integration Test Suite")
    print("=" * 70)
    print("\nThis test suite validates the integration bridges between")
    print("the educational garden and IBM Watson / NVIDIA CUDA platforms.")
    print("\nNote: Some tests may be skipped if optional dependencies")
    print("(IBM Watson SDK, CUDA) are not installed.\n")
    print("=" * 70)
    print()

    success = run_tests()
    sys.exit(0 if success else 1)
