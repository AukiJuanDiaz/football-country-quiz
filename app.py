from flask import Flask, render_template, request, session, redirect, url_for
import os
import random
import time
import json

def calculate_tendency(home_goals, away_goals):
    """
    Helper to get tendency out of a result
    """
    tendency = home_goals - away_goals
    if tendency > 0:
        return 1
    elif tendency < 0:
        return -1
    else:
        return 0


app = Flask(__name__)
# Necessary to allow session variables
app.secret_key = 'my_secret_key_test'

@app.route('/', methods=['GET', 'POST'])
def start_game():
    if request.method == 'POST':
        competition = request.form['competition']
        num_rounds = request.form['num_rounds']
        return redirect(url_for('guess_match', competition=competition, num_rounds=num_rounds))
    else:
        # Delete all session variables in case the user wants to start a new game again
        session.clear()
        return render_template('start_game.html')

@app.route("/guess_match", methods=['GET', 'POST'])
def guess_match():  
    if request.method == 'POST':
        # Get the arguments from the start page. So far not used
        competition = request.form.get('competition')
        num_rounds = request.form.get('num_rounds')

        # Specify the directory path
        dir_path = "static/competition_data/CL2122"

        # Check if this is the first call in this session by checking the session variables
        if 'random_match_number_list' in session:
            # key exists, do something with it
            random_match_number_list = session['random_match_number_list']

            # increase the round number
            round = session['round']
            round += 1
            session['round'] = round
        else:
            # FIRST ROUND
            # Initalize all session variables
            # Get a list of all subfolders in the directory
            subfolders = [f.path for f in os.scandir(dir_path) if f.is_dir()]
            match_numbers = [path.split('\\')[-1].rstrip() for path in subfolders]
        
            # Check if the number of rounds is smaller than the number of matches
            if int(num_rounds) > len(match_numbers):
                num_rounds = len(match_numbers)
            
            # Store the number of rounds in a session variable
            session['num_rounds'] = int(num_rounds)

            # Choose num_rounds many random subfolders from the list
            random.seed(time.time())
            random_match_number_list = random.sample(match_numbers, int(num_rounds))

            print(match_numbers)
            print(random_match_number_list)

            # Store the random_match_number_list in a session variable
            session['random_match_number_list'] = random_match_number_list

            # Start counting the rounds
            round = 1
            session['round'] = round

            # Start counting the points
            session['points_total'] = 0
            
        # In both cases, get the next match number from the list
        random_match_number = random_match_number_list[(round-1)]
        
        # put together the path to the image
        path_to_guess_image = rf"static/competition_data/CL2122/{random_match_number}/guess.png"
        return render_template("guess_match_CL2122.html", path_to_guess_image=path_to_guess_image)
    else:     
        # path_to_guess_image = "static/competition_data/CL2122/3714222/output.png"
        # ERROR case. Comes without an image
        return render_template("guess_match_CL2122.html")

@app.route("/match_solution", methods=['POST'])
def match_solution():
    if request.method == 'POST':
        # Get the data from the input form
        guessed_round = request.form.get('round')
        guessed_home_team = request.form.get('home-team')
        guessed_away_team = request.form.get('away-team')
        guessed_goals_home_team = request.form.get('digit1')
        guessed_goals_away_team = request.form.get('digit2')

        # Print all input for debugging
        print(f"guessed_round: {guessed_round}, guessed_home_team: {guessed_home_team}, guessed_away_team: {guessed_away_team}, guessed_goals_home_team: {guessed_goals_home_team}, guessed_goals_away_team: {guessed_goals_away_team}")

        # Get the number of the match out of the session to calculate the points
        random_match_number_list = session['random_match_number_list']
        round = session['round']
        random_match_number = random_match_number_list[(round-1)]
        path_to_match_data = rf"static/competition_data/CL2122/{random_match_number}/match_data.json"
        with open(path_to_match_data, 'r') as f:
            match_data = json.load(f)

        # Pretty printing the stage
        guessed_round_print = ""
        if guessed_round == 'GROUP_STAGE':
            guessed_round_print = 'Gruppenphase'
        elif guessed_round == 'ROUND_OF_16':
            guessed_round_print = 'Achtelfinale'
        elif guessed_round == 'QUARTER_FINALS':
            guessed_round_print = 'Viertelfinale'
        elif guessed_round == 'SEMI_FINALS':
            guessed_round_print = 'Halbfinale'
        elif guessed_round == 'FINAL':
            guessed_round_print = 'Finale'
        else:
            guessed_round_print = "-"

        # Input dummy values in case of missing inputs for the teams
        if guessed_home_team is None:
            guessed_home_team = "Heimteam"
        if guessed_away_team is None:
            guessed_away_team = "Auswärtsteam"


        # Pretty printing the goals in case of invalid input
        guessed_goals_home_team_print = guessed_goals_home_team
        guessed_goals_away_team_print = guessed_goals_away_team
        if guessed_goals_home_team is None or guessed_goals_away_team is None or guessed_goals_home_team == "" or guessed_goals_away_team == "":
            guessed_goals_home_team_print = "-"
            guessed_goals_away_team_print = "-"

            # Make sure the user does not get points for guessing the result, when none was entered
            guessed_goals_home_team = -1
            guessed_goals_away_team = -1

            # In case of invalid input, set tendency to inreachable value, so the user does not get any points for the tendency
            guessed_tendency = 2
        else:
            # In case the user entered a valid input, calculate the guessed_tendency
            guessed_tendency = calculate_tendency(int(guessed_goals_home_team), int(guessed_goals_away_team))

        # Calculate the actual tendency either way
        actual_tendency = calculate_tendency(int(match_data['match_result']['goals_home_team']), int(match_data['match_result']['goals_away_team']))

        # Fetch together the pretty version of the input data, also when the input was incomplete.
        text = f"Wettbewerbsphase: {guessed_round_print} \n {guessed_home_team} {guessed_goals_home_team_print} : {guessed_goals_away_team_print} {guessed_away_team}"
        print(text)


        path_to_match_data = rf"static/competition_data/CL2122/{random_match_number}/match_data.json"
        with open(path_to_match_data, 'r') as f:
            match_data = json.load(f)
        print(match_data)



        # Calculate points
        points_this_round = 0
        if guessed_round == match_data['competition_stage']:
            points_this_round += 1
        if guessed_home_team == match_data['home_team']['name']:
            points_this_round += 1
        if guessed_away_team == match_data['away_team']['name']:
            points_this_round += 1
        if guessed_goals_home_team == match_data['match_result']['goals_home_team'] and guessed_goals_away_team == match_data['match_result']['goals_away_team']:
            points_this_round += 2
        elif guessed_tendency == actual_tendency:
            points_this_round += 1
        
        print(f"points_this_round: {points_this_round}")

        # Add the points to the total points
        points_total = session['points_total']
        points_total += points_this_round
        session['points_total'] = points_total

        # Show how many rounds are played
        round = session['round']
        num_rounds = session['num_rounds']

        round_of_rounds = f"Runde {round} von {num_rounds}"

        last_round = False
        if round == num_rounds:
            # If this was the last round, show the final score
            last_round = True

        print("last_round:", last_round)
        return render_template("match_solution_CL2122.html",
                                text=text,
                                random_match_number=random_match_number,
                                points_this_round=points_this_round,
                                points_total=points_total,
                                round_of_rounds=round_of_rounds,
                                last_round=last_round)
    else:
        return render_template("match_solution_CL2122.html", text="ERROR")

if __name__ == "__main__":
    app.run(debug=True)