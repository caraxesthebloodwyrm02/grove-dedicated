import os
import pathlib
import sys
from typing import Dict

# --------------------------------------------------------------------------- #
#  Configuration – adjust this if you want to target a different base folder
# --------------------------------------------------------------------------- #
BASE_DIR = pathlib.Path(__file__).parent.resolve()  # where scripts live
GRID_ROOT = BASE_DIR / "grid"  # this is the root you listed

# --------------------------------------------------------------------------- #
#  Helper – create a directory + __init__.py
# --------------------------------------------------------------------------- #
def mkdir(path: pathlib.Path) -> None:
    """Create *path* and all parents, then drop a blank __init__.py."""
    path.mkdir(parents=True, exist_ok=True)
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")  # empty file
        print(f"Created package init: {init_file}")


# --------------------------------------------------------------------------- #
#  Helper – write a module file with a small docstring
# --------------------------------------------------------------------------- #
def write_module(path: pathlib.Path, module_name: str) -> None:
    """Create a .py file with a short unique docstring."""
    module_file = path / f"{module_name}.py"
    content = f'"""Module {module_name} under {path.name}. Added by create_grid_structure.py."""\n\npass\n'
    module_file.write_text(content)
    print(f"Created module: {module_file}")


# --------------------------------------------------------------------------- #
#  Definition of the skeleton
# --------------------------------------------------------------------------- #
PACKAGE_STRUCTURE: Dict[str, Dict[str, str]] = {
    "essence": {
        "core_state.py": "core_state",
        "quantum_state.py": "quantum_state",
        "state_transform.py": "state_transform",
    },
    "patterns": {
        "recognition.py": "recognition",
        "emergence.py": "emergence",
        "resonance.py": "resonance",
    },
    "awareness": {
        "context.py": "context",
        "observer.py": "observer",
        "field.py": "field",
    },
    "evolution": {
        "version.py": "version",
        "transform.py": "transform",
        "coherence.py": "coherence",
    },
    "interfaces": {
        "sensory.py": "sensory",
        "bridge.py": "bridge",
    },
}

# --------------------------------------------------------------------------- #
#  Main logic
# --------------------------------------------------------------------------- #
def main() -> None:
    print(f"Creating grid package at {GRID_ROOT}")

    # 1️⃣ Create the top‑level 'grid' directory
    GRID_ROOT.mkdir(parents=True, exist_ok=True)

    # 2️⃣ Iterate over the top‑level packages
    for pkg_name, modules in PACKAGE_STRUCTURE.items():
        pkg_path = GRID_ROOT / pkg_name
        mkdir(pkg_path)  # package init

        # write each module inside the package
        for filename, module_name in modules.items():
            write_module(pkg_path, module_name)

    print("\nAll done – directory tree:")
    for root, dirs, files in os.walk(GRID_ROOT):
        level = root.replace(str(GRID_ROOT), "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in sorted(files):
            print(f"{subindent}{f}")

if __name__ == "__main__":
    # Allow optional target directory on command line
    if len(sys.argv) > 1:
        BASE_DIR = pathlib.Path(sys.argv[1]).resolve()
        GRID_ROOT = BASE_DIR / "grid"
    main()
