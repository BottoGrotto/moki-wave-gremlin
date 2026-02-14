# Wave Gremlin

A tiny Pygame-based wave function visualizer that renders a scrolling sine wave and lets you tweak the amplitude, frequency, and scroll speed on the fly.

## Features

- Real-time rendering of a sine wave
- Adjustable amplitude, frequency, and scroll speed via keyboard controls
- Lightweight codebase (single Python file) and zero external assets

## Requirements

- Python 3.10+
- [Pygame](https://www.pygame.org/) 2.5+

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python wave_visualizer.py
```

### Controls

| Key | Action |
| --- | --- |
| ↑ / ↓ | Increase / decrease amplitude |
| ← / → | Decrease / increase frequency |
| A / Z | Decrease / increase scroll speed |
| R | Reset parameters to defaults |
| Esc / Q | Quit |

Have fun watching the digital ripple! 😛
