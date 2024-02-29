"""
Project for Week 4 of "Python Data Analysis".
Processing CSV files with baseball statistics.
"""

import csv


def load_data(filename, separator, quote):
    """
    Loads data from a CSV file into a list of dictionaries.

    Inputs:
      filename  - Name of the CSV file
      separator - Character that separates fields in the CSV
      quote     - Character used to quote fields in the CSV

    Output:
      Returns a list of dictionaries where each dictionary corresponds to a row in the CSV file.
    """
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter=separator, quotechar=quote)
        for row in reader:
            data.append(row)
    return data


def compute_top_stats_year(info, stat_function, numplayers, year):
    """
    Computes the top statistics for a given year.

    Inputs:
      info          - Dictionary containing information about the data files
      stat_function - Function to compute the statistic
      numplayers    - Number of top players to return
      year          - Year to filter by

    Output:
      Returns a list of dictionaries containing the top player statistics for the given year.
    """
    master_data = load_data(info["masterfile"], info["separator"], info["quote"])
    batting_data = load_data(info["battingfile"], info["separator"], info["quote"])

    year_stats = []
    for player in batting_data:
        if player[info["yearid"]] == str(year):
            player_id = player[info["playerid"]]
            player_info = next((item for item in master_data if item[info["playerid"]] == player_id), None)
            if player_info:
                player_stats = {**player, **player_info}
                year_stats.append(player_stats)

    top_stats = sorted(year_stats, key=lambda x: stat_function(info, x), reverse=True)[:numplayers]
    return top_stats


def compute_top_stats_career(info, stat_function, numplayers):
    """
    Computes the top career statistics.

    Inputs:
      info          - Dictionary containing information about the data files
      stat_function - Function to compute the statistic
      numplayers    - Number of top players to return

    Output:
      Returns a list of dictionaries containing the top player statistics for their career.
    """
    master_data = load_data(info["masterfile"], info["separator"], info["quote"])
    batting_data = load_data(info["battingfile"], info["separator"], info["quote"])

    career_stats = []
    for player in master_data:
        player_id = player[info["playerid"]]
        player_batting_data = [item for item in batting_data if item[info["playerid"]] == player_id]
        if player_batting_data:
            player_stats = {**player, **player_batting_data[-1]}
            career_stats.append(player_stats)

    top_stats = sorted(career_stats, key=lambda x: stat_function(info, x), reverse=True)[:numplayers]
    return top_stats


info = {
    "masterfile": "C:/Users/user/Downloads/Master_2016 (1).csv",
    "battingfile": "C:/Users/user/Downloads/Batting_2016 (1).csv",
    "separator": ",",
    "quote": '"',
    "playerid": "playerID",
    "firstname": "nameFirst",
    "lastname": "nameLast",
    "yearid": "yearID",
    "atbats": "AB",
    "hits": "H",
    "doubles": "2B",
    "triples": "3B",
    "homeruns": "HR",
    "walks": "BB",
    "battingfields": ["AB", "H", "2B", "3B", "HR", "BB"]
}


def batting_average(info, stat):
    if int(stat[info["atbats"]]) >= 500:
        return float(stat[info["hits"]]) / float(stat[info["atbats"]])
    else:
        return 0.0


def onbase_percentage(info, stat):
    if int(stat[info["atbats"]]) >= 500:
        return (float(stat[info["hits"]]) + float(stat[info["walks"]])) / float(stat[info["atbats"]])
    else:
        return 0.0


def slugging_percentage(info, stat):
    if int(stat[info["atbats"]]) >= 500:
        singles = float(stat[info["hits"]]) - float(stat["2B"]) - float(stat["3B"]) - float(stat["HR"])
        total_bases = singles + 2 * float(stat["2B"]) + 3 * float(stat["3B"]) + 4 * float(stat["HR"])
        return total_bases / float(stat[info["atbats"]])
    else:
        return 0.0


year = 2016
numplayers = 5

print("Top players by batting average in {}: ".format(year))
print(compute_top_stats_year(info, batting_average, numplayers, year))

print("\nTop players by on-base percentage in {}: ".format(year))
print(compute_top_stats_year(info, onbase_percentage, numplayers, year))

print("\nTop players by slugging percentage in {}: ".format(year))
print(compute_top_stats_year(info, slugging_percentage, numplayers, year))


# Additional functions for career stats

def compute_top_career_batting_average(info, numplayers):
    return compute_top_stats_career(info, batting_average, numplayers)


def compute_top_career_onbase_percentage(info, numplayers):
    return compute_top_stats_career(info, onbase_percentage, numplayers)


def compute_top_career_slugging_percentage(info, numplayers):
    return compute_top_stats_career(info, slugging_percentage, numplayers)


print("\nTopplayers by career batting average: ")
print(compute_top_career_batting_average(info, numplayers))

print("\nTop players by career on-base percentage: ")
print(compute_top_career_onbase_percentage(info, numplayers))

print("\nTop players by career slugging percentage: ")
print(compute_top_career_slugging_percentage(info, numplayers))
