import os
import logging
import json
import requests
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich import box
from rich import print
from rich.columns import Columns
from rich.panel import Panel

# set the root of the SW API URL - all API request URLs start with this
SWAPI_API_ROOT = "https://swapi.dev/api/"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# set up the app, creating the needed cache folder
def setup():
    os.remove("app.log")
    logging.basicConfig(
        filename="app.log"
    )
    if os.path.isdir("cache"):
        return
    os.mkdir("cache")

# handles making requests to the API, caching all data
def make_request(path):
    logger.log(logging.DEBUG, f"make_request({path})")
    cache_file_path = prepare_cache_file_path(path)
    logger.log(logging.DEBUG, f"  cache_file_path = {cache_file_path}")
    if file_exists(cache_file_path):
        logger.log(logging.DEBUG, f"  cache hit")
        return get_cache_json(cache_file_path)
    response = requests.get(SWAPI_API_ROOT + prepare_api_path(path))
    logger.log(logging.DEBUG, f"  response.status_code = {response.status_code}")
    save_cache(cache_file_path, response.text)
    return response.json()

# makes sure a URL is converted to a valid path for the API
def prepare_api_path(path):
    path = path.replace("http://", "https://")
    return path.replace(SWAPI_API_ROOT, "")

# saves data in a cache file
def save_cache(path, text):
    with open(path, "w+") as file:
        file.write(text)

# gets JSON from a cache file
def get_cache_json(path):
    with open(path, "r") as file:
        return json.loads(file.read())

# prepares the path for a cache file
def prepare_cache_file_path(path):
    return "cache/" + path.strip("/").replace("/", ".").replace("?", ".").replace("=", ".") + ".json"

def file_exists(path):
    return os.path.isfile(path)

def extract_id(url):
    return url.strip("/").split("/")[-1]

def clear(): 
    # for windows 
    if os.name == 'nt': 
        os.system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        os.system('clear') 

def main_screen():
    clear()
    print("")
    print("")
    print(".        .               .       .     .            .")
    print("   .           .        .                     .        .            .")
    print("             .               .    .          .              .   .         .")
    print("               _________________      ____         __________")
    print(" .       *    /                 |    /    \    .  |          \\")
    print("     .       /    ______   _____| . /      \      |    ___    |     .     .")
    print("             \    \    |   |       /   /\   \     |   |___>   |")
    print("           .  \    \   |   |      /   /__\   \  . |         _/               .")
    print(" .     ________>    |  |   | .   /            \   |   |\    \_______    .")
    print("      |            /   |   |    /    ______    \  |   | \           |")
    print("      |___________/    |___|   /____/      \____\ |___|  \__________|    .")
    print("  .     ____    __  . _____   ____      .  __________   .  _________")
    print("       \    \  /  \  /    /  /    \       |          \    /         |      .")
    print("        \    \/    \/    /  /      \      |    ___    |  /    ______|  .")
    print("         \              /  /   /\   \ .   |   |___>   |  \    \\")
    print("   .      \            /  /   /__\   \    |         _/.   \    \            +")
    print("           \    /\    /  /            \   |   |\    \______>    |   .")
    print("            \  /  \  /  /    ______    \  |   | \              /          .")
    print(" .       .   \/    \/  /____/      \____\ |___|  \____________/  LS")
    print("                               .                                        .")
    print("     +                           .         .               .                 .")
    print("                .                                   .            .")
    print("")
    options = [
        Panel("P: People"),
        Panel("S: Species"),
        Panel("T: Starships"),
        Panel("W: Worlds"),
        Panel("V: Vehicles"),
        Panel("F: Films")
    ]
    print(Columns(options))
    choice = input("Make your choice ('q' to quit): ").lower()
    if choice == "p":
        people_screen()
    if choice == "f":
        films_screen()

