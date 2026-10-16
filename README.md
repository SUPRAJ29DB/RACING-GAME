# Neon Rush — Hard Mode

A top-down arcade racing game built with Python and Pygame. The visuals are generated in code; no external image assets are needed.

## Features

- Real-time 60 FPS game loop
- Keyboard controls: **Left/Right arrows** or **A/D**
- Mouse/touch-friendly steering: click/tap the left or right half of the game window
- Traffic spawning and rectangle-based collision detection
- Three lives, temporary post-crash invulnerability, and game-over screen
- Collectible coins, score bonuses, and survival scoring
- Increasing speed and traffic frequency as the run continues
- Pause with **P**, restart with **Enter** or **Space**
- Windows EXE packaging script using PyInstaller

## Run from source

1. Install Python 3.10 or newer from https://www.python.org/downloads/windows/
2. During installation, enable **Add Python to PATH**.
3. Extract this project ZIP.
4. Open the extracted folder in File Explorer.
5. Click the address bar, type `cmd`, and press Enter.
6. Run:

```bat
py -m pip install -r requirements.txt
py game.py
```

## Build a Windows EXE

Run `build_exe.bat` by double-clicking it, or execute it from Command Prompt. It installs the dependencies and builds a standalone executable in `dist\NeonRush.exe`.

```bat
build_exe.bat
```

When it finishes, launch:

```text
dist\NeonRush.exe
```

The EXE is built for the Windows architecture and Python environment on which you run the build script. Windows may show a SmartScreen warning for an unsigned, self-built executable; only run builds you created or trust.

## Controls

| Action | Control |
|---|---|
| Steer left | Left arrow / A / click or tap left half |
| Steer right | Right arrow / D / click or tap right half |
| Pause / resume | P |
| Restart after game over | Enter / Space |
| Quit | Esc or close window |

## Project structure

```text
neon_rush_windows/
├── game.py
├── requirements.txt
├── build_exe.bat
├── run_game.bat
├── .gitignore
└── README.md
```

## Notes

- All art is drawn using Pygame primitives; no assets need to be downloaded.
- High scores are session-only in this version and reset when the game restarts.
- This is a small arcade project, not a professionally signed installer.
