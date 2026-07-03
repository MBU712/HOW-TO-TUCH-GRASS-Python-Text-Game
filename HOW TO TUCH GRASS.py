import random  # Randomizer
import pickle  # For saving and loading progress
import os      # For file handling
import sys
import time    # For delays
import urllib.request  # For downloading content updates
from colorama import Fore, init  # For styling text

init(autoreset = True)  # Automatically reset colorama styles after each print
os.chdir(os.path.dirname(sys.executable))  # Change working directory to the location of the executable (for bundled versions)

local_game_version = "1.3 Beta"  # Current version of the game

ITALIC_VAR = "\033[3m"
RESET_VAR = "\033[0m"

# ====== REMOTE URLs ======
GAME_VERSION_URL = "https://raw.githubusercontent.com/MBU712/HOW-TO-TUCH-GRASS-Python-Text-Game/refs/heads/main/game_version.txt"
VERSION_URL = "https://raw.githubusercontent.com/MBU712/HOW-TO-TUCH-GRASS-Github-Raw-Package/refs/heads/main/version.txt"
CONTENT_URL = "https://github.com/MBU712/HOW-TO-TUCH-GRASS-Github-Raw-Package/raw/refs/heads/main/content.bin"

# ====== DOWNLOAD LATEST CONTENT FILE ======
def get_latest_version():
    try:
        urllib.request.urlretrieve(VERSION_URL, "version.txt")
        with open("version.txt", "r") as f:
            latest = f.read().strip()
        os.remove("version.txt")
        return latest
    except Exception as e:
        print(f"Error occurred while fetching latest content. Refresh your internet and try again.")
        return "0"

#====== DOWNLOAD LATEST CODE VERSION ======
def get_latest_game_version():
    try:
        urllib.request.urlretrieve(GAME_VERSION_URL, "game_version.txt")
        with open("game_version.txt", "r") as f:
            latest = f.read().strip()
        os.remove("game_version.txt")
        return latest
    except Exception as e:
        print(f"Error occurred while fetching latest code version. Refresh your internet and try again.")
        return "0"

# ====== DOWNLOAD CONTENT.BIN ======
def download_content():
    try:
        urllib.request.urlretrieve(CONTENT_URL, "content.bin")
        print("Download complete.")
    except Exception as e:
        print(f"\nError occurred while downloading content. Refresh your internet and try again.")

# ====== LOAD CONTENT.BIN ======
def load_content():
    try:    
        with open("content.bin", "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error occurred while downloading content. Refresh your internet and try again.\n")
        time.sleep(1.2)
        sys.exit(0)


