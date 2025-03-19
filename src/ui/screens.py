import curses
import textwrap
from .components import draw_box, display_title, display_instructions, setup_colors


def show_welcome_screen(stdscr):
    """
    Display a welcome screen with instructions.
    
    Args:
        stdscr: Curses standard screen object
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    
    # Setup colors
    setup_colors()
    
    # Draw box
    draw_box(stdscr, 0, 0, max_y - 1, max_x - 1, "NCAA BRACKET VIEWER")
    
    # Title
    display_title(stdscr, 2, "NCAA TOURNAMENT BRACKET VIEWER")
    
    # Instructions
    instructions = [
        "This tool helps you view your NCAA bracket predictions in a nice format.",
        "",
        "How to use:",
        "- Each bracket will be displayed one at a time",
        "- Press any key to navigate between screens",
        "- Teams are shown for each round of the tournament",
        "- The champion is highlighted at the end",
        "",
        "You can use this to easily enter your brackets online or compare predictions."
    ]
    
    y_pos = 5
    for line in instructions:
        if y_pos < max_y - 3:
            if not line:
                y_pos += 1
                continue
                
            wrapped_lines = textwrap.wrap(line, max_x - 10)
            for wrapped in wrapped_lines:
                if y_pos < max_y - 3:
                    x_pos = (max_x - len(wrapped)) // 2 if line.startswith("NCAA") else 5
                    stdscr.addstr(y_pos, x_pos, wrapped)
                    y_pos += 1
    
    # Press key to continue
    display_instructions(stdscr, max_y, "Press any key to start viewing brackets...")
    
    stdscr.refresh()
    stdscr.getch()


def show_error_screen(stdscr, error_message):
    """
    Display an error screen with the provided error message.
    
    Args:
        stdscr: Curses standard screen object
        error_message: Error message to display
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    
    # Setup colors
    setup_colors()
    
    # Draw box
    draw_box(stdscr, 0, 0, max_y - 1, max_x - 1, "ERROR")
    
    # Title
    display_title(stdscr, 2, "NCAA BRACKET VIEWER - ERROR")
    
    # Error message
    error_msg = f"Error: {error_message}"
    stdscr.addstr(max_y // 2, (max_x - len(error_msg)) // 2, error_msg)
    
    # Instructions
    display_instructions(stdscr, max_y, "Press any key to exit...")
    
    stdscr.refresh()
    stdscr.getch()


def show_no_file_screen(stdscr):
    """
    Display a screen indicating no input file was provided.
    
    Args:
        stdscr: Curses standard screen object
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    
    # Setup colors
    setup_colors()
    
    message = "No input file provided. Please provide a filename."
    stdscr.addstr(max_y // 2, (max_x - len(message)) // 2, message)
    
    usage = "Usage: python3 main.py <filename>"
    stdscr.addstr(max_y // 2 + 2, (max_x - len(usage)) // 2, usage)
    
    display_instructions(stdscr, max_y, "Press any key to exit...")
    
    stdscr.refresh()
    stdscr.getch()