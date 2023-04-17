import json
from PIL import Image, ImageDraw, ImageFont


# the final for testing
# match_data = {'match_number': 3812391, 'home_team': {'name': 'FC Liverpool', 'number': '31', 'starting_lineup': [{'name': 'Alisson', 'profile_link': '/alisson/profil/spieler/105470', 'top': '80%', 'left': '40%', 'nationality': 'Brasilien'}, {'name': 'Konaté', 'profile_link': '/ibrahima-konate/profil/spieler/357119', 'top': '63%', 'left': '28%', 'nationality': 'Frankreich'}, {'name': 'van Dijk', 'profile_link': '/virgil-van-dijk/profil/spieler/139208', 'top': '63%', 'left': '52.5%', 'nationality': 'Niederlande'}, {'name': 'Robertson', 'profile_link': '/andrew-robertson/profil/spieler/234803', 'top': '61%', 'left': '7.5%', 'nationality': 'Schottland'}, {'name': 'Alexander-.', 'profile_link': '/trent-alexander-arnold/profil/spieler/314353', 'top': '61%', 'left': '73%', 'nationality': 'England'}, {'name': 'Fabinho', 'profile_link': '/fabinho/profil/spieler/225693', 'top': '39%', 'left': '40%', 'nationality': 'Brasilien'}, {'name': 'Henderson', 'profile_link': '/jordan-henderson/profil/spieler/61651', 'top': '28%', 'left': '53%', 'nationality': 'England'}, {'name': 'Thiago', 'profile_link': '/thiago/profil/spieler/60444', 'top': '28%', 'left': '27%', 'nationality': 'Spanien'}, {'name': 'Díaz', 'profile_link': '/luis-diaz/profil/spieler/480692', 'top': '10%', 'left': '15%', 'nationality': 'Kolumbien'}, {'name': 'Mané', 'profile_link': '/sadio-mane/profil/spieler/200512', 'top': '3%', 'left': '40%', 'nationality': 'Senegal'}, {'name': 'Mohamed Sa.', 'profile_link': '/mohamed-salah/profil/spieler/148455', 'top': '10%', 'left': '65%', 'nationality': 'Ägypten'}]}, 'away_team': {'name': 'Real Madrid', 'number': '418', 'starting_lineup': [{'name': 'Courtois', 'profile_link': '/thibaut-courtois/profil/spieler/108390', 'top': '80%', 'left': '40%', 'nationality': 'Belgien'}, {'name': 'Alaba', 'profile_link': '/david-alaba/profil/spieler/59016', 'top': '63%', 'left': '28%', 'nationality': 'Österreich'}, {'name': 'Militão', 'profile_link': '/eder-militao/profil/spieler/401530', 'top': '63%', 'left': '52.5%', 'nationality': 'Brasilien'}, {'name': 'Mendy', 'profile_link': '/ferland-mendy/profil/spieler/291417', 'top': '61%', 'left': '7.5%', 'nationality': 'Frankreich'}, {'name': 'Carvajal', 'profile_link': '/daniel-carvajal/profil/spieler/138927', 'top': '61%', 'left': '73%', 'nationality': 'Spanien'}, {'name': 'Casemiro', 'profile_link': '/casemiro/profil/spieler/16306', 'top': '39%', 'left': '40%', 'nationality': 'Brasilien'}, {'name': 'Kroos', 'profile_link': '/toni-kroos/profil/spieler/31909', 'top': '28%', 'left': '53%', 'nationality': 'Deutschland'}, {'name': 'Modric', 'profile_link': '/luka-modric/profil/spieler/27992', 'top': '28%', 'left': '27%', 'nationality': 'Kroatien'}, {'name': 'Valverde', 'profile_link': '/federico-valverde/profil/spieler/369081', 'top': '10%', 'left': '65%', 'nationality': 'Uruguay'}, {'name': 'Vinicius J.', 'profile_link': '/vinicius-junior/profil/spieler/371998', 'top': '10%', 'left': '15%', 'nationality': 'Brasilien'}, {'name': 'Benzema', 'profile_link': '/karim-benzema/profil/spieler/18922', 'top': '3%', 'left': '40%', 'nationality': 'Frankreich'}]}, 'competition_stage': 'FINAL', 'match_result': {'goals_home_team': '0', 'goals_away_team': '1'}}
# print(json.dumps(match_data, indent=4, ensure_ascii=False))

