"""
NCAA Bracket Viewer - UI Components

This module contains reusable UI components for the terminal interface.
"""

import curses


def draw_box(stdscr, start_y, start_x, height, width, title=None):
    """
    Draw a box with optional title in the terminal.
    
    Args:
        stdscr: Curses standard screen object
        start_y: Y-coordinate for the top-left corner
        start_x: X-coordinate for the top-left corner
        height: Height of the box
        width: Width of the box
        title: Optional title to display at the top of the box
    """
    # Draw the box
    stdscr.addch(start_y, start_x, curses.ACS_ULCORNER)
    stdscr.addch(start_y, start_x + width - 1, curses.ACS_URCORNER)
    stdscr.addch(start_y + height - 1, start_x, curses.ACS_LLCORNER)
    stdscr.addch(start_y + height - 1, start_x + width - 1, curses.ACS_LRCORNER)
    
    stdscr.hline(start_y, start_x + 1, curses.ACS_HLINE, width - 2)
    stdscr.hline(start_y + height - 1, start_x + 1, curses.ACS_HLINE, width - 2)
    stdscr.vline(start_y + 1, start_x, curses.ACS_VLINE, height - 2)
    stdscr.vline(start_y + 1, start_x + width - 1, curses.ACS_VLINE, height - 2)
    
    # Add title if provided
    if title:
        if len(title) > width - 4:
            title = title[:width - 7] + "..."
        title_x = start_x + (width - len(title)) // 2
        stdscr.addstr(start_y, title_x, f" {title} ")


def setup_colors():
    """
    Set up color pairs for the application.
    
    Returns:
        Dictionary mapping color names to their respective curses color pair numbers
    """
    curses.start_color()
    curses.use_default_colors()
    
    # Define color pairs
    curses.init_pair(1, curses.COLOR_BLUE, -1)      # Round headers
    curses.init_pair(2, curses.COLOR_GREEN, -1)     # Team names
    curses.init_pair(3, curses.COLOR_YELLOW, -1)    # Champion
    curses.init_pair(4, curses.COLOR_MAGENTA, -1)   # Bracket title
    curses.init_pair(5, curses.COLOR_CYAN, -1)      # Instructions
    
    # Return a dictionary for easier reference
    return {
        'header': 1,
        'team': 2,
        'champion': 3,
        'title': 4,
        'instruction': 5
    }


def display_team(stdscr, y, x, team_idx, team, is_champion=False, max_width=None):
    """
    Display a formatted team entry in the bracket view.
    """
    try:
        # Format team name (replace hyphens with spaces and title case)
        formatted_team = str(team).replace('-', ' ').title()
        
        # Truncate if needed
        if max_width and len(formatted_team) > max_width - 4:  # Account for number and dots
            formatted_team = formatted_team[:max_width - 7] + "..."
        
        # Format the complete entry with team number
        team_entry = f"{team_idx:2d}. {formatted_team}"
        
        # Apply champion formatting if needed
        if is_champion:
            stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(y, x, team_entry)
            stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
        else:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, team_entry)
            stdscr.attroff(curses.color_pair(2))
        
        return team_entry
    except Exception as e:
        # Handle errors gracefully
        error_entry = f"{team_idx:2d}. [Error]"
        stdscr.addstr(y, x, error_entry)
        return error_entry


def display_instructions(stdscr, max_y, text):
    """
    Display navigation instructions at the bottom of the screen.
    
    Args:
        stdscr: Curses standard screen object
        max_y: Maximum Y-coordinate (screen height)
        text: Instruction text to display
    """
    stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
    stdscr.addstr(max_y - 2, 2, text)
    stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)


def display_title(stdscr, y, title):
    """
    Display a centered title with appropriate formatting.
    
    Args:
        stdscr: Curses standard screen object
        y: Y-coordinate for the title
        title: Title text to display
    """
    max_y, max_x = stdscr.getmaxyx()
    x = (max_x - len(title)) // 2
    
    stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
    stdscr.addstr(y, x, title)
    stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)