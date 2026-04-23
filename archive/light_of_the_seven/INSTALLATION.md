# Installation Guide

Welcome to the Light of the Seven! This guide will help you set up the platform integrations for exploring the computational garden.

## Quick Start

### Basic Installation (CPU only)

```bash
# Clone the repository
git clone https://github.com/irfankabir02/light_of_the_seven.git
cd light_of_the_seven

# With uv (recommended)
uv sync --group dev --group test

# With pip
pip install -e ".[test]"

# Run full test suite (baseline: 163 passed, 0 failed)
uv run pytest tests/ -q --tb=no
# or: pytest tests/ -q --tb=no
```

### Run Tests and Lint

```bash
# Full test suite
uv run pytest tests/ -q --tb=no

# Lint (must pass before push)
uv run ruff check src/ tests/ grid/ tools/
uv run ruff format --check src/ tests/ grid/ tools/
```

## Platform-Specific Installation

### IBM Watson Integration

To enable IBM watsonx.ai integration:

```bash
# Install IBM Watson dependencies
pip install -e ".[ibm]"

# Or manually
pip install ibm-watsonx-ai ibm-watson
```

**Configuration:**
1. Sign up for IBM Cloud: https://cloud.ibm.com/
2. Create a watsonx.ai service instance
3. Get your API key and service URL
4. Use in code:
   ```python
   from platform_integration import IBMWatsonIntegration

   watson = IBMWatsonIntegration(
       api_key="your-api-key",
       url="your-service-url"
   )
   watson.connect()
   ```

### NVIDIA CUDA Integration

To enable NVIDIA CUDA acceleration:

**Prerequisites:**
- NVIDIA GPU with CUDA support
- CUDA Toolkit installed (11.x or 12.x)
- cuDNN (optional, for deep learning)

**Installation:**

```bash
# For CUDA 11.x
pip install cupy-cuda11x

# For CUDA 12.x
pip install cupy-cuda12x

# Verify installation
python -c "import cupy as cp; print(cp.cuda.runtime.getDeviceCount())"
```

**PyTorch with CUDA:**

Visit https://pytorch.org/get-started/locally/ for the exact command for your system.

Example for CUDA 11.8:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**TensorFlow with GPU:**

```bash
pip install tensorflow[and-cuda]
```

### All Optional Dependencies

To install everything (except CUDA, which must match your system):

```bash
pip install -e ".[all]"
```

## Verification

Run the platform integration to verify your setup:

```bash
python platform_integration.py
```

You should see:
- ✓ marks for installed platforms
- ✗ marks for unavailable platforms
- Branch information from the educational garden
- CUDA benchmark (if GPU available)

## Educational Path

The Light of the Seven is structured as an educational garden with four main branches:

1. **Foundations_of_Computation/** - Information theory, Boolean algebra, logic gates
2. **Structure_of_Programming_and_Cognitive_Architecture/** - Mental models, language design
3. **The_AI_Swift_and_Cognitive_Framework/** - Machine learning, personalization
4. **The_Logistic_Field_Hardware_Domain/** - Expert systems, NLP, VLSI design

Each branch contains detailed README files with:
- Conceptual explanations
- Code examples
- Exercises
- References

## Troubleshooting

### CUDA Issues

**Problem:** `ImportError: No module named 'cupy'`
- **Solution:** Install cupy matching your CUDA version

**Problem:** `cupy.cuda.runtime.CUDARuntimeError: cudaErrorNoDevice`
- **Solution:** No NVIDIA GPU detected. The code will fall back to CPU.

**Problem:** CUDA version mismatch
- **Solution:** Check your CUDA version with `nvcc --version` and install matching cupy

### IBM Watson Issues

**Problem:** `ImportError: No module named 'ibm_watsonx_ai'`
- **Solution:** `pip install ibm-watsonx-ai`

**Problem:** Authentication errors
- **Solution:** Verify your API key and service URL are correct

### General Issues

**Problem:** Tests fail with import errors
- **Solution:** Ensure you're in the repository root directory

**Problem:** Permission errors during installation
- **Solution:** Use `pip install --user -e .` or a virtual environment

## Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install
pip install -e ".[all]"
```

## Docker (Alternative)

A Dockerfile is provided for containerized deployment:

```bash
# Build image
docker build -t light-of-seven .

# Run container
docker run -it --gpus all light-of-seven
```

## Next Steps

1. Explore the README.md for repository structure
2. Read `directional_direvative.md` for the conceptual framework
3. Browse the four main branches
4. Run the examples in each subdirectory
5. Contribute your own insights!

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/irfankabir02/light_of_the_seven/issues
- Documentation: See README files in each branch

---

**Note:** This project was created with dedication to provide an educational journey through computational understanding. Each component was carefully crafted to guide learners from theory to implementation.
