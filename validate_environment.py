#!/usr/bin/env python3
"""
Environment validation script for ViT5 notebooks.
Checks Python version, dependencies, hardware resources, and model imports.
"""

import sys
import subprocess
import importlib.util
import platform
import shutil
from pathlib import Path

# Try to import psutil for system info, but don't fail if missing
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False


# Required packages for ViT5 notebooks
REQUIRED_PACKAGES = [
    "torch",
    "transformers",
    "datasets",
    "accelerate",
    "sentencepiece",
    "protobuf",
    "rouge_score",
    "seqeval",
    "scikit-learn",
    "huggingface_hub",
    "numpy",
    "pandas",
    "tqdm",
    "matplotlib",
    "seaborn",
    "jupyter",
]

# Critical packages - must be installed for basic functionality
CRITICAL_PACKAGES = [
    "torch",
    "transformers",
    "datasets",
    "accelerate",
    "sentencepiece",
    "numpy",
    "pandas",
]


class CheckResult:
    """Stores result of a single check."""
    def __init__(self, name, status, details="", suggestion=""):
        self.name = name
        self.status = status  # "PASS", "WARN", "FAIL"
        self.details = details
        self.suggestion = suggestion


def check_python_version():
    """Check if Python version is >= 3.9."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        return CheckResult(
            "Python Version",
            "FAIL",
            f"Found: {version_str} (requires >= 3.9)",
            "Install Python 3.9 or higher from python.org"
        )
    return CheckResult(
        "Python Version",
        "PASS",
        f"{version_str}",
        ""
    )


def check_package(package_name):
    """Check if a package is installed and return its version."""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            return CheckResult(
                f"Package: {package_name}",
                "FAIL",
                "Not installed",
                f"pip install {package_name}"
            )

        module = importlib.import_module(package_name)
        version = getattr(module, "__version__", "unknown")
        return CheckResult(
            f"Package: {package_name}",
            "PASS",
            f"v{version}",
            ""
        )
    except Exception as e:
        return CheckResult(
            f"Package: {package_name}",
            "FAIL",
            f"Error: {str(e)[:30]}",
            f"pip install {package_name}"
        )


def check_cuda():
    """Check CUDA availability."""
    if not HAS_TORCH:
        return CheckResult(
            "CUDA Support",
            "FAIL",
            "PyTorch not installed",
            "pip install torch (CPU) or torch+cu118 (GPU)"
        )

    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_name(0) if device_count > 0 else "N/A"
        cuda_version = torch.version.cuda or "unknown"
        return CheckResult(
            "CUDA Support",
            "PASS",
            f"Available - {device_count} GPU(s), CUDA {cuda_version}",
            ""
        )
    else:
        return CheckResult(
            "CUDA Support",
            "WARN",
            "CPU only (no GPU detected)",
            "Install CUDA-enabled PyTorch for faster training"
        )


def check_ram():
    """Check available RAM."""
    if not HAS_PSUTIL:
        return CheckResult(
            "RAM Check",
            "WARN",
            "psutil not installed",
            "pip install psutil"
        )

    ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    if ram_gb < 8:
        return CheckResult(
            "RAM Check",
            "WARN",
            f"{ram_gb:.1f} GB (<8GB recommended)",
            "Consider upgrading RAM for larger models"
        )
    return CheckResult(
        "RAM Check",
        "PASS",
        f"{ram_gb:.1f} GB",
        ""
    )


def check_jupyter():
    """Check if Jupyter can be launched."""
    jupyter_path = shutil.which("jupyter")
    if jupyter_path:
        try:
            result = subprocess.run(
                ["jupyter", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            if result.returncode == 0:
                versions = result.stdout.strip().split('\n')
                return CheckResult(
                    "Jupyter Installation",
                    "PASS",
                    f"v{versions[0] if versions else 'unknown'}",
                    ""
                )
        except Exception as e:
            pass

    return CheckResult(
        "Jupyter Installation",
        "WARN",
        "jupyter command not found",
        "pip install jupyter or use 'python -m notebook'"
    )


def check_disk_space():
    """Check disk space in current directory."""
    if not HAS_PSUTIL:
        return CheckResult(
            "Disk Space",
            "WARN",
            "psutil not installed",
            "pip install psutil"
        )

    try:
        current_dir = str(Path.cwd())
        usage = psutil.disk_usage(current_dir)
        free_gb = usage.free / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)

        if free_gb < 10:
            return CheckResult(
                "Disk Space",
                "WARN",
                f"Free: {free_gb:.1f}GB / {total_gb:.1f}GB",
                "Free up space for models (~10GB+ needed)"
            )
        return CheckResult(
            "Disk Space",
            "PASS",
            f"Free: {free_gb:.1f}GB / {total_gb:.1f}GB",
            ""
        )
    except Exception as e:
        return CheckResult(
            "Disk Space",
            "WARN",
            f"Error: {str(e)[:30]}",
            ""
        )


def test_model_imports():
    """Test importing model families and tokenizers."""
    results = []

    # Test ViT5/ViT5-like models (T5-based vision-language models)
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        # ViT5 uses T5 tokenizer (t5-base or google/t5-v1_1-base)
        # Try a few known model IDs
        tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-small")
        results.append(CheckResult(
            "ViT5/T5 Import Test",
            "PASS",
            "T5 tokenizer loaded (ViT5-compatible)",
            ""
        ))
    except Exception as e:
        results.append(CheckResult(
            "ViT5/T5 Import Test",
            "FAIL",
            f"Import failed: {str(e)[:50]}",
            "Check internet connection and transformers version"
        ))

    # Test PhoBERT - just tokenizer to avoid loading warnings
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
        results.append(CheckResult(
            "PhoBERT Tokenizer Test",
            "PASS",
            "PhoBERT tokenizer loaded",
            ""
        ))
    except Exception as e:
        results.append(CheckResult(
            "PhoBERT Tokenizer Test",
            "FAIL",
            f"Import failed: {str(e)[:50]}",
            "Ensure vinai/phobert-base is accessible"
        ))

    return results


def get_status_symbol(status):
    """Get text symbol for status (Windows-safe)."""
    symbols = {
        "PASS": "[OK]",
        "WARN": "[WARN]",
        "FAIL": "[FAIL]"
    }
    return symbols.get(status, "?")


def print_table(results, title):
    """Print results in a formatted table."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

    # Header
    print(f"{'Check':<38} {'Status':<10} {'Details':<32}")
    print("-" * 80)

    for result in results:
        print(f"{result.name:<38} {get_status_symbol(result.status):<10} {result.details:<32}")

    print("=" * 80)


def print_suggestions(results):
    """Print installation suggestions for failed/warning checks."""
    suggestions = [(r.name, r.suggestion) for r in results if r.suggestion]
    if suggestions:
        print("\n" + "-" * 80)
        print("Suggestions:")
        print("-" * 80)
        for name, suggestion in suggestions:
            if suggestion:
                print(f"  [{name}]")
                print(f"    > {suggestion}")


def main():
    """Run all checks and generate report."""
    # Print header with safe encoding
    print("\n" + "=" * 80)
    print(f"{'ViT5 Environment Validation':^80}".encode('ascii', errors='replace').decode())
    print(f"{'Python: ' + sys.version.split()[0]:<40} {'Platform: ' + platform.system():>40}")
    print("=" * 80)

    all_results = []

    # 1. Python version check
    print("\n[1/8] Checking Python version...")
    all_results.append(check_python_version())

    # 2. Package checks
    print("[2/8] Checking required packages...")
    for i, pkg in enumerate(REQUIRED_PACKAGES, 1):
        all_results.append(check_package(pkg))

    # 3. CUDA check
    print("[3/8] Checking hardware...")
    all_results.append(check_cuda())

    # 4. RAM check
    all_results.append(check_ram())

    # 5. Jupyter check
    print("[4/8] Checking Jupyter...")
    all_results.append(check_jupyter())

    # 6. Disk space check
    print("[5/8] Checking disk space...")
    all_results.append(check_disk_space())

    # 7. Model import tests
    print("[6/8] Testing model imports...")
    all_results.extend(test_model_imports())

    # 8. Summary
    print_table(all_results, "Validation Results")

    # Summary statistics
    passed = sum(1 for r in all_results if r.status == "PASS")
    warnings = sum(1 for r in all_results if r.status == "WARN")
    failed = sum(1 for r in all_results if r.status == "FAIL")

    print(f"\nSummary:")
    print(f"  Total checks: {len(all_results)}")
    print(f"  Passed: {passed}")
    print(f"  Warnings: {warnings}")
    print(f"  Failed: {failed}")

    # Check for critical failures - only CRITICAL packages and Python version
    critical_failures = any(
        r.status == "FAIL" and r.name.replace("Package: ", "") in CRITICAL_PACKAGES
        for r in all_results
    )
    critical_failures |= any(r.name == "Python Version" and r.status == "FAIL" for r in all_results)

    print("\n" + "-" * 80)
    if critical_failures:
        print("CRITICAL: Environment not ready - missing required core packages or wrong Python.")
        print_suggestions(all_results)
        print("\nRun the suggested pip install commands to resolve issues.")
        print("After installation, re-run this script to verify.")
        print("")
        sys.exit(1)
    elif failed > 0 or warnings > 0:
        print("WARNING: Environment mostly ready but has warnings/failures.")
        print("Some optional features may not work. Review suggestions above.")
        print("")
        sys.exit(0)
    else:
        print("SUCCESS: Environment is properly configured for ViT5 notebooks!")
        print("\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
