"""
NCAA Bracket Viewer - Bracket View UI

This module handles the display of bracket data on the screen.
"""

import curses
from .components import draw_box, display_team, display_title, display_instructions, setup_colors


def format_bracket(stdscr, bracket_list, bracket_num, round_sizes, round_names, total_brackets):
    """
    Format and display a bracket with curses for fancy terminal display.
    
    Args:
        stdscr: Curses standard screen object
        bracket_list: List of teams in the bracket
        bracket_num: Number of the current bracket (for display purposes)
        round_sizes: List of integers representing the number of teams in each round
        round_names: List of strings with round names
    """
    # Get terminal dimensions
    max_y, max_x = stdscr.getmaxyx()
    
    # Setup colors
    colors = setup_colors()
    
    # Verify the bracket has the right number of teams
    total_expected = sum(round_sizes)
    if len(bracket_list) != total_expected:
        # Try to adjust by truncating or warning
        if len(bracket_list) > total_expected:
            bracket_list = bracket_list[:total_expected]
        else:
            # Show a warning at the bottom of the screen
            warning = f"Warning: Bracket {bracket_num} has {len(bracket_list)} teams, expected {total_expected}"
            stdscr.attron(curses.A_BOLD)
            stdscr.addstr(max_y-3, 2, warning[:max_x-4])
            stdscr.attroff(curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()  # Wait for keypress to acknowledge
    
    # Calculate column widths and how many rounds we can fit side by side
    longest_team_names = []
    start_idx = 0
    
    for i, size in enumerate(round_sizes):
        longest_name = 0
        for j in range(size):
            if start_idx + j < len(bracket_list):
                team = bracket_list[start_idx + j]
                try:
                    longest_name = max(longest_name, len(team.replace('-', ' ').title()))
                except Exception:
                    # If there's an error with a team name, use a default length
                    longest_name = max(longest_name, 20)
        longest_team_names.append(longest_name)
        start_idx += size
    
    # Each column needs space for: number (3), team name, and some padding (3)
    column_widths = [max(len(round_names[i]), longest_team_names[i] + 6) for i in range(len(round_sizes))]
    
    # Calculate how many rounds we can display at once based on screen width
    # We need to account for column widths plus spacing
    total_width = 0
    max_rounds_per_page = 0
    
    for width in column_widths:
        if total_width + width + 4 <= max_x - 4:  # Account for borders and spacing
            total_width += width + 4
            max_rounds_per_page += 1
        else:
            break
    
    max_rounds_per_page = max(1, max_rounds_per_page)  # At least show one round
    total_pages = (len(round_sizes) + max_rounds_per_page - 1) // max_rounds_per_page
    
    # Navigation between pages
    current_page = 0
    
    while True:
        stdscr.clear()
        
        # Draw bracket box
        draw_box(stdscr, 0, 0, max_y - 1, max_x - 1)
        
        # Draw the bracket header
        bracket_title = f"NCAA BRACKET {bracket_num}/{total_brackets} - Page {current_page + 1}/{total_pages}"
        display_title(stdscr, 1, bracket_title)
        
        # Calculate how many rounds we can fit on this page
        start_round = current_page * max_rounds_per_page
        end_round = min(start_round + max_rounds_per_page, len(round_sizes))
        rounds_on_page = end_round - start_round
        
        # Calculate columns and widths for this page
        actual_width = sum(column_widths[start_round:end_round]) + 4 * rounds_on_page
        start_x = max(2, (max_x - actual_width) // 2)
        
        # Calculate start_idx for this page
        current_start_idx = 0
        for i in range(start_round):
            if i < len(round_sizes):
                current_start_idx += round_sizes[i]
        
        # Display rounds side by side
        for col in range(rounds_on_page):
            round_idx = start_round + col
            if round_idx >= len(round_sizes):
                break
                
            size = round_sizes[round_idx]
            col_x = start_x + sum(column_widths[start_round:start_round + col]) + 4 * col
            
            # Round header
            round_title = round_names[round_idx] 
            stdscr.attron(curses.color_pair(colors['header']) | curses.A_BOLD)
            stdscr.addstr(3, col_x, round_title)
            stdscr.attroff(curses.color_pair(colors['header']) | curses.A_BOLD)
            
            # Title underline
            title_width = min(column_widths[round_idx], len(round_title))
            stdscr.hline(4, col_x, curses.ACS_HLINE, title_width)
            
            # Teams in this round
            current_y = 5
            max_lines_in_col = max_y - 8  # Leave space for headers and footer
            
            # Calculate if we need to shrink display due to many teams
            compress_display = size > max_lines_in_col
            line_skip = 1 if not compress_display else max(1, size // max_lines_in_col)
            
            for j in range(0, size, line_skip):
                if current_y >= max_y - 5:  # Leave space for footer
                    break
                    
                team_idx = current_start_idx + j
                if team_idx < len(bracket_list):
                    try:
                        team = bracket_list[team_idx]
                        
                        # Determine if this is a champion team
                        is_champion = (round_idx == len(round_sizes) - 1)
                        
                        # Display the team
                        display_team(
                            stdscr, 
                            current_y, 
                            col_x, 
                            j+1, 
                            team, 
                            is_champion=is_champion, 
                            max_width=column_widths[round_idx]
                        )
                    except Exception as e:
                        # If there's an error with a team, show a placeholder
                        error_msg = f"{j+1}. [Error: invalid team]"
                        stdscr.addstr(current_y, col_x, error_msg[:column_widths[round_idx]])
                    
                    current_y += 1
            
            current_start_idx += size
        
        # Special display for the champion (only on the last page)
        if end_round == len(round_sizes) and len(bracket_list) > 0:
            try:
                champion = bracket_list[-1]
                champion_text = f"CHAMPION: {champion.replace('-', ' ').title()}"
                
                # Position at the bottom of the screen
                champion_y = max_y - 4
                
                stdscr.attron(curses.color_pair(colors['champion']) | curses.A_BOLD)
                centered_x = (max_x - len(champion_text)) // 2
                stdscr.addstr(champion_y, centered_x, champion_text)
                stdscr.attroff(curses.color_pair(colors['champion']) | curses.A_BOLD)
            except Exception:
                # If there's an error with the champion, show a placeholder
                error_msg = "CHAMPION: [Error: invalid team]"
                stdscr.attron(curses.color_pair(colors['champion']) | curses.A_BOLD)
                centered_x = (max_x - len(error_msg)) // 2
                stdscr.addstr(max_y - 4, centered_x, error_msg)
                stdscr.attroff(curses.color_pair(colors['champion']) | curses.A_BOLD)
        
        # Navigation instructions
        navigation = []
        
        if current_page > 0:
            navigation.append("← Previous Page")
        else:
            navigation.append("← Previous Bracket")
        
        if current_page < total_pages - 1:
            navigation.append("→ Next Page")
        else:
            navigation.append("→ Next Bracket")
        
        navigation.append("q: Quit")
        
        nav_text = " | ".join(navigation)
        display_instructions(stdscr, max_y, nav_text)
        
        stdscr.refresh()
        
        # Handle key presses for navigation
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):  # Q to quit
            return "quit"
            
        elif key == curses.KEY_LEFT:
            if current_page > 0:
                current_page -= 1
            else:
                return "prev"  # Go to previous bracket if at first page
            
        elif key == curses.KEY_RIGHT:
            if current_page < total_pages - 1:
                current_page += 1
            else:
                return "next"  # Go to next bracket if at last page
            
        elif key == ord('n') or key == ord('N'):  # N for next bracket
            return "next"
            
        elif key == ord('p') or key == ord('P'):  # P for previous bracket
            return "prev"
            
        elif key == 10 or key == 13 or key == curses.KEY_ENTER:  # Enter key
            return "next"
            
        # Any other key just refreshes the current view