def people_screen():
    path = "people"
    navigate = True
    while navigate:
        clear()
        print(".______    _______   ______   .______    __       _______ ")
        print("|   _  \  |   ____| /  __  \  |   _  \  |  |     |   ____|")
        print("|  |_)  | |  |__   |  |  |  | |  |_)  | |  |     |  |__   ")
        print("|   ___/  |   __|  |  |  |  | |   ___/  |  |     |   __|  ")
        print("|  |      |  |____ |  `--'  | |  |      |  `----.|  |____ ")
        print("| _|      |_______| \______/  | _|      |_______||_______|")
        print()
        people = make_request(path)
        print(str(people["count"]) + " people in the database")
        render_people(people)
        action = do_navigation(people)
        if action == "q":
            navigate = False
        if action == "p":
            path = prepare_api_path(people["previous"])
        if action == "n":
            path = prepare_api_path(people["next"])
        if action.isnumeric():
            person_screen(action)
    main_screen()

def films_screen():
    path = "films"
    navigate = True
    while navigate:
        clear()
        print(" _______  __   __      .___  ___.      _______.")
        print("|   ____||  | |  |     |   \/   |     /       |")
        print("|  |__   |  | |  |     |  \  /  |    |   (----`")
        print("|   __|  |  | |  |     |  |\/|  |     \   \    ")
        print("|  |     |  | |  `----.|  |  |  | .----)   |   ")
        print("|__|     |__| |_______||__|  |__| |_______/    ")
        print()
        films = make_request(path)
        print(str(films["count"]) + " films in the database")
        render_films(films)
        action = do_navigation(films)
        if action == "q":
            navigate = False
        if action == "p":
            path = prepare_api_path(films["previous"])
        if action == "n":
            path = prepare_api_path(films["next"])
        if action.isnumeric():
            film_screen(action)
    main_screen()

def person_screen(id):
    clear()
    console = Console()
    with console.status("[bold green]Loading person details...") as status:
        person = make_request("people/" + id)
        person_details = render_person_details(person)

        if person["homeworld"] is not None and person["homeworld"] != "":
            homeworld = make_request(prepare_api_path(person["homeworld"]))
            homeworld_details = render_homeworld_details(homeworld)
        else:
            homeworld_details = """
Homeworld not recorded

"""
        if person["species"] is not None and len(person["species"]) > 0:
            species_list = render_species_list(person["species"])
        else:
            species_list = """
Species not recorded

"""        
        if person["starships"] is not None and len(person["starships"]) > 0:
            starships_list = render_starships_list(person["starships"])
        else:
            starships_list = """
Starships not recorded

"""
        if person["vehicles"] is not None and len(person["vehicles"]) > 0:
            vehicles_list = render_vehicles_list(person["vehicles"])
        else:
            vehicles_list = """
Vehicles not recorded

"""
        if person["films"] is not None and len(person["films"]) > 0:
            film_list = render_films_list(person["films"])
        else:
            film_list = """
Films not recorded

"""
        md = f"""
# {person["name"]}

{person_details}

## Homeworld

{homeworld_details}

## Species

{species_list}

## Starships

{starships_list}

## Vehicles

{vehicles_list}

## Films

{film_list}


"""
    markdown = Markdown(md)
    console.print(markdown)
    print()
    input("Press any key to return to the list of films")

def film_screen(id):
    clear()
    console = Console()
    with console.status("[bold green]Loading film details...") as status:
        film = make_request("films/" + id)
        film_details = render_film_details(film)

        if film["characters"] is not None and len(film["characters"]) > 0:
            characters_list = render_characters_list(film["characters"])
        else:
            characters_list = """
Characters not recorded

"""        
        if film["starships"] is not None and len(film["starships"]) > 0:
            starships_list = render_starships_list(film["starships"])
        else:
            starships_list = """
Starships not recorded

"""

    md = f"""
# {film["episode_id"]}: {film["title"]}

{film_details}

## Characters

{characters_list}

## Starships

{starships_list}


"""
    markdown = Markdown(md)
    console.print(markdown)
    print()
    input("Press any key to return to the list of films")

