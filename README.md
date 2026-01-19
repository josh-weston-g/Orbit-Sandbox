# Orbit-Sandbox

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&logoColor=ffffff)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

A physics-accurate Newtonian orbital mechanics simulator built from first principles. Watch planets orbit stars, create elliptical trajectories, or launch escape maneuvers - all emerging naturally from Newton's laws and numerical integration.

> **⚠️ Work in Progress:** This project is actively under development. Features are being added incrementally, and the codebase is evolving. Expect breaking changes and incomplete functionality.

## What it does

Orbit-Sandbox simulates gravitational interactions between celestial bodies using real Newtonian physics. You set initial conditions (position, velocity, mass), and the simulator evolves the system forward in time using Velocity Verlet integration.

The simulator can run in two modes:
- **Console mode:** Outputs orbital data to the terminal with periodic position/velocity updates
- **Visualization mode:** Interactive Pygame window with real-time rendering, zoom controls, and orbital trails

Whether you want to explore orbital mechanics, experiment with different initial conditions, or just watch a planet spiral into a star, Orbit-Sandbox provides an honest physics engine that behaves like the real universe.

## Current Features

- 🪐 **Three orbital scenarios:**
  - Circular orbit - stable, constant radius
  - Elliptical orbit - oscillates between periapsis and apoapsis
  - Escape trajectory - hyperbolic path to infinity
- ⚙️ **Physics simulation:**
  - Newtonian gravity (inverse square law)
  - Velocity Verlet integration (2nd order accuracy)
  - Excellent energy conservation
  - Conserves angular momentum
- 🎮 **Interactive visualization:**
  - Real-time Pygame rendering
  - Dynamic window resolution (auto-detection or fixed sizes)
  - Mouse wheel zoom with limits
  - Camera panning with WASD keys or click-and-drag
  - Toggleable velocity vector display
  - Toggleable acceleration vector display
  - Toggleable grid overlay
  - Orbital trail rendering
  - Pause/resume with spacebar
  - Rewind simulation
  - Reset simulation with R key
  - ESC to return to menu
- 🖥️ **Console mode:**
  - CLI scenario selection
  - Periodic position/distance/velocity output
  - Ctrl+C graceful exit
- 📊 **Data export:**
  - CSV logging for post-simulation analysis
  - Matplotlib plotting script included
- 🎯 **Modular architecture:**
  - Clean separation between physics, simulation, and rendering
  - Easy to extend with new scenarios or integrators

## Project Structure

The codebase is organized with clear separation of concerns:

```
Orbit-Sandbox/
├── main.py                # Entry point - CLI argument handling
├── requirements.txt       # Python dependencies
├── orbit/
│   ├── __init__.py
│   ├── body.py            # Body class - position, velocity, acceleration, mass
│   ├── physics.py         # Gravity calculations and orbital velocity formulas
│   ├── planets.py         # Real planet data (orbital parameters and masses)
│   ├── simulation.py      # Simulation class - physics loop, integration and time stepping
│   ├── systems.py         # Scenario factory functions (circular, elliptical, escape)
│   └── units.py           # Unit conversions and constants (AU, years, G)
├── tools/
│   ├── __init__.py
│   └── plot_orbit.py      # Matplotlib plotting script for CSV data
└── ui/
    ├── __init__.py
    └── visualize.py       # Pygame visualization and menu system
```

Core classes:
- **Body:** Represents a physical object with position, velocity, acceleration and mass
- **Simulation:** Orchestrates the physics loop, integration and advances time
- **Visualization:** Handles Pygame rendering, menu, and user input

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/josh-weston-g/Orbit-Sandbox.git
   cd Orbit-Sandbox
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
   > **Note:** Use Python 3.12 or 3.13. Python 3.14 has compatibility issues with pygame.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Console Mode

Run a specific scenario with terminal output:

```bash
# Circular orbit (defaults to Earth if --planet not specified)
python main.py --scenario circular

# Choose a specific planet
python main.py --scenario circular --planet mars
python main.py --scenario circular --planet jupiter

# Elliptical orbit
python main.py --scenario elliptical

# Escape trajectory
python main.py --scenario escape
```

Available planets: `mercury`, `venus`, `earth`, `mars`, `jupiter`, `saturn` (case-insensitive)

Output shows time, position, distance from star, and orbital speed at regular intervals.

### Visualization Mode

#### With menu selection:
```bash
python main.py --visualize

# Specify window resolution (defaults to auto)
python main.py --visualize --resolution 1080p
python main.py --visualize --resolution 1440p
```
This opens a menu where you can click to choose a scenario.

Available resolutions:
- `auto` - Auto-detect display size and use borderless fullscreen (default)
- `720p` - 1280×720 window
- `1080p` - 1920×1080 window
- `1440p` - 2560×1440 window

#### Direct to a specific scenario:
```bash
# Defaults to Earth if --planet not specified
python main.py --visualize --scenario circular

# Choose a specific planet
python main.py --visualize --scenario circular --planet saturn
```

**Visualization Controls:**
- **Mouse wheel/+/-:** Zoom in/out
- **WASD keys:** Pan camera up/left/down/right
- **Click and drag:** Pan camera with mouse
- **V:** Toggle velocity vector display (cyan arrows)
- **C:** Toggle acceleration vector display (red arrows)
- **G:** Toggle infinite grid overlay (0.5 AU spacing)
- **T:** Toggle orbital trail
- **[ / ]:** Adjust trail length
- **E:** Toggle energy display
- **Spacebar:** Pause/resume simulation
- **LEFT arrow:** Rewind simulation
- **R:** Reset simulation to initial conditions
- **ESC:** Return to scenario menu
- **UP/DOWN arrows:** Adjust simulation speed (when paused)

### Data Export and Plotting

Generate CSV data from a simulation run (requires minor code modification to use `sim.run_and_log()` instead of `sim.run_continuous()`), then plot the results:

```bash
python plot_orbit.py
```

This creates a 4-panel plot showing:
- Orbital path (x vs y)
- Distance from star over time
- Orbital speed over time
- Phase space diagram (distance vs speed)

## Requirements

- **Python 3.12 or 3.13** (Python 3.14 not yet supported due to pygame compatibility issues)
- NumPy
- Pygame
- Matplotlib (optional - for plotting)
- Pandas (optional - for plotting)

## How it Works

### Physics Engine

The simulation uses Newton's law of universal gravitation:

```
F = G * m1 * m2 / r²
```

Acceleration is computed from force, then **Velocity Verlet integration** (2nd order) updates velocity and position:

```python
# 1. Calculate acceleration at current position
old_acceleration = compute_acceleration(body, star, G)

# 2. Update position with half-step correction
position += velocity * dt + 0.5 * old_acceleration * dt²

# 3. Calculate acceleration at new position
new_acceleration = compute_acceleration(body, star, G)

# 4. Update velocity using average acceleration
velocity += 0.5 * (old_acceleration + new_acceleration) * dt
```

This method evaluates acceleration at both the start and end of each timestep, using their average for velocity updates. This provides 2nd-order accuracy and excellent long-term energy conservation, keeping orbits stable over thousands of orbits.

### Numerical Integration

The simulator uses a fixed timestep (`dt = 0.001` years) and advances the universe forward in discrete steps using the **Velocity Verlet algorithm**. Each step:
1. Computes gravitational acceleration at the current position
2. Updates position using current velocity plus a half-step acceleration correction
3. Computes new acceleration at the updated position
4. Updates velocity using the average of old and new accelerations
5. Advances simulation time

By evaluating forces at both the beginning and end of each timestep and averaging them, Velocity Verlet achieves 2nd-order accuracy. This means errors scale with dt² rather than dt, providing excellent long-term stability and energy conservation even with relatively large timesteps.

### Energy Conservation

The simulation displays total mechanical energy (kinetic + potential) as a diagnostic tool. In a perfect orbital system, total energy should remain constant. Thanks to the Velocity Verlet integrator (2nd order accuracy), energy is conserved to within ~0.01% over thousands of orbits - a 200x improvement over basic Euler methods. This excellent conservation allows the simulation to run stably for extended periods without drift.

## Known Limitations & Future Work

**Current limitations:**
- Single central mass only (star doesn't move)
- 2D simulation (no z-axis)
- Fixed timestep (not adaptive)

**Planned features:**
- N-body physics (multiple bodies affecting each other)
- Additional integration methods (RK4, adaptive timestep)
- Binary star systems
- 3-body chaos demonstrations
- Adjustable gravitational constant
- More scenario presets (Lagrange points, figure-8 orbits)
- Configurable integration method selection

## Contributing

This is a learning project and contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a Pull Request

Since this is a work in progress, feel free to open issues with ideas, bugs, or questions about the physics implementation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Josh Weston - [@josh-weston-g](https://github.com/josh-weston-g)
