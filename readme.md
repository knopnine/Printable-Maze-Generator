# Maze Generator

The `maze_generator.py` script is designed to generate and render mazes using Python. This tool can be used for educational purposes, entertainment, or as part of larger projects involving puzzle generation.

## Features

- **Maze Generation**: Uses a depth-first search (DFS) algorithm to create mazes with specified dimensions.
- **PDF Output**: Generates PDF files containing the generated mazes. Optionally includes solutions marked on separate pages.
- **User Input**: Allows users to specify maze difficulty, number of pages, page size, orientation, and whether to include solution paths.
- **Command Line Interface**: Supports automation through command line arguments for easy batch generation.

## Installation

To run this script, you need Python installed on your system. No additional dependencies are required since the script uses built-in libraries.

## Usage

### Interactive Mode

Run the script without any command line arguments to interactively set up maze parameters:

```sh
python maze_generator.py
```

Follow the prompts to specify the maze difficulty, number of pages, page size, orientation, and whether to include solutions.

### Command Line Mode

For automated generation, use command line arguments. For example:

```sh
python maze_generator.py --difficulty expert --pages 3 --page-size a4 --orientation landscape --solutions --output custom_mazes.pdf
```

- `--difficulty`: Specifies the difficulty level of the mazes (choices: kids, easy, normal, hard, expert).
- `--pages`: Number of maze pages to generate.
- `--page-size`: Page size for the output PDF (choices: a4, letter).
- `--orientation`: Orientation of the page (choices: portrait, landscape).
- `--solutions`: Include solution paths in the generated mazes.
- `--output`: Custom filename for the output PDF.

### Output

The script will generate a PDF file containing the specified number of mazes. If solutions are included, they will be saved in a separate file with "_solutions" appended to the base filename.

## Example Outputs

- **Interactive Mode**: Prompts user for input and generates a PDF based on the provided settings.
- **Command Line Mode**: Automatically generates mazes according to the specified parameters without manual intervention.

This script provides a simple yet effective way to create maze puzzles, making it suitable for various applications where puzzle generation is required.