def render_person_details(person):
    return f"""
- Height: {person["height"]}cm
- Mass: {person["mass"]}kg
- Hair colour: {person["hair_color"]}
- Skin colour: {person["skin_color"]}
- Eye colour: {person["eye_color"]}
- Birth year: {person["birth_year"]}
- Gender: {person["gender"]}
"""

def render_film_details(film):
    return f"""
- Director: {film["director"]}
- Producer: {film["producer"]}
- Release date: {film["release_date"]}

{film["opening_crawl"]}

"""

def render_homeworld_details(homeworld):
    if homeworld["diameter"] == "0":
        diameter = "unknown"
    else:
        diameter = str(homeworld["diameter"]) + "km"
    return f"""
- Name: {homeworld["name"]}
- Terrain: {homeworld["terrain"]}
- Gravity: {homeworld["gravity"]}
- Population: {homeworld["population"]}
- Diameter: {diameter}
"""

def render_species_list(species):
    md = ""
    for species_url in species:
        species = make_request(prepare_api_path(species_url))
        md = md + f"""
- {species["name"]}
"""
    return md

def render_characters_list(characters):
    md = ""
    for character_url in characters:
        character = make_request(prepare_api_path(character_url))
        md = md + f"""
- {character["name"]}
"""
    return md

def render_starships_list(starships):
    md = ""
    for starship_url in starships:
        starship = make_request(prepare_api_path(starship_url))
        md = md + f"""
- {starship["name"]}
"""
    return md

def render_vehicles_list(vehicles):
    md = ""
    for vehicle_url in vehicles:
        vehicle = make_request(prepare_api_path(vehicle_url))
        md = md + f"""
- {vehicle["name"]}
"""
    return md

def render_films_list(films):
    md = ""
    for film_url in films:
        film = make_request(prepare_api_path(film_url))
        md = md + f"""
- {film["episode_id"]}: {film["title"]}
"""
    return md

def do_navigation(list):
    entry = "q"
    valid_entry = False
    valid_chars, text = setup_list_menu(list)
    while valid_entry == False:
        entry = input(text).lower()
        valid_entry = entry in valid_chars
    return entry

def setup_list_menu(list):
    valid_values = []
    text = "Enter 'n' for the next page, 'p' for the previous page, 'q' to return to the main screen, or an ID to view details: "
    for item in list["results"]:
        valid_values.append(extract_id(item["url"]))
    if list["next"] is not None and list["previous"] is not None:
        valid_values.extend(["n", "p", "q"])
    if list["next"] is None and list["previous"] is not None:
        text = "Enter 'p' for the previous page, 'q' to return to the main screen, or an ID to view details: "
        valid_values.extend(["p", "q"])
    if list["next"] is not None and list["previous"] is None:
        text = "Enter 'n' for the next page, 'q' to return to the main screen, or an ID to view details: "
        valid_values.extend(["n", "q"])
    if list["next"] is None and list["previous"] is None:
        text = "Enter 'q' to return to the main screen, or an ID to view details: "
        valid_values.extend(["q"])
    return valid_values, text

def render_people(people):
    table = Table(show_header=True, box=box.SIMPLE)
    table.add_column("ID", width=6)
    table.add_column("Name")
    table.add_column("Number of films")
    for person in people["results"]:
        table.add_row(
            extract_id(person["url"]), 
            person["name"],
            str(len(person["films"]))
        )
    console = Console()
    console.print(table)

def render_films(films):
    table = Table(show_header=True, box=box.SIMPLE)
    table.add_column("Episode ID", width=12)
    table.add_column("Title")
    table.add_column("Release date")
    for film in films["results"]:
        table.add_row(
            str(film["episode_id"]),
            film["title"],
            film["release_date"]
        )
    console = Console()
    console.print(table)

setup()
main_screen()