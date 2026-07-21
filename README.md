# Jigglypuff Timer

A disciplined, event-driven sleep timer and screen manager built using Python, `uv`, and Pygame. The utility plays an audio lullaby loop paired with a centered GIF animation, mathematically fades out the audio over a customisable window, executes a 10-second total screen blackout, and cleanly restores the system desktop.

## System Architecture

The application operates as a single-process event loop driven by Pygame, operating across two discrete stages:

1. **Active Playback & Decay:** The audio engine plays an asset track on a loop while an animated GIF is center-rendered on a borderless, fullscreen canvas. When the countdown enters the fading window, the audio undergoes a linear volume decay:
   
   $$V(t) = V_{\text{max}} \times \left(1 - \frac{t}{t_{\text{fade}}}\right)$$

2. **Blackout Phase:** Upon timer expiration, audio threads are safely terminated, and the canvas transitions to a pure pitch-black state (`0, 0, 0`) for exactly 10 seconds before restoring cursor visibility and exiting.

## Environment Setup

This project uses `uv` for blazing-fast, deterministic dependency management. 

### Prerequisites
Ensure you have Python 3.11+ and `uv` installed locally.

### Installation
Clone the repository and sync the virtual environment dependencies:

```bash
# Clone the repository
git clone [https://github.com/JHerron1990/jigglypuff-timer.git](https://github.com/JHerron1990/jigglypuff-timer.git)
cd jigglypuff-timer

# Create environment and sync dependencies
uv venv --python 3.12
uv sync
```

## Required Assets
Place your media assets into an assets/ directory at the project root:

- assets/lullaby.mp3 — The loopable background melody.
- assets/jigglypuff.gif — The animated visual asset.

## Repository Structure

```bash
jigglypuff-timer/
├── assets/
│   ├── jigglypuff.gif     # Application graphical asset
│   └── lullaby.mp3        # Loopable audio track
├── tests/
│   ├── __init__.py        # Test package marker
│   └── test_engine.py     # Unit tests for the TimerEngine math
├── audio.py               # Legacy system reference (or audio helper)
├── engine.py              # Pure mathematical volume decay logic
├── LICENSE                # Project distribution rights and permissions
├── main.py                # Main Pygame visual event loop & CLI entrypoint
├── pyproject.toml         # Comprehensive project metadata & lock state
├── system.py              # Native Windows API execution scripts
└── uv.lock                # Deterministic dependency lockfile            
```

## Usage
Run the script natively using uv run. You can configure the timer windows dynamically using CLI flags.

```bash
# Run with default settings (1.0 minute timer, 12-second fade)
uv run main.py

# Execute a fast 15-second test with a 5-second fade window
uv run main.py -d 0.25 -f 0.083
```

## CLI Arguments

| Flag | Long Flag | Type | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `-d` | `--duration` | `float` | `1.0` | Total countdown runtime in minutes. |
| `-f` | `--fade` | `float` | `0.2` | Window duration in minutes over which audio fades out. |
| `-a` | `--audio` | `str` | `assets/lullaby.mp3` | Local file path to the audio track. |
| `-g` | `--gif` | `str` | `assets/jigglypuff.gif` | Local file path to the animated GIF. |

> **Note:** Pressing the `Escape` key at any point during fullscreen execution triggers an immediate, surgical override, cleanly restoring the desktop.

## Development & Quality Control
Code quality and style constraints are rigorously enforced using Ruff.

```bash
# Run style and syntax verification
uv run ruff check

# Automatically resolve fixable lint issues
uv run ruff check --fix
```

## License
This project is licensed under the MIT Licence.