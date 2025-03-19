import sys
import curses
from curses import wrapper

from src.data.parser import parse_input_file, calculate_round_sizes, get_round_names
from src.ui.screens import show_welcome_screen, show_error_screen, show_no_file_screen
from src.ui.bracket_view import format_bracket


def main(stdscr):
    """
    Main function using curses.
    """
    # Set up curses
    curses.curs_set(0)  # Hide cursor
    stdscr.keypad(True)  # Enable keyboard special keys
    stdscr.clear()
    
    # Check if a filename was provided
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # Display a message and exit if no filename
        show_no_file_screen(stdscr)
        return
    
    # Show welcome screen
    show_welcome_screen(stdscr)
    
    # Parse the input file
    try:
        brackets = parse_input_file(filename)
        
        # Debug output
        print(f"Found {len(brackets)} brackets")
        
        if not brackets:
            show_error_screen(stdscr, "No valid brackets found in the input file.")
            return
        
        # Format and display each bracket
        current_bracket = 0
        
        while True:
            # Ensure we have a valid bracket index
            if current_bracket < 0:
                current_bracket = len(brackets) - 1
            elif current_bracket >= len(brackets):
                current_bracket = 0
                
            # Skip empty brackets
            if not brackets[current_bracket]:
                current_bracket += 1
                continue
                
            # Calculate round sizes and names for the current bracket
            round_sizes = calculate_round_sizes(brackets[current_bracket])
            round_names = get_round_names(round_sizes)
            
            # Display the bracket
            result = format_bracket(
                stdscr, 
                brackets[current_bracket], 
                current_bracket + 1, 
                round_sizes, 
                round_names, 
                total_brackets=len(brackets)
            )
            
            # Handle navigation result
            if result == "quit":
                break  # Exit the application
            elif result == "next":
                current_bracket += 1
            elif result == "prev":
                current_bracket -= 1
            else:
                # Default to next
                current_bracket += 1
                
    except FileNotFoundError:
        show_error_screen(stdscr, f"File not found: {filename}")
    except Exception as e:
        # Handle other errors
        import traceback
        traceback.print_exc()
        show_error_screen(stdscr, str(e))


if __name__ == "__main__":
    wrapper(main)  # curses wrapper handles setup/teardown