def prepare_away_team_for_image_generation(match_data):
    away_team = match_data['away_team']['starting_lineup']

    top_away = [player['top'] for player in away_team]
    left_away = [player['left'] for player in away_team]
    positions_in_tm_percentages = list(zip(top_away, left_away))

    # The tm percentages are 80% as max. We need to scale them to 1005 and convert to float
    positios_in_scaled_percentages = []
    for tup in positions_in_tm_percentages:
        x = float(tup[0].replace("%", "")) / 100.0
        y = float(tup[1].replace("%", "")) / 100.0
        scaled_x = x / 0.8
        scaled_y = y / 0.8
        positios_in_scaled_percentages.append((scaled_x, scaled_y))
    
    # The pitch background is 2000 x 3000 pixels. 
    # We need to map the percentages to the pixel values in the lower half for the away team
    top_start, top_end = 1650, 2800
    left_start, left_end = 100, 1900
    mapped_positions_away = []
    for percentage in positios_in_scaled_percentages:
        top = int(top_start + (top_end - top_start) * float(percentage[0]))
        left = int(left_start + (left_end - left_start) * float(percentage[1]))

        # switch from top left to left top to make it easier with the PIL library
        mapped_positions_away.append((left, top))
    
    # Get the nationalities and names of the away players as a list
    nationalities_away = [player['nationality'] for player in away_team]
    names_away = [player['name'] for player in away_team]

    return mapped_positions_away, nationalities_away, names_away

def prepare_home_team_for_image_generation(match_data):
    home_team = match_data['home_team']['starting_lineup']

    top_home = [player['top'] for player in home_team]
    left_home = [player['left'] for player in home_team]
    positions_in_tm_percentages = list(zip(top_home, left_home))

    # The tm percentages are 80% as max. We need to scale them to 1005 and convert to float
    positios_in_scaled_percentages = []
    for tup in positions_in_tm_percentages:
        x = float(tup[0].replace("%", "")) / 100.0
        y = float(tup[1].replace("%", "")) / 100.0
        scaled_x = x / 0.8
        scaled_y = y / 0.8
        positios_in_scaled_percentages.append((scaled_x, scaled_y))
    
    # The pitch background is 2000 x 3000 pixels. 
    # We need to map the percentages to the pixel values in the upper half for the home team
    # Also, the data for left needs to be reversed, because on Transfermarkt both teams are shown playing "upwards". Here the home team is playing "downwards"
    top_start, top_end = 1350, 150
    left_start, left_end = 1900, 100
    mapped_positions_home = []

    for percentage in positios_in_scaled_percentages:
        top = int(top_start + (top_end - top_start) * float(percentage[0]))
        left = int(left_start + (left_end - left_start) * float(percentage[1]))

        # switch from top left to left top to make it easier with the PIL library
        mapped_positions_home.append((left, top))

    # Get the nationalities and names of the home players as a list
    nationalities_home = [player['nationality'] for player in home_team]
    names_home = [player['name'] for player in home_team]

    return mapped_positions_home, nationalities_home, names_home


def generate_the_guessing_image(match_data):
    """
    Generate the image where the 22 flags are shown on the background image
    """
    folder = "data_gathering/images/countries"
    background = Image.open("data_gathering/images/background_2.png").convert("RGBA")


    # Put the flags of the home team on the background image
    mapped_positions_home, nationalities_home, names_home = prepare_home_team_for_image_generation(match_data)

    foregrounds = []
    for country in nationalities_home:
        foreground = folder + '/' + country + ".png"
        foregrounds.append(foreground)

    for i in range(len(foregrounds)):
        foreground = Image.open(foregrounds[i]).convert("RGBA")
        width, height = foreground.size
        positions = mapped_positions_home
        position = positions[i]
        position = (position[0] - width // 2, position[1] - height // 2)
        background.alpha_composite(foreground, position)


    # Put the flags of the away team on the background image
    mapped_positions_away, nationalities_away, names_away = prepare_away_team_for_image_generation(match_data)

    foregrounds = []
    for country in nationalities_away:
        foreground = folder + '/' + country + ".png"
        foregrounds.append(foreground)

    for i in range(len(foregrounds)):
        foreground = Image.open(foregrounds[i]).convert("RGBA")
        width, height = foreground.size
        positions = mapped_positions_away
        position = positions[i]
        position = (position[0] - width // 2, position[1] - height // 2)
        background.alpha_composite(foreground, position)

    #background.save("output.png")
    match_number = match_data['match_number']
    path = rf'static\competition_data\CL2122\{match_number}\guess.png'
    background.save(path)


def generate_the_solution_image(match_data):
    """
    Generate the image where the 22 flags are shown on the background image.
    Also, the names of the players are shown under the flags
    Aditionally, on an extension below of the pitch the information regarding the match is shown
    """
    folder = "data_gathering/images/countries"
    # Change folder team logos to the folder where the logos of the teams are stored rearding the competition. Here Champions League 2021/2022
    folder_team_logos = "data_gathering/images/CL2122"
    background = Image.open("data_gathering/images/background_2_extended.png").convert("RGBA")

    # specify a font
    font = ImageFont.truetype('arial.ttf', size=72)

    bold_font = ImageFont.truetype('arial.ttf', size=72)
    bold_font.font_variant = 'bold'

    # write text on the image
    draw = ImageDraw.Draw(background)

    # Put the flags of the home team on the background image
    mapped_positions_home, nationalities_home, names_home = prepare_home_team_for_image_generation(match_data)

    foregrounds = []
    for country in nationalities_home:
        foreground = folder + '/' + country + ".png"
        foregrounds.append(foreground)

    for i in range(len(foregrounds)):
        foreground = Image.open(foregrounds[i]).convert("RGBA")
        width, height = foreground.size
        positions = mapped_positions_home
        position = positions[i]
        position = (position[0] - width // 2, position[1] - height // 2)
        background.alpha_composite(foreground, position)

        # calculate position to center text below foreground image
        text_width, text_height = draw.textsize(names_home[i], font=bold_font)
        position_text = (position[0] + width // 2 - text_width // 2, position[1] + height + 20)

        draw.text(position_text, names_home[i], fill='black', font=bold_font)


    # Put the flags of the away team on the background image
    mapped_positions_away, nationalities_away, names_away = prepare_away_team_for_image_generation(match_data)

    foregrounds = []
    for country in nationalities_away:
        foreground = folder + '/' + country + ".png"
        foregrounds.append(foreground)

    for i in range(len(foregrounds)):
        foreground = Image.open(foregrounds[i]).convert("RGBA")
        width, height = foreground.size
        positions = mapped_positions_away
        position = positions[i]
        position = (position[0] - width // 2, position[1] - height // 2)
        background.alpha_composite(foreground, position)

        # calculate position to center text below foreground image
        text_width, text_height = draw.textsize(names_away[i], font=bold_font)
        position_text = (position[0] + width // 2 - text_width // 2, position[1] + height + 20)

        # write text on the image
        draw.text(position_text, names_away[i], fill='black', font=bold_font)

    # Write the match data solution on the extension of the background
    # COMPETITION STAGE
    competition_stage = match_data['competition_stage']
    if competition_stage == 'GROUP_STAGE':
        competition_stage = 'Gruppenphase'
    elif competition_stage == 'ROUND_OF_16':
        competition_stage = 'Achtelfinale'
    elif competition_stage == 'QUARTER_FINALS':
        competition_stage = 'Viertelfinale'
    elif competition_stage == 'SEMI_FINALS':
        competition_stage = 'Halbfinale'
    elif competition_stage == 'FINAL':
        competition_stage = 'Finale'
    
    text = competition_stage

    # Specify the font and font size
    font = ImageFont.truetype("arial.ttf", 72)

    # Specify the text color as dark green
    text_color = (0, 124, 0)

    # Get the size of the text
    text_width, text_height = font.getsize(text)

    # Calculate the position of the text
    x_position = (background.width - text_width) // 2
    y_position = 3000 + (text_height // 2)

    # If the y_position is greater than the height of the image, adjust it to align on top
    if y_position + (text_height // 2) > background.height:
        y_position = text_height // 2

    # Draw the text on the image
    draw = ImageDraw.Draw(background)
    draw.text((x_position, y_position), text, fill=text_color, font=font)

    # RESULT
    goals_home_team, goals_away_team = match_data['match_result']['goals_home_team'], match_data['match_result']['goals_away_team']
    text = f'{goals_home_team} : {goals_away_team}'

    # Specify the font and font size
    font = ImageFont.truetype("arial.ttf", 150)

    # Define the position for the "result" text
    result_text = text
    result_width, result_height = draw.textsize(result_text, font=font)

    # Calculate the position of the text
    x = background.width / 2
    y = (background.height - 3050) / 2 + 3050 - text_height / 2

    result_position = (x - result_width / 2, y - result_height / 2)

    # Draw the "result" text on the image
    draw.text(result_position, result_text, fill=text_color, font=font)

    # TEAM NAMES AND LOGOS

    font = ImageFont.truetype("arial.ttf", 72)
    home_team_name = match_data['home_team']['name']
    away_team_name = match_data['away_team']['name']

    # Get the dimensions of the image
    image_width, image_height = background.size

    home_team_name_width, home_team_name_height = draw.textsize(home_team_name, font=font)
    away_team_name_width, away_team_name_height = draw.textsize(away_team_name, font=font)

    home_team_x = image_width / 4
    home_team_y = image_height - home_team_name_height - 20

    away_team_x = 3 * image_width / 4
    away_team_y = image_height - away_team_name_height - 20

    draw.text((home_team_x, home_team_y), home_team_name, font=font, fill=text_color, anchor="mm")
    draw.text((away_team_x, away_team_y), away_team_name, font=font, fill=text_color, anchor="mm")

    folder_team_logos = "data_gathering/images/CL2122"
    home_team_logo = Image.open(f"{folder_team_logos}/{home_team_name}.png").convert("RGBA")
    away_team_logo = Image.open(f"{folder_team_logos}/{away_team_name}.png").convert("RGBA")

    # The x can be reused from the text, should be centered then
    home_team_logo_x = home_team_x - home_team_logo.width / 2
    away_team_logo_x = away_team_x - away_team_logo.width / 2
    
    # Find the height as the height of the text, 150 pixel buffer for the text underneath
    home_team_logo_y = image_height - home_team_logo.height - 150
    away_team_logo_y = image_height - away_team_logo.height - 150

    background.alpha_composite(home_team_logo, (int(home_team_logo_x), home_team_logo_y))
    background.alpha_composite(away_team_logo, (int(away_team_logo_x), away_team_logo_y))


    #Save the solution image on disk
    match_number = match_data['match_number']
    path = rf'static\competition_data\CL2122\{match_number}\solution.png'
    background.save(path)