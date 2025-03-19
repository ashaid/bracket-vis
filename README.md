# NCAA Bracket Viewer

A terminal-based application to help view and navigate NCAA tournament brackets, making it easier to input picks on websites.

## Features

- Parse and display NCAA tournament brackets
- Navigate between different brackets
- Color-coded terminal interface
- View brackets by round with proper formatting
- Highlight champions and round progressions

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bracket-vis.git
cd bracket-vis
```

## Usage

```bash
# Run directly from the project root
python main.py <path-to-bracket-file>
```

### Input File Format

The input file should contain bracket data in the following format:

```
['team1', 'team2', ..., 'champion1'] ['team1', 'team2', ..., 'champion2']
```

Each bracket is enclosed in square brackets, with team names listed in order of appearance in the bracket. The last team in each list is the champion.

## Navigation

- Press any key to navigate between screens
- Each bracket will be displayed one at a time
- Multiple rounds are shown on each page when possible

## Project Structure

```
bracket-vis/
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── components.py      # UI components like boxes, team displays
│   │   ├── screens.py         # Welcome screen, help screen
│   │   └── bracket_view.py    # Main bracket display logic
│   ├── data/
│   │   ├── __init__.py
│   │   └── parser.py          # File parsing and data handling
├── main.py                    # Main entry point
├── LICENSE
└── README.md
```

## Requirements

- Python 3.6+
- curses (included in standard library for Unix/Linux/macOS)
  - For Windows users, you'll need to install the `windows-curses` package

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - a strong copyleft license that requires anyone who distributes your code or derivative works to make the source available under the same terms.

See the [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) for more details.
