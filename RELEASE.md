# Wordle Solver v1.0.0 Release

## 🎉 What's New in v1.0.0

This is the first official release of the Wordle Solver! This version includes:

- ✅ Complete GUI application with intuitive interface
- ✅ Command-line interface for terminal users
- ✅ Smart entropy-based suggestion engine
- ✅ Word frequency optimization
- ✅ Hard mode constraint enforcement
- ✅ Comprehensive test suite
- ✅ **Windows executable files** for easy distribution

## 📦 Download Options

### For Windows Users (Recommended)
Download the pre-built executables from the release:

- **WordleSolver.exe** - GUI version with visual interface
- **WordleSolverCLI.exe** - Command-line version for terminal use

No Python installation required! Just download and run.

### For Developers/Python Users
Clone the repository and install dependencies:

```bash
git clone https://github.com/BrianJackson/Wordle.git
cd Wordle
pip install -r requirements.txt
```

## 🚀 Quick Start

### Windows Executable
1. Download `WordleSolver.exe` or `WordleSolverCLI.exe`
2. Double-click to run (Windows may show a security warning - click "More info" → "Run anyway")
3. For CLI: Open Command Prompt, navigate to download folder, run:
   ```cmd
   WordleSolverCLI.exe --guess crane --feedback BYGBY
   ```

### GUI Application
```bash
python main.py
```

### Command Line
```bash
python cli.py --guess crane --feedback BYGBY
```

## 🎯 How to Use

### GUI Interface
1. Enter your guess in the letter boxes
2. Click the feedback buttons to set colors:
   - ⬜ Gray = letter not in word
   - 🟨 Yellow = letter in word, wrong position  
   - 🟩 Green = correct letter and position
3. Click "Apply Feedback" to get suggestions
4. Use "Auto Suggest" for the best next guess

### CLI Interface
```bash
WordleSolverCLI --guess <your-guess> --feedback <feedback-string>
```

Feedback format:
- `B` = Gray (not in word)
- `Y` = Yellow (wrong position)
- `G` = Green (correct position)

Example:
```bash
WordleSolverCLI --guess crane --feedback BYGBY
```

## 🔧 Building Executables

To build your own executables:

```bash
python build_executable.py
```

Requirements:
- Python 3.8+
- PyInstaller
- All project dependencies

## 📊 Features

- **Smart Suggestions**: Uses entropy × frequency scoring for optimal guesses
- **Hard Mode Enforcement**: Ensures logical consistency across guesses
- **Word List**: 12,000+ valid 5-letter words
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No Internet Required**: All processing done locally

## 🐛 Known Issues

- First run may be slow due to wordfreq library initialization
- Windows Defender may flag executables as potentially unwanted (false positive)
- GUI requires tkinter (included with most Python installations)

## 📝 Version History

### v1.0.0 (2024-08-28)
- Initial release
- GUI and CLI interfaces
- Windows executable support
- Comprehensive test suite
- Documentation improvements

---

## 🛠️ For Developers

### Running Tests
```bash
python -m unittest discover tests
```

### Project Structure
```
Wordle/
├── main.py              # GUI application
├── cli.py               # Command-line interface  
├── wordlist.py          # Word loading and frequency
├── feedback.py          # Feedback logic and constraints
├── solver.py            # Entropy calculation and ranking
├── version.py           # Version information
├── build_executable.py  # Build script for executables
├── wordle_list.txt      # Word database
├── requirements.txt     # Python dependencies
└── tests/               # Unit tests
```

### Dependencies
- `wordfreq` - Word frequency data
- `numpy` - Numerical operations
- `pyinstaller` - Executable building
- `tkinter` - GUI framework (usually included with Python)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. See the repository for license details.

---

**Happy Wordling! 🎯**