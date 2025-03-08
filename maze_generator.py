import random
import os
import argparse
from reportlab.lib.pagesizes import A4, LETTER, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class MazeGenerator:
    def __init__(self, width, height):
        # Ensure odd dimensions for proper maze generation
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        
    def generate(self):
        """Generate a maze using depth-first search algorithm"""
        # Initialize maze with walls
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        def carve_path(x, y):
            maze[y][x] = 0
            # Four directions: right, down, left, up (with 2-cell steps for proper walls)
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.width and 0 <= new_y < self.height and maze[new_y][new_x] == 1):
                    # Carve the wall between current cell and the new cell
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve_path(new_x, new_y)
        
        # Start carving from position (1,1)
        carve_path(1, 1)
        
        # Create entrance and exit
        maze[0][1] = 0  # Top entrance
        maze[self.height - 1][self.width - 2] = 0  # Bottom exit
        
        return maze

class MazePDFRenderer:
    def __init__(self, page_size=A4, orientation='portrait'):
        self.page_size = landscape(page_size) if orientation == 'landscape' else page_size
        self.page_width, self.page_height = self.page_size
        
    def render_to_pdf(self, mazes, filename, title=None, solution=False):
        """Render multiple mazes to a PDF file"""
        c = canvas.Canvas(filename, pagesize=self.page_size)
        
        for i, maze in enumerate(mazes):
            # Calculate appropriate scaling
            scale_factor = 0.8  # Use 80% of available space
            cell_size = min(self.page_width / len(maze[0]), 
                           self.page_height / len(maze)) * scale_factor
            
            maze_width = len(maze[0]) * cell_size
            maze_height = len(maze) * cell_size
            
            # Center the maze on the page
            x_offset = (self.page_width - maze_width) / 2
            y_offset = (self.page_height - maze_height) / 2
            
            # Add title if provided
            if title:
                c.setFont("Helvetica-Bold", 14)
                c.drawString(x_offset, self.page_height - y_offset / 2, 
                            f"{title} - Page {i+1}")
                
                # Add difficulty indicator
                maze_size = f"{len(maze[0])}x{len(maze)}"
                difficulty = ""
                if len(maze[0]) <= 11: difficulty = "Kids"
                elif len(maze[0]) <= 21: difficulty = "Easy"
                elif len(maze[0]) <= 31: difficulty = "Normal" 
                elif len(maze[0]) <= 41: difficulty = "Hard"
                else: difficulty = "Expert"
                
                c.setFont("Helvetica", 10)
                c.drawString(x_offset, self.page_height - y_offset / 2 - 15, 
                            f"Difficulty: {difficulty} ({maze_size})")
            
            # Draw the maze
            c.setLineWidth(0.5)  # Thin walls
            
            # Draw the grid
            for y in range(len(maze)):
                for x in range(len(maze[0])):
                    cell_x = x_offset + x * cell_size
                    cell_y = self.page_height - y_offset - (y + 1) * cell_size
                    
                    if maze[y][x] == 1:  # Wall
                        c.setFillColor(colors.black)
                        c.rect(cell_x, cell_y, cell_size, cell_size, fill=1)
                    elif solution and maze[y][x] == 2:  # Solution path
                        c.setFillColor(colors.lightgreen)
                        c.rect(cell_x, cell_y, cell_size, cell_size, fill=1)
            
            # Mark entrance and exit
            c.setFillColor(colors.green)
            c.circle(x_offset + 1 * cell_size + cell_size/2, 
                    self.page_height - y_offset - 0 * cell_size - cell_size/2, 
                    cell_size/4, fill=1)
            
            c.setFillColor(colors.red)
            c.circle(x_offset + (len(maze[0])-2) * cell_size + cell_size/2, 
                    self.page_height - y_offset - (len(maze)-1) * cell_size - cell_size/2, 
                    cell_size/4, fill=1)
            
            if i < len(mazes) - 1:
                c.showPage()
        
        c.save()

class MazeSolver:
    @staticmethod
    def solve(maze):
        """Solve the maze using BFS algorithm and return a new maze with the solution path"""
        height = len(maze)
        width = len(maze[0])
        
        # Create a copy of the maze for the solution
        solution = [row[:] for row in maze]
        
        # Find entrance and exit
        start = (1, 0)  # Assuming entrance is at (1,0)
        end = (width-2, height-1)  # Assuming exit is at (width-2, height-1)
        
        # BFS algorithm
        queue = [start]
        visited = {start: None}  # Store parent of each visited cell
        
        while queue:
            current = queue.pop(0)
            
            # If we reached the exit
            if current == end:
                break
            
            # Check neighboring cells
            x, y = current
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                # Check if the neighboring cell is valid and not a wall
                if (0 <= nx < width and 0 <= ny < height and 
                    maze[ny][nx] == 0 and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited[(nx, ny)] = current
        
        # Reconstruct the path
        if end in visited:
            current = end
            while current != start:
                x, y = current
                solution[y][x] = 2  # Mark the solution path
                current = visited[current]
        
        return solution

def get_user_input():
    """Get user input for maze generation"""
    difficulties = {
        "kids": (10, 10),
        "easy": (20, 20),
        "normal": (30, 30),
        "hard": (40, 40),
        "expert": (60, 60)
    }
    
    print("\n=== MAZE GENERATOR ===")
    print("Choose difficulty: kids, easy, normal, hard, expert")
    difficulty = input("Difficulty: ").lower()
    while difficulty not in difficulties:
        print("Invalid choice. Choose: kids, easy, normal, hard, expert")
        difficulty = input("Difficulty: ").lower()
    
    width, height = difficulties[difficulty]
    
    try:
        pages = int(input("Number of mazes (1 or more): "))
        if pages < 1:
            raise ValueError
    except ValueError:
        print("Invalid input. Defaulting to 1 maze.")
        pages = 1
    
    page_size = input("Page size (A4 or letter) [default: A4]: ").upper()
    if page_size not in ["A4", "LETTER"]:
        print("Invalid choice. Defaulting to A4.")
        page_size = "A4"
    
    orientation = input("Orientation (portrait or landscape) [default: portrait]: ").lower()
    if orientation not in ["portrait", "landscape"]:
        print("Invalid choice. Defaulting to portrait.")
        orientation = "portrait"
    
    include_solutions = input("Include solutions? (y/n) [default: n]: ").lower() == 'y'
    
    return width, height, pages, page_size, orientation, include_solutions

def main():
    # Command line arguments for automation
    parser = argparse.ArgumentParser(description='Generate mazes.')
    parser.add_argument('--difficulty', choices=['kids', 'easy', 'normal', 'hard', 'expert'],
                        help='Maze difficulty')
    parser.add_argument('--pages', type=int, help='Number of maze pages to generate')
    parser.add_argument('--page-size', choices=['a4', 'letter'], help='Page size')
    parser.add_argument('--orientation', choices=['portrait', 'landscape'], help='Page orientation')
    parser.add_argument('--solutions', action='store_true', help='Include solutions')
    parser.add_argument('--output', help='Output PDF filename')
    args = parser.parse_args()
    
    # If command line arguments are provided, use them
    if args.difficulty:
        difficulties = {
            "kids": (10, 10),
            "easy": (20, 20),
            "normal": (30, 30),
            "hard": (40, 40),
            "expert": (60, 60)
        }
        width, height = difficulties[args.difficulty]
        pages = args.pages or 1
        page_size = args.page_size or "a4"
        orientation = args.orientation or "portrait"
        include_solutions = args.solutions
        output_file = args.output or f"maze_{width}x{height}_{pages}pages.pdf"
    else:
        # Get input interactively
        print("Welcome to the Maze Generator!")
        width, height, pages, page_size, orientation, include_solutions = get_user_input()
        output_file = f"maze_{width}x{height}_{pages}pages.pdf"
    
    # Create generator and renderer
    generator = MazeGenerator(width, height)
    renderer = MazePDFRenderer(
        page_size=A4 if page_size.upper() == "A4" else LETTER,
        orientation=orientation
    )
    
    # Generate mazes
    mazes = []
    for _ in range(pages):
        maze = generator.generate()
        mazes.append(maze)
    
    # Generate solutions if requested
    if include_solutions:
        solution_mazes = []
        for maze in mazes:
            solution = MazeSolver.solve(maze)
            solution_mazes.append(solution)
        
        # Split the output filename
        base, ext = os.path.splitext(output_file)
        solution_file = f"{base}_solutions{ext}"
        
        # Render solutions
        renderer.render_to_pdf(
            solution_mazes, 
            solution_file, 
            title="Maze Solutions", 
            solution=True
        )
        print(f"Solutions generated and saved as '{solution_file}'")
    
    # Render mazes
    renderer.render_to_pdf(mazes, output_file, title="Maze Puzzle")
    
    print(f"\nMazes generated and saved as '{output_file}'")
    print("Entrance is at the top (green), exit is at the bottom (red).")

if __name__ == "__main__":
    main()