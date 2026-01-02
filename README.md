# Orbit-Sandbox

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&logoColor=ffffff)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

A physics-accurate Newtonian orbital mechanics simulator built from first principles. Watch planets orbit stars, create elliptical trajectories, or launch escape maneuvers - all emerging naturally from Newton's laws and numerical integration.

> **⚠️ Work in Progress:** This project is actively under development. Features are being added incrementally, and the codebase is evolving. Expect breaking changes and incomplete functionality.

## What it does

Orbit-Sandbox simulates gravitational interactions between celestial bodies using real Newtonian physics - no predetermined paths, no fake orbits. You set initial conditions (position, velocity, mass), and the simulator evolves the system forward in time using Velocity Verlet integration. Orbital paths emerge naturally from the underlying forces.

The simulator can run in two modes:
- **Console mode:** Outputs orbital data to the terminal with periodic position/velocity updates
- **Visualization mode:** Interactive Pygame window with real-time rendering, zoom controls, and orbital trails

Whether you want to explore orbital mechanics, experiment with different initial conditions, or just watch a planet spiral into a star, Orbit-Sandbox provides an honest physics engine that behaves like the real universe.

## Current Features

- 🪐 **Three orbital scenarios:**
  - Circular orbit - stable, constant radius
  - Elliptical orbit - oscillates between periapsis and apoapsis
  - Escape trajectory - hyperbolic path to infinity
- ⚙️ **Honest physics simulation:**
  - Newtonian gravity (inverse square law)
  - Velocity Verlet integration (2nd order accuracy)
  - Excellent energy conservation
  - Conserves angular momentum
  - No hardcoded orbital paths
- 🎮 **Interactive visualization:**
  - Real-time Pygame rendering
  - Mouse wheel zoom with limits
  - Camera panning with WASD keys or click-and-drag
  - Toggleable velocity vector display with arrowheads
  - Toggleable grid overlay
  - Orbital trail rendering
  - Pause/resume with spacebar
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
├── main.py            # Entry point - CLI argument handling
├── body.py            # Body class - position, velocity, mass, integration
├── physics.py         # Gravity calculations and orbital velocity formulas
├── simulation.py      # Simulation class - physics loop and time stepping
├── systems.py         # Scenario factory functions (circular, elliptical, escape)
├── visualize.py       # Pygame visualization and menu system
├── plot_orbit.py      # Matplotlib plotting script for CSV data
└── requirements.txt   # Python dependencies
```

Core classes:
- **Body:** Represents a physical object with position, velocity, and mass
- **Simulation:** Orchestrates the physics loop and advances time
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
# Circular orbit
python main.py --scenario circular

# Elliptical orbit
python main.py --scenario elliptical

# Escape trajectory
python main.py --scenario escape
```

Output shows time, position, distance from star, and orbital speed at regular intervals.

### Visualization Mode

#### With menu selection:
```bash
python main.py --visualize
```
This opens a menu where you can click to choose a scenario.

#### Direct to a specific scenario:
```bash
python main.py --visualize --scenario circular
```

**Visualization Controls:**
- **Mouse wheel:** Zoom in/out
- **WASD keys:** Pan camera up/left/down/right
- **Click and drag:** Pan camera with mouse
- **V:** Toggle velocity vector display
- **G:** Toggle infinite grid overlay
- **T:** Toggle orbital trail
- **Spacebar:** Pause/resume simulation
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

The simulator uses a fixed timestep (`dt = 0.01`) and advances the universe forward in discrete steps. Each step:
1. Computes gravitational acceleration based on current positions
2. Updates velocities using acceleration
3. Updates positions using new velocities
4. Advances simulation time

This is an approximation of continuous calculus with small rectangles - the smaller the timestep, the more accurate the simulation.

### Energy Conservation

The simulation displays total mechanical energy (kinetic + potential) as a diagnostic tool. In a perfect orbital system, total energy should remain constant. Thanks to the Velocity Verlet integrator (2nd order accuracy), energy is conserved to within ~0.01% over thousands of orbits - a 200x improvement over basic Euler methods. This excellent conservation allows the simulation to run stably for extended periods without drift.

## Known Limitations & Future Work

**Current limitations:**
- Single central mass only (star doesn't move)
- 2D simulation (no z-axis)
- Fixed timestep (not adaptive)
- Arbitrary units (not real-world meters/kg/seconds yet)

**Planned features:**
- N-body physics (multiple bodies affecting each other)
- Real-world units (AU, solar masses, meters)
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