def load_slot(slot_name):
    #Load progress from a save file.
    try:
        with open(os.path.join("saves", f"{slot_name}.dat"), "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError):
        return {"games_found": [], "eggs_found": [], "coins": 0, "unlocked_themes":['Default']}

def save_slot(slot_name, progress):
    #Save progress to a file.
    with open(os.path.join("saves", f"{slot_name}.dat"), "wb") as f:
        pickle.dump(progress, f)

def get_completion(progress):
    total_found = len(progress["games_found"]) + len(progress["eggs_found"])
    total_possible = len(GAMES) + len(EASTER_EGGS)
    if total_possible == 0:
        return 0
    return round((total_found / total_possible) * 100, 2)

def get_rank(progress):
    percent = get_completion(progress)
    if percent == 100:
        return "🌿 GRASS GOD 🌿"
    elif percent >= 80:
        return "🌱 Grass Guardian"
    elif percent >= 60:
        return "🍃 Grass Master"
    elif percent >= 40:
        return "🌾 Turf Warrior"
    elif percent >= 20:
        return "🌱 Lawn Explorer"
    elif percent >= 10:
        return "🥀 Grass Beginner"
    elif percent >= 1: 
        return "🌵 Grass Noob 🌵"
    else:
        return "GET OUT OF MY LAWN YOU DON'T EVEN HAVE ANY GRASSTOUCHING EXPERIENCE"

def clearTerminal():
	os.system('cls' if os.name == 'nt' else 'clear')

def iinput(text):
    return input(Fore.LIGHTRED_EX + ITALIC_VAR + text + RESET_VAR)

def tprint(text):
    print(sel_theme + text)

def itprint(text):
    print(Fore.LIGHTRED_EX + ITALIC_VAR + text + RESET_VAR)

def oprint(text):
    print(ITALIC_VAR + Fore.LIGHTBLUE_EX + text + RESET_VAR)

# ====== CREATE SAVES FOLDER IF NONEXISTENT ======
if not os.path.exists("saves"):
    os.makedirs("saves")


# ====== STARTUP LOGIC ======
clearTerminal()
print("\n\nChecking for content updates...\n")
	
# ====== UPDATE CHECKER ======
latest_version = get_latest_version()
latest_game_version = get_latest_game_version()
if 'Beta' in local_game_version and (local_game_version[0] + local_game_version[1] + local_game_version[2]) == latest_game_version:
    latest_game_version_beta = latest_game_version
    
if not os.path.exists("content.bin"):
    print("\nNo local content found. Downloading...")
    download_content()
    content = load_content()
    local_version = content.get("version", "0")
else:
    content = load_content()
    local_version = content.get("version", "0")

if latest_version == "0":
    print("Can't fetch latest content.")
elif local_version != latest_version:
    print(f"New content version available! Local: {Fore.GREEN}{local_version}{Fore.RESET}, Latest: {Fore.GREEN}{latest_version}")
    print(f"Dowloading content version {Fore.GREEN}{latest_version}.")
    download_content()
    content = load_content()
else:
    print(f"\nContent is up to date.{Fore.GREEN} Version: {local_version}\n")

if latest_game_version == "0":
	print("Can't fetch latest version.")
elif 'Beta' in local_game_version:
    print(f"Game is in beta mode. Version: {Fore.GREEN}{local_game_version}{Fore.RESET}")
    try: 
        if latest_game_version == latest_game_version_beta:
            print(f"New stable version of current Beta version available! Local: {Fore.GREEN}{local_game_version}{Fore.RESET}, Latest: {Fore.GREEN}{latest_game_version}")
            print(f"Go to {Fore.YELLOW}'https://github.com/MBU712/HOW-TO-TUCH-GRASS-Python-Text-Game/releases'{Fore.RESET} and download the latest game release.")
        elif latest_game_version > latest_game_version_beta:
            print(f"New stable version available! Local: {Fore.GREEN}{local_game_version}{Fore.RESET}, Latest: {Fore.GREEN}{latest_game_version}")
            print(f"Go to {Fore.YELLOW}'https://github.com/MBU712/HOW-TO-TUCH-GRASS-Python-Text-Game/releases'{Fore.RESET} and download the latest game release.")
    except Exception as e:
        print(f"{Fore.CYAN}No matching or newer stable version found.")
elif local_game_version != latest_game_version and local_game_version < latest_game_version:
    print(f"New game version available! Local: {Fore.GREEN}{local_game_version}{Fore.RESET}, Latest: {Fore.GREEN}{latest_game_version}")
    print(f"Go to {Fore.YELLOW}'https://github.com/MBU712/HOW-TO-TUCH-GRASS-Python-Text-Game/releases'{Fore.RESET} and download the latest game release.")
    time.sleep(2)
    sys.exit(0)
else:
    print(f"Game is up to date. Version: {Fore.GREEN}{local_game_version}")

time.sleep(2)
clearTerminal()

# ====== UNPACK CONTENT ======
GAMES = content["games"]
EASTER_EGGS = content["eggs"]
THEMES = content["themes"]

# ====== SAVE SLOT SELECTION ======

# List of save names (without .dat)
SAVES = [f[:-4] for f in os.listdir("saves") if f.endswith(".dat")]

while True:
    print (Fore.WHITE + f'\nSelect a save slot from the following:\n')
    for n in SAVES:
            oprint(f"- {n}")
    print(Fore.WHITE + f'\nOr type "new" to start a new save, or type "q" to exit the game.')
    slot = iinput('\nType here: ').replace(' ', '').lower()
    # New Slot
    if slot == "new":
        slot = iinput("Enter a name for your new save: ").replace(' ', '_').lower()
        SAVES.append(slot)
        progress = {"games_found": [], "eggs_found": [], "coins": 0, "unlocked_themes":['Default']}
        break
    # Load a previous slot
    elif slot in SAVES:
        progress = load_slot(slot)
        break
    # Quit the game
    elif slot == "q":
        print("\nGoodbye!!! Go TUCH some grass!\n")
        time.sleep(1.2)
        sys.exit(0)
    # Invalid input
    else:
        clearTerminal()
        itprint("\nInvalid save name. Please try again.")
        time.sleep(0.9)
        clearTerminal()


# ====== REQUIRED KEYS CHECK ======
REQUIRED_KEYS = {
    "games_found": [],
    "eggs_found": [],
    "coins": 0,
    "unlocked_themes": ["Default"]
}

# ====== KEY AUTO-FIX =====
for key, default_value in REQUIRED_KEYS.items():
    if key not in progress:
        progress[key] = default_value

if "Default" not in progress["unlocked_themes"]:
    progress["unlocked_themes"].append("Default")

if "Default" not in progress["unlocked_backgrounds"]:
    progress["unlocked_backgrounds"].append("Default")

THEMEs = list()
for value in progress['unlocked_themes']:
    THEMEs.append(value)

themeS = list()
for value in THEMES.keys():
    themeS.append(value)
for value in progress['unlocked_themes']:
    themeS.remove(value)

length = 0
GAME = list(GAMES.keys())
EGG = list(EASTER_EGGS.keys())

# ====== THEME SELECTION ======
clearTerminal()
print("\n\nEnter the theme you would like to use for this game from the following:\n")
for t in THEMEs:
    oprint(f"-{t} ")
THEME=iinput("\nEnter your selected Theme here: ").title()

if THEME == "Default":
    print("Theme set to Default.")
    sel_theme = ""
elif THEME != "Default" and THEME in progress["unlocked_themes"]:
    print(f"Theme set to {THEME}.")
    sel_theme = THEMES[THEME]
else:
    print('Theme not recognized. Setting theme to default.')
    sel_theme = ""

time.sleep(1)
clearTerminal()

# ====== START MENU ======
print(ITALIC_VAR + Fore.WHITE + '\nHow To TUCH Grass!! \nBased On Your Favorite Games!!!' + RESET_VAR)
iinput('\nPress enter to continue....')

# ====== MAIN GAME STRUCTURE ======
while True:
    clearTerminal()
    tprint('\nType Your Favorite Video Game or Board Game Here,\nOr "q" To Quit The Game,\nOr "s" to save your progress,\nor "delete" to delete a save slot,\nor "p" to view your progress,\nOr "shop" to visit the grass shop,\nOr "themes" to change themes!!!')
    game: str = iinput('\n\nType here: ').replace(' ', '').lower()
    
    # === QUIT GAME ===
    if game == 'q':
        clearTerminal()
        tprint("\nWhich save slot do you want to save to?\n")
        for n in SAVES:
            oprint(f"- {n}")

        save_to = iinput("\nEnter the save name (or type 'none' to skip): ").replace(' ', '').lower()

        if save_to in SAVES:
            with open(os.path.join("saves", f"{save_to}.dat"), "wb") as f:
                pickle.dump(progress, f)
            tprint(f"\nProgress saved to {save_to}!")
        elif save_to == "none":
            tprint("\nProgress not saved.")
        else:
            tprint("\nProgress not saved.")

        tprint("\nGoodbye!!! Go TUCH some grass!\n")
        time.sleep(1.2)
        sys.exit(0)

    # === CHANGE THEME ===
    elif game == 'themes':
        clearTerminal()
        print("\n\nEnter the theme you would like to use for this game from the following:\n")
        for t in THEMEs:
            print(Fore.LIGHTRED_EX + "- " + t)
        print('\n')
        THEME=iinput(Fore.LIGHTRED_EX + ITALIC_VAR + "Enter your selected Theme here: " + Fore.RESET + RESET_VAR).title()

        if THEME in THEMES.keys() and THEME in progress["unlocked_themes"]:
            if THEME == "Default":
                print("Theme set to Default.")
                sel_theme = ""
            elif THEME != "Default" and THEME in progress["unlocked_themes"]:
                sel_theme = THEMES[THEME]
                tprint(f"Theme set to {THEME}.")
            else:
                print('Theme not recognized. Setting theme to default.')


    # === GAME LIST ===
    elif game == 'h':
        clearTerminal()
        tprint('\n == Games == \n')
        for g in GAME:
            tprint(g)
        iinput('\nPress enter to continue....')
        continue


    # === EASTER EGG LIST ===
    elif game == 'eh':
        clearTerminal()
        tprint('\n == Easter Eggs == \n')
        for e in EGG:
            tprint(e)
        iinput('\nPress enter to continue....')
        continue


    # === COUNT GAMES & EASTER EGGS ===
    elif game == 'len':
        clearTerminal()
        tprint('\nThe number of games in this list is: ' + str(len(GAMES) + len(EASTER_EGGS)))
        iinput('\nPress enter to continue....')
        continue


    # === COUNT EASTER EGGS ONLY ===
    elif game == 'lene':
        clearTerminal()
        tprint('\nThe number of easter eggs in this list is: ' + str(len(EASTER_EGGS)))
        iinput('\nPress enter to continue....')
        continue


    # === UNLOCK ALL PROGRESS ===
    elif game == 'grassgod':
        clearTerminal()
        tprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have ascended beyond mortal grass touchers.")

        progress["games_found"] = list(GAMES.keys())
        progress["eggs_found"] = list(EASTER_EGGS.keys())

        tprint("\n\nAll games and easter eggs unlocked!")
        iinput("\nPress Enter to continue...")
        continue


    # == UNLOCK ALL BACKGORUNDS ===
    elif game == 'backgroundgod':
        clearTerminal()
        tprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have unlocked all backgrounds.")

        progress["unlocked_themes"] = list(THEMES.keys())
        THEMEs.clear()
        THEMEs.extend(progress["unlocked_themes"])
        themeS.clear()

        tprint("\n\nAll backgrounds unlocked!")
        iinput("\nPress Enter to continue...")
        continue

    # == UNLOCK ALL THEMES ===
    elif game == 'themegod':
        clearTerminal()
        tprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have unlocked all themes.")

        progress["unlocked_themes"] = list(THEMES.keys())
        THEMEs.clear()
        THEMEs.extend(progress["unlocked_themes"])
        themeS.clear()

        tprint("\n\nAll themes unlocked!")
        iinput("\nPress Enter to continue...")
        continue


    # === GAIN GRASS COINS ===
    elif game == 'coingod':
        clearTerminal()
        tprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have discovered the secret to infinite Grass Coins.")

        progress["coins"] += 100

        tprint("\n\n+100 Grass Coins added!")
        iinput("\nPress Enter to continue...")
        continue


    # === GRASS SHOP ===
    elif game == 'shop':
        clearTerminal()
        tprint("\n=== 🌿 GRASS SHOP 🌿 ===")
        tprint(f"You have {progress['coins']} Grass Coins.\n")
        tprint("Available items:")
        tprint("1. Hint (5 coins)")
        tprint("2. Theme (10 coins)")
        tprint("3. Background (10 coins)")
        tprint("4. Exit shop")

        choice = iinput("\nChoose an option: ").strip()

        if choice == "1":
            if progress["coins"] >= 5:
                progress["coins"] -= 5
                hint = random.choice(list(GAMES.keys()))
                tprint(f"\n🌱 Your hint: Try searching for '{hint}'.")
            else:
                tprint("\nNot enough coins!")

        elif choice == "2":
            if progress["coins"] >= 10: 
                clearTerminal()
                tprint("\nAvailable themes:")
                for t in themeS:
                    tprint("- " + t)
                theme_choice = iinput("\nEnter the theme you want to unlock: ").title()
                if theme_choice in THEMES and theme_choice not in progress["unlocked_themes"]:
                    progress["coins"] -= 10
                    progress["unlocked_themes"].append(theme_choice)
                    THEMEs.append(theme_choice)
                    themeS.remove(theme_choice)
                    tprint(f"\nTheme '{theme_choice}' unlocked!")
                else:
                    tprint("\nInvalid theme choice or already unlocked.")
                    progress["coins"] += 10  # Refund coins if invalid choice
            else:
                tprint("\nNot enough coins!")

        elif choice == "3":
            clearTerminal()
            tprint("\nLeaving the shop...")

        else:
            tprint("\nInvalid choice. Leaving the shop...")

        iinput("\nPress Enter to continue...")
        continue


    # === RANDOM HINT ===
    elif game == 'seed':
        clearTerminal()
        all_games = list(GAMES.keys())
        hint = random.choice(all_games)
        tprint(f"\nA mysterious seed whispers: Try searching for '{hint}'...")
        iinput("\nPress Enter to continue...")
        continue


    # === GAME FROUND ===
    elif game in GAMES:
        clearTerminal()
        tprint(f'\n == {game.upper()} ==\n')
        tprint(GAMES[game][0])

        # If new discovery
        if game not in progress["games_found"]:
            tprint("\nWOW! You found this game for the first time!")
            progress["games_found"].append(game)
            progress["coins"] += 1
            tprint("+1 Grass Coin!")
        tprint('\nCongratulations!! If you followed the steps, you have OFFICIALLY TUCHED GRASS!!!!!')
        iinput('\nPress enter to continue....')
        continue


    # === SAVE PROGRESS ===
    elif game == 's':
        clearTerminal()
        tprint("\nWhich save slot do you want to save to?")
        for n in SAVES:
            tprint(Fore.LIGHTRED_EX + f"- {n}")

        save_to = iinput("\nEnter the save name: ").replace(" ", "").lower()

        if save_to in SAVES:
            save_slot(save_to, progress)
            tprint(f"\nProgress saved to {save_to}!")
        else:
            tprint("\nInvalid save name. Save cancelled.")

        iinput("\nPress Enter to continue...")
        continue


    # === DELETE SAVE SLOT ===
    elif game == 'delete':
        clearTerminal()
        tprint("\n=== DELETE SAVE SLOT ===")
        tprint("Available saves:")
        for n in SAVES:
            tprint(f"- {n}")

        to_delete = iinput("\nType the name of the save to delete: ").replace(" ", "").lower()

        if to_delete in SAVES:
            os.remove(f"saves/{to_delete}.dat")
            SAVES.remove(to_delete)
            tprint(f"\nSave '{to_delete}' deleted successfully!")
        else:
            tprint("\nSave not found. Nothing deleted.")

        iinput("\nPress Enter to continue...")
        continue


    # === VIEW PROGRESS ===
    elif game == 'p':
        clearTerminal()
        tprint("\n=== YOUR PROGRESS ===")
        tprint("\nGames found:")
        g = len(progress["games_found"])
        tprint(f"- {g}")

        tprint("\nEaster eggs found:")
        e = len(progress["eggs_found"])
        tprint(f"- {e}")

        percent = get_completion(progress)
        rank = get_rank(progress)
        
        tprint(f"\nCompletion: {percent}%")
        tprint(f"Rank: {rank}")
        tprint(f"\nGrass Coins: {progress['coins']}")

        iinput("\nPress Enter to continue...")
        continue


    # === EASTER EGG FOUND ===
    elif game in EASTER_EGGS:
        clearTerminal()
        tprint('\nCONGRATULATIONS!!! You have successfully found an easter egg!!!')
        tprint(f'\n == {game.upper()} ==\n')
        tprint(EASTER_EGGS[game][0])

        # If new discovery
        if game not in progress["eggs_found"]:
            tprint("\nWOW! You found this easter egg for the first time!")
            progress["eggs_found"].append(game)
            progress["coins"] += 2
            tprint("+2 Grass Coins!")
        tprint('\nCongratulations!! If you followed the steps, you have OFFICIALLY TUCHED GRASS!!!!!')
        iinput('\nPress enter to continue....')
        continue

    # === INVALID INPUT ===
    else:
        tprint('\nSorry, game not recognized. Try Again!!!')
        time.sleep(1)
