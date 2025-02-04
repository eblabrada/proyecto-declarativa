# Robot Collector Path

## Objective

The objective of this project is to create a robot that collects garbage bags appearing on a map. The robot starts at a specific position and must collect all the garbage bags and return to its starting position, following the shortest path possible. 

The solution to the problem is achieved using dynamic programming with bitmask.

## Files

- `prog.hs`: Haskell program that calculates the shortest path for the robot to collect all garbage bags and return to the starting position.
- `app.py`: Python application that visualizes the robot's movement on the map using the `game2dboard` library.

## Prerequisites

- GHC (Glasgow Haskell Compiler)
- Python 3
- `game2dboard` library for Python

## How to Run

1. Ensure you have GHC (Glasgow Haskell Compiler) installed.
2. Ensure you have Python and the `game2dboard` library installed.
3. Run the Python application:

   ```sh
   python3 app.py
   ```

## License

This project is licensed under the MIT License.