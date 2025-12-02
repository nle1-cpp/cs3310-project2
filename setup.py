#!/usr/bin/env python
import subprocess
from pathlib import Path
import venv
import stat
import sys
import os

is_windows = os.name == "nt"

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR =  PROJECT_ROOT / ".venv"
BIN_DIR = VENV_DIR / ("Scripts" if is_windows else "bin")

if not VENV_DIR.is_dir():
    print(f"[setup] Creating virtual environment at: {VENV_DIR}")
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(str(VENV_DIR))
    print("[setup] Virtual environment created.")

# ensure permissions
for f, _, _ in BIN_DIR.walk():
    f.chmod(f.stat().st_mode | stat.S_IEXEC)

activate_this = BIN_DIR / "activate_this.py"
if activate_this.is_file():
    print(f"Activating venv using: {activate_this}")
    # Standard virtualenv pattern
    with activate_this.open("rb") as f:
        code = compile(f.read(), str(activate_this), "exec")
        exec(code, {"__file__": str(activate_this)})


req_file = "requirements.txt"
venv_python = BIN_DIR / ("python.exe" if is_windows else "python")
if not venv_python.is_file():
    raise RuntimeError(f"Could not find venv python at: {venv_python}")

print(f"Installing packages from {req_file} using {venv_python} ...")
cmd = [str(venv_python), "-m", "pip", "install", "-vvr", str(req_file)]
subprocess.check_call(cmd)
print("Requirements installed.")

