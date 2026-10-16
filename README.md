# Neon Rush

A top-down arcade racing game built with Python and Pygame. Dodge traffic, collect coins, survive as long as possible, and chase a high score.

All visuals are generated with Pygame primitives, so no external image assets are required.

## Features

- Real-time 60 FPS game loop
- Keyboard controls using the Left/Right arrow keys or A/D
- Mouse and touch-friendly steering
- Traffic spawning with rectangle-based collision detection
- Three lives with temporary post-crash invulnerability
- Collectible coins and score bonuses
- Survival scoring
- Increasing speed and traffic frequency
- Pause and restart support
- Windows executable packaging with PyInstaller
- No external image assets required

## Requirements

- Windows 10 or newer
- Python 3.10 or newer
- Pygame

Python can be downloaded from the official website:

<https://www.python.org/downloads/windows/>

During Python installation, enable **Add Python to PATH**.

## Installation

1. Clone or download this repository.
2. Open a Command Prompt in the project directory.
3. Install the required dependencies:

```bat
py -m pip install -r requirements.txt
```

## Run the Game

Start the game with:

```bat
py game.py
```

You can also use the included launcher:

```bat
run_game.bat
```

## Controls

| Action | Keyboard | Mouse / Touch |
|---|---|---|
| Steer left | Left Arrow or A | Click or tap the left half of the window |
| Steer right | Right Arrow or D | Click or tap the right half of the window |
| Pause / resume | P | — |
| Restart after game over | Enter or Space | — |
| Quit | Esc or close the window | — |

## Scoring

Your score increases through:

- Surviving over time
- Collecting coins
- Avoiding traffic
- Reaching higher speeds

The game becomes more difficult as the run continues because traffic frequency and speed increase.

## Build a Windows Executable

To create a standalone Windows executable, run:

```bat
build_exe.bat
```

The script installs the dependencies and creates the executable at:

```text
dist\NeonRush.exe
```

You can also double-click `build_exe.bat` from File Explorer.

The executable is built for the Windows architecture and Python environment used to run the build script. Windows may display a SmartScreen warning because the executable is self-built and unsigned. Only run executables you built yourself or obtained from a trusted source.

## Project Structure

```text
RACING-GAME/
├── game.py
├── requirements.txt
├── build_exe.bat
├── run_game.bat
├── .gitignore
└── README.md
```

## Troubleshooting

### `py` is not recognized

Reinstall Python and enable **Add Python to PATH** during installation. You can also try:

```bat
python --version
```

### Pygame is missing

Install the dependencies again:

```bat
py -m pip install -r requirements.txt
```

### The game window closes immediately

Run the game from Command Prompt so that any error message remains visible:

```bat
py game.py
```

### The executable does not build

Confirm that Python and PyInstaller are installed, then run:

```bat
py -m pip install -r requirements.txt
py -m PyInstaller --version
```

After that, run `build_exe.bat` again.

## Notes

- All artwork is drawn using Pygame primitives.
- No external image or audio assets are required.
- High scores are session-only and reset when the game restarts.
- This project creates a standalone executable, not a professionally signed installer.

## Contributing

Suggestions, bug reports, and improvements are welcome. Please open an issue describing the problem or proposed change before submitting a pull request.
