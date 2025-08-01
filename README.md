# Particle Swarm Optimization (PSO) Visualization

This project demonstrates a simple 1D Particle Swarm Optimization (PSO) algorithm and visualizes the movement of particles as they search for the optimum of a given objective function.

## Features

- 1D PSO implementation
- Interactive matplotlib animation showing particle movement, personal bests, and global best
- Play/pause and manual iteration navigation via slider

## Requirements

Install the required Python packages using pip:

```bash
pip install matplotlib numpy uv
```

## Running the Program

To run the visualization, use:

```bash
uv run main.py
```

Make sure your `main.py` file imports and calls the `visualize_pso()` function from `src/pso_algorithm_visualization.py`.

## Project Structure

```
pso_algorithm/
├── src/
│   ├── particle.py
│   ├── test_functions.py
│   ├── pso_algorithm.py
│   └── pso_algorithm_visualization.py
├── main.py
└── README.md
```

## Usage

- The animation window will show the objective function curve and the movement of particles.
- Use the play/pause button to control the animation.
- Use the slider to manually inspect any iteration.

## License

MIT