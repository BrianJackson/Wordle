#!/usr/bin/env python3
"""
Build script for creating Windows executable of Wordle Solver
"""

import os
import subprocess
import sys
from pathlib import Path

def build_executable():
    """Build the Windows executable using PyInstaller"""
    
    print("Building Wordle Solver v1.0.0 executable...")
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Use different separators based on platform for PyInstaller
    separator = ";" if sys.platform == "win32" else ":"
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create a single executable file
        "--windowed",                   # Don't show console window (for GUI)
        "--name=WordleSolver",          # Name of the executable
        f"--add-data=wordle_list.txt{separator}.", # Include the word list file
        "--paths=.",                    # Add current directory to Python path
        "--collect-data=wordfreq",      # Include wordfreq data files
        "main.py"
    ]
    
    # Add icon if it exists
    icon_path = Path("docs/wordle_solver.png")
    if icon_path.exists():
        cmd.insert(-1, f"--icon={icon_path}")
    
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
        "--onefile",                    # Create a single executable file
        "--console",                    # Show console window (for CLI)
        "--name=WordleSolverCLI",       # Name of the executable
        f"--add-data=wordle_list.txt{separator}.", # Include the word list file
        "--paths=.",                    # Add current directory to Python path
        "--collect-data=wordfreq",      # Include wordfreq data files
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

if __name__ == "__main__":
    success = True
    
    # Build CLI executable first (always works)
    if not build_cli_executable():
        success = False
    
    # Build GUI executable (may fail if tkinter not available)
    print("\nAttempting to build GUI executable...")
    try:
        import tkinter
        if not build_executable():
            success = False
    except ImportError:
        print("⚠️  Tkinter not available - skipping GUI executable build")
        print("   GUI executable can be built on systems with tkinter installed")
    
    if success:
        print("\n✅ All available builds completed successfully!")
        print("Executables are available in the 'dist' directory")
        
        # List built executables
        dist_dir = Path("dist")
        if dist_dir.exists():
            print("\nBuilt executables:")
            for exe in dist_dir.glob("*"):
                if exe.is_file():
                    size_mb = exe.stat().st_size / (1024 * 1024)
                    print(f"  - {exe.name} ({size_mb:.1f} MB)")
    else:
        print("\n❌ Some builds failed")
        sys.exit(1)