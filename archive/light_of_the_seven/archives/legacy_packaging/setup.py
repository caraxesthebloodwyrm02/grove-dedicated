"""
Setup configuration for Light of the Seven.

This educational repository explores the directional derivative of computation,
from foundational theory through cognitive architecture and AI frameworks
to hardware implementation.

Installation:
    pip install -e .

With IBM Watson support:
    pip install -e ".[ibm]"

With NVIDIA CUDA support (requires CUDA toolkit):
    pip install -e ".[cuda]"

With all optional dependencies:
    pip install -e ".[all]"
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="light-of-the-seven",
    version="2.0.0",
    author="GRID Research Team",
    author_email="",
    description="An educational journey through computational understanding from theory to hardware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/irfankabir02/light_of_the_seven",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests", "*.tests", "*.tests.*"]),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
    ],
    extras_require={
        "ibm": [
            "ibm-watsonx-ai>=1.0.0",
            "ibm-watson>=7.0.0",
        ],
        "cuda": [
            # Note: Users should install the appropriate cupy version
            # for their CUDA toolkit manually
            "cupy-cuda11x>=12.0.0; platform_system!='Darwin'",
        ],
        "torch": [
            "torch>=2.0.0",
            "torchvision>=0.15.0",
            "torchaudio>=2.0.0",
        ],
        "tensorflow": [
            "tensorflow>=2.13.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "all": [
            "ibm-watsonx-ai>=1.0.0",
            "ibm-watson>=7.0.0",
            "torch>=2.0.0",
            "torchvision>=0.15.0",
            "torchaudio>=2.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "light-of-seven=light_of_the_seven.integration:print_welcome_message",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.json"],
    },
    project_urls={
        "Documentation": "https://github.com/irfankabir02/light_of_the_seven",
        "Source": "https://github.com/irfankabir02/light_of_the_seven",
        "Tracker": "https://github.com/irfankabir02/light_of_the_seven/issues",
    },
    keywords=[
        "education",
        "computer-science",
        "artificial-intelligence",
        "hardware-design",
        "cognitive-architecture",
        "machine-learning",
        "computational-theory",
        "ibm-watson",
        "nvidia-cuda",
    ],
)
