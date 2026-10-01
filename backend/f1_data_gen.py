#import fastf1 as f1
#f1.set_log_level('CRITICAL') # ignores all warnings from fastf1 unless CRITICAL
import random
import os
import json
import time
from datetime import date

FEATURED_VENUES = [
    "British Grand Prix",
    "Spanish Grand Prix",
    "Hungarian Grand Prix",
    "Italian Grand Prix",
    "Monaco Grand Prix",
    "Australian Grand Prix",
    "Belgian Grand Prix",
    "Japanese Grand Prix",
    "Canadian Grand Prix",
    "United States Grand Prix",
    "Bahrain Grand Prix",
    "Brazilian Grand Prix",
    "Chinese Grand Prix",
    "Malaysian Grand Prix",
    "Austrian Grand Prix",
    "German Grand Prix",
    "Abu Dhabi Grand Prix",
    "Singapore Grand Prix",
    "European Grand Prix",
    "French Grand Prix",
    "Mexican Grand Prix",
]

with open('f1_race_results_2000_2026.json') as f:
    RACES = json.load(f)

def generate(level, featured): # future scope changes races/years active
    level += 1 # level 1 has 2 drivers

    if not featured: # if we not using featured
        race = random.choice(RACES)
    else:
        featuredRace = featured_race()
        matching = [r for r in RACES if r["race"] == featuredRace]  # all races at that venue
        race = random.choice(matching) 
    order = race['order']

    num = min(level, len(order))                # the anti-hang guard, still needed
    chosen = random.sample(order, num)          # random subset of drivers
    finishing_order = [d for d in order if d in chosen]  # subset, in correct order (the answer)

    random_drivers = finishing_order.copy()
    random.shuffle(random_drivers)

    return race['race'], race['year'], random_drivers, finishing_order


def featured_race():
    day = date.today().toordinal() # gets the day number
    featured = FEATURED_VENUES[day % len(FEATURED_VENUES)] # get the race
    return featured


def game_logic():
    alive = True
    level = 0

    while alive:
        level += 1 # add one to get number of drivers for that level

        race_name, year, drivers, results = generate(level)

        print(f"Level: {level}")
        print(f"Current Race: {race_name}")
        print(f"Season: {year}")

        for n in range(1, len(drivers)+1):
            print(f"Driver No{n}: {drivers[n - 1]}")

        print('\n')

        guess_order = []
        for j in range(1, len(drivers)+1):
            guess = input(f"What is your guess for Finishing Pos{j}: \n")
            guess_order.append(guess)

        if results == guess_order:
            alive = True
            print("You got them all correct! Well done, moving to the next level... \n")

        else:
            print("Awh damn you got it wrong! Better luck next time.")
            print(f"You got to Level {level}..")
            print(results)
            alive = False

    return


# generates a json file for races - unnecessary

def json_file():
    game_data = []

    for year in range(2025, 2027):
        print(year)
        schedule = f1.get_event_schedule(year)
        rounds = schedule[schedule['RoundNumber'] > 0]

        for _, race in rounds.iterrows():
            try:
                session = f1.get_session(year, int(race['RoundNumber']), 'R')
                session.load()
                finishers = session.results[
                    session.results['Status'].str.startswith(('Finished', '+'))
                ]
                order = finishers.sort_values('Position')['FullName'].tolist()

                time.sleep(20)

                if len(order) >= 6:  # enough drivers to support your levels
                    game_data.append({
                        'race': race['EventName'],
                        'year': year,
                        'order': order,
                    })
            except Exception:
                continue  # skip races that fail to load

        json.dump(game_data, open('races.json', 'w'), indent=2)


if __name__ == "__main__":
    json_file()
    #game_logic()

