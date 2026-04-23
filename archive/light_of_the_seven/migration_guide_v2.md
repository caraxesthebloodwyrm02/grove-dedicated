# 🚀 Migration Guide: v1.x → v2.0.0

This guide helps you upgrade your code from Light of the Seven v1.x to v2.0.0.

---

## 📋 Overview of Changes

| Category | v1.x | v2.0.0 |
|----------|------|--------|
| **Import Path** | `from platform_integration import ...` | `from light_of_the_seven import ...` |
| **Version Access** | Not available | `from light_of_the_seven import __version__` |
| **Package Structure** | Flat files | Proper Python package |
| **Type Hints** | Partial | Full coverage on public API |

---

## ⚠️ Breaking Changes

### 1. Import Path Changes

**Before (v1.x):**
```python
from platform_integration import LightOfTheSevenIntegration
from platform_integration import check_environment
```

**After (v2.0.0):**
```python
from light_of_the_seven import LightOfTheSevenIntegration
from light_of_the_seven import check_environment
```

### 2. Version Checking

**Before (v1.x):**
```python
# No programmatic version access
```

**After (v2.0.0):**
```python
from light_of_the_seven import __version__, VersionManager

print(__version__)  # "2.0.0"

vm = VersionManager()
print(vm.major)  # 2
print(vm.is_compatible("2.1.0"))  # True
```

### 3. Entry Point Changes

**Before (v1.x):**
```bash
python platform_integration.py
```

**After (v2.0.0):**
```bash
light-of-seven          # CLI command
python -m light_of_the_seven  # Module execution
```

---

## 🔧 Step-by-Step Migration

### Step 1: Update Your Imports

Replace all direct file imports with package imports:

```python
# Find and replace in your codebase:
# OLD                                    → NEW
# from platform_integration import X     → from light_of_the_seven import X
# from structured_geometry import X      → from light_of_the_seven.geometry import X
# from version_structure import X        → from light_of_the_seven.models import X
```

### Step 2: Update Version Checks

If you have any version-dependent logic:

```python
from light_of_the_seven import VersionManager

vm = VersionManager()
if vm.major >= 2:
    # Use v2.0.0 features
    pass
```

### Step 3: Update Your Dependencies

**requirements.txt:**
```txt
light-of-the-seven>=2.0.0,<3.0.0
```

**pyproject.toml:**
```toml
[project]
dependencies = [
    "light-of-the-seven>=2.0.0,<3.0.0",
]
```

---

## 🆕 New Features in v2.0.0

### VersionManager Class

```python
from light_of_the_seven import VersionManager

vm = VersionManager()

# Get version info
print(vm.current_version)     # "2.0.0"
print(vm.version_info)        # VersionInfo(major=2, minor=0, patch=0)

# Check compatibility
vm.is_compatible("2.0.5")     # True
vm.is_compatible("1.5.0")     # False

# Compare versions
vm.compare("2.1.0")           # -1 (current < other)
vm.compare("2.0.0")           # 0  (equal)
vm.compare("1.9.0")           # 1  (current > other)

# Export metadata
vm.to_dict()                  # Full version dictionary
```

### Type Hints

All public functions now have complete type annotations:

```python
def check_environment() -> Dict[str, bool]: ...
def get_version() -> str: ...
def get_version_info() -> VersionInfo: ...
```

---

## 🐛 Troubleshooting

### ImportError: No module named 'light_of_the_seven'

**Cause:** Package not installed or using old installation.

**Fix:**
```bash
pip uninstall light-of-the-seven
pip install light-of-the-seven>=2.0.0
```

### AttributeError: module has no attribute '__version__'

**Cause:** Using v1.x package.

**Fix:** Upgrade to v2.0.0 as shown above.

---

## 📞 Getting Help

- **Issues:** [GitHub Issues](https://github.com/irfankabir02/light_of_the_seven/issues)
- **Documentation:** See `README.md` and `INSTALLATION.md`

---

*Last updated: 2025-12-20 for v2.0.0 release*
