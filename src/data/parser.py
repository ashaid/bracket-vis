def parse_input_file(filename):
    """
    Parse the input file containing bracket data.
    """
    brackets = []
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Find all brackets using string indices
    bracket_start = 0
    while True:
        # Find the start of a bracket
        bracket_start = content.find('[', bracket_start)
        if bracket_start == -1:
            break
        
        # Find the end of this bracket
        bracket_end = content.find(']', bracket_start)
        if bracket_end == -1:
            break
        
        # Extract the bracket content
        bracket_content = content[bracket_start+1:bracket_end]
        
        # Parse the teams
        teams = []
        for team in bracket_content.split(','):
            team = team.strip("' \"\t\n")
            if team:
                teams.append(team)
        
        if teams:
            brackets.append(teams)
        
        # Move past this bracket
        bracket_start = bracket_end + 1
    
    
    return brackets


def calculate_round_sizes(bracket):
    """
    Calculate the number of teams in each round of a bracket.
    """
    num_teams = len(bracket) // 2 + 1
    round_sizes = []
    teams_remaining = num_teams
    
    while teams_remaining > 1:
        round_sizes.append(teams_remaining)
        teams_remaining = teams_remaining // 2
    
    round_sizes.append(1)  # Championship winner
    
    return round_sizes


def get_round_names(round_sizes):
    """
    Determine appropriate names for tournament rounds based on the number of rounds.
    """
    if len(round_sizes) == 6:  # 64-team tournament (standard NCAA format)
        return ["First Round", "Second Round", "Sweet 16", "Elite 8", "Final Four", "Championship"]
    else:
        return [f"Round {i+1}" for i in range(len(round_sizes))]