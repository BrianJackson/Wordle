#!/usr/bin/env python3
"""
Build script for creating Windows executable of Wordle Solver
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def build_executable():
    """Build the Windows executable using PyInstaller"""
    
    print("Building Wordle Solver v1.0.0 executable...")
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Use different separators based on platform for PyInstaller
    separator = ";" if sys.platform == "win32" else ":"
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=WordleSolver",
        f"--add-data=wordle_list.txt{separator}.",
        "--paths=.",
        "--collect-data=wordfreq",
        "--hidden-import=numpy",
        "--hidden-import=wordfreq",
    ]

    # Icon handling (Windows requires .ico)
    ico_path = Path("docs/solver_icon.ico")
    png_path = Path("docs/wordle_solver.png")
    if ico_path.exists():
        cmd.append(f"--icon={ico_path}")
    else:
        if png_path.exists():
            print("[warn] PNG icon found but .ico required for Windows. Skipping icon. (Convert to docs/wordle_solver.ico to include.)")
        else:
            print("[info] No icon file found; proceeding without custom icon.")

    cmd.append("main.py")
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("GUI Build successful!")
        exe_name = "WordleSolver.exe" if sys.platform == "win32" else "WordleSolver"
        print(f"GUI Executable created in: {project_dir / 'dist' / exe_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"GUI Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def build_cli_executable():
    """Build the CLI executable"""
    
    print("Building Wordle Solver CLI v1.0.0 executable...")
    
    # Use different separators based on platform for PyInstaller
    separator = ";" if sys.platform == "win32" else ":"
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=WordleSolverCLI",
        f"--add-data=wordle_list.txt{separator}.",
        "--paths=.",
        "--collect-data=wordfreq",
        "--hidden-import=numpy",
        "--hidden-import=wordfreq",
        "cli.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("CLI Build successful!")
        exe_name = "WordleSolverCLI.exe" if sys.platform == "win32" else "WordleSolverCLI"
        print(f"CLI Executable created in: {Path.cwd() / 'dist' / exe_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"CLI Build failed: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def ensure_pyinstaller():
    """Verify pyinstaller is installed; if not, provide guidance."""
    if shutil.which("pyinstaller"):
        return True
    print("[error] PyInstaller not found in PATH. Install with: pip install pyinstaller")
    return False

def main():
    if not ensure_pyinstaller():
        sys.exit(1)

    success = True

    if not build_cli_executable():
        success = False

    print("\nAttempting to build GUI executable...")
    try:
        import tkinter  # noqa: F401
        if not build_executable():
            success = False
    except ImportError:
        print("⚠️  Tkinter not available - skipping GUI executable build")
        print("   Install a Python distribution with tkinter to build the GUI.")

    if success:
        print("\n✅ All available builds completed successfully!")
        dist_dir = Path("dist")
        if dist_dir.exists():
            print("\nBuilt executables:")
            for exe in dist_dir.glob("*"):
                if exe.is_file():
                    size_mb = exe.stat().st_size / (1024 * 1024)
                    print(f"  - {exe.name} ({size_mb:.1f} MB)")
    else:
        print("\n❌ Some builds failed. See messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()