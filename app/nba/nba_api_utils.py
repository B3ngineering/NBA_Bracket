from nba_api.stats.endpoints import LeagueStandings
import json

def get_playoff_teams():
    """
    Fetch the current NBA playoff teams and their seedings.
    Returns two lists: east_teams and west_teams.
    """
    try:
        # Fetch the current league standings
        standings = LeagueStandings(season='2024-25')  # Adjust the season as needed
        standings_data = standings.get_normalized_dict()

        # Extract the playoff teams based on seeding
        east_teams = []
        west_teams = []

        for team in standings_data['Standings']:
            if team['Conference'] == 'East' and team['PlayoffRank'] <= 8:
                east_teams.append({
                    'seed': team['PlayoffRank'],
                    'team_name': team['TeamName']
                })
            elif team['Conference'] == 'West' and team['PlayoffRank'] <= 8:
                west_teams.append({
                    'seed': team['PlayoffRank'],
                    'team_name': team['TeamName']
                })

        return east_teams, west_teams

    except Exception as e:
        print(f"Error fetching playoff teams: {e}")
        return [], []