import random  # Randomizer
import pickle  # For saving and loading progress
import os      # For file handling
import sys
import time    # For delays
import urllib.request  # For downloading content updates
from colorama import Fore, Back, init  # For styling text

init(autoreset = True)  # Automatically reset colorama styles after each print
os.chdir(os.path.dirname(sys.executable))  # Change working directory to the location of the executable (for bundled versions)

local_game_version = "2.0"  # Current version of the game

if os.name == 'nt':  # Check if the operating system is Windows
    local_app_data = os.getenv("LOCALAPPDATA")  # Get the local app data directory
    save_dir = os.path.join(local_app_data, "How_To_TUCH_Grass", "saves")
elif os.name == 'posix':  # Check if the operating system is macOS or Linux
    save_dir = os.path.expanduser("~/Library/Application Support/MyGame/saves")

ITALIC_VAR = "\033[3m"
RESET_VAR = "\033[0m"

# ====== REMOTE URLs ======
GAME_VERSION_URL = "https://raw.githubusercontent.com/MBU712/HOW-TO-TUCH-GRASS-Python-Text-Game/refs/heads/main/game_version.txt"
VERSION_URL = "https://raw.githubusercontent.com/MBU712/HOW-TO-TUCH-GRASS-Github-Raw-Package/refs/heads/main/version.txt"
CONTENT_URL = "https://github.com/MBU712/HOW-TO-TUCH-GRASS-Github-Raw-Package/raw/refs/heads/main/content.bin"

# ====== DOWNLOAD LATEST CONTENT FILE ======
def get_latest_version():
    try:
        file_path = os.path.join(save_dir, "version.txt")
        urllib.request.urlretrieve(VERSION_URL, file_path)
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
        file_path = os.path.join(save_dir, "game_version.txt")
        urllib.request.urlretrieve(GAME_VERSION_URL, file_path)
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
        file_path = os.path.join(save_dir, "content.bin")
        urllib.request.urlretrieve(CONTENT_URL, file_path)
        print("Download complete.")
    except Exception as e:
        print(f"\nError occurred while downloading content. Refresh your internet and try again.")

# ====== LOAD CONTENT.BIN ======
def load_content():
    try:    
        file_path = os.path.join(save_dir, "content.bin")
        with open(file_path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error occurred while accessing content. Try again later. Note: this might be because of a previous downloading error.\n")
        time.sleep(1.2)
        sys.exit(0)

def load_slot(slot_name):
    #Load progress from a save file.
    try:
        with open(os.path.join(save_dir, f"{slot_name}.dat"), "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError):
        return {"games_found": [], "eggs_found": [], "coins": 0, "unlocked_themes":['Default']}

def save_slot(slot_name, progress):
    #Save progress to a file.
    with open(os.path.join(save_dir, f"{slot_name}.dat"), "wb") as f:
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
    return input(Fore.LIGHTRED_EX + Back.BLACK + ITALIC_VAR + text + RESET_VAR)

def tprint(text):
    print(sel_bg + sel_theme + text)

def itprint(text):
    print(Fore.LIGHTRED_EX + Back.BLACK + ITALIC_VAR + text + RESET_VAR)

def oprint(text):
    print(ITALIC_VAR + Fore.LIGHTBLUE_EX + Back.BLUE + text + RESET_VAR)

def iprint(text):
    print(ITALIC_VAR + text + RESET_VAR)

# ====== CREATE SAVES FOLDER IF NONEXISTENT ======
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


# ====== STARTUP LOGIC ======
clearTerminal()
print("\n\nChecking for updates...\n")
	
# ====== UPDATE CHECKER ======
latest_version = get_latest_version()
latest_game_version = get_latest_game_version()
if 'Beta' in local_game_version and (local_game_version[0] + local_game_version[1] + local_game_version[2]) == latest_game_version:
    latest_game_version_beta = latest_game_version
    
if not os.path.exists(os.path.join(save_dir, "content.bin")):
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
BACKGROUNDS = content["backgrounds"]

# ====== SAVE SLOT SELECTION ======
# List of save names (without .dat)
SAVES = [f[:-4] for f in os.listdir(save_dir) if f.endswith(".dat")]

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
    "unlocked_themes": ["Default"],
    "unlocked_backgrounds": ["Default"]
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

BACKGROUNDs = list()
for value in progress['unlocked_backgrounds']:
    BACKGROUNDs.append(value)

backgroundS = list()
for value in BACKGROUNDS:
    backgroundS.append(value)
for value in progress['unlocked_backgrounds']:
    backgroundS.remove(value)

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

# ====== BACKGROUND SELECTION ======
clearTerminal()
print("\n\nEnter the text background you would like to use for this game from the following:\n")
for t in BACKGROUNDs:
    oprint(f"-{t} ")
BACKGROUND=iinput("\nEnter your selected Background here: ").title()

if BACKGROUND == "Default":
    print("Background set to Default.")
    sel_bg = ""
elif BACKGROUND in BACKGROUNDs:
    sel_bg = BACKGROUNDS[BACKGROUND]
    print(f"Background set to {BACKGROUND}.")
else:
    print('Background not recognized. Setting background to default.')
    sel_bg = ""

time.sleep(1)
clearTerminal()

# ====== START MENU ======
print(ITALIC_VAR + Fore.WHITE + '\nHow To TUCH Grass!! \nBased On Your Favorite Games!!!' + RESET_VAR)
iinput('\nPress enter to continue....')

# ====== MAIN GAME STRUCTURE ======
while True:
    clearTerminal()
    tprint('\nType Your Favorite Video Game or Board Game Here,\nOr "q" To Quit The Game,\nOr "s" to save your progress,\nor "delete" to delete a save slot,\nor "p" to view your progress,\nOr "shop" to visit the grass shop,\nOr "locker" to change your theme or background.')
    game: str = iinput('\n\nType here: ').replace(' ', '').lower()
    
    # === QUIT GAME ===
    if game == 'q':
        clearTerminal()
        tprint("\nWhich save slot do you want to save to?\n")
        for n in SAVES:
            oprint(f"- {n}")

        while True:
            save_to = iinput("\nEnter the save name (or type 'none' to skip): ").replace(' ', '').lower()
        
            if save_to in SAVES:
                with open(os.path.join("saves", f"{save_to}.dat"), "wb") as f:
                        pickle.dump(progress, f)
                itprint(f"\nProgress saved to {save_to}!")
                break
            elif save_to == "none":
                itprint("\nProgress not saved.")
                break
            else:
                itprint("\nInvalid selection.")
                continue

        itprint("\nGoodbye!!! Go TUCH some grass!\n")
        time.sleep(1.2)
        sys.exit(0)


    # ====== LOCKER MENU ======
    elif game == 'locker':
        clearTerminal()
        itprint("\n=== 🌿 GRASS LOCKER 🌿 ===")
        iprint("1. Change Theme")
        iprint("2. Change Background")
        iprint("3. Exit Locker")

        locker_choice = iinput("\nChoose an option: ").strip().lower()

        if locker_choice == "1" or locker_choice.lower() == "theme":
            clearTerminal()
            print("\n\nEnter the theme you would like to use for this game from the following:\n")
            for t in THEMEs:
                oprint("- " + t)
            print('\n')
            THEME=iinput(Fore.LIGHTRED_EX + ITALIC_VAR + "Enter your selected Theme here: " + Fore.RESET + RESET_VAR).title()

            if THEME in THEMES.keys() and THEME in progress["unlocked_themes"]:
                if THEME == "Default":
                    itprint("Theme set to Default.")
                    sel_theme = ""
                elif THEME != "Default" and THEME in progress["unlocked_themes"]:
                    sel_theme = THEMES[THEME]
                    itprint(f"Theme set to {THEME}.")
            else:
                print('Theme not recognized. Setting theme to default.')
            time.sleep(0.7)
            continue

        elif locker_choice == "2" or locker_choice.lower() == "background":
            clearTerminal()
            print("\n\nEnter the background you would like to use for this game from the following:\n")
            for t in BACKGROUNDs:
                oprint("- " + t)
            print('\n')
            BACKGROUND=iinput(Fore.LIGHTRED_EX + ITALIC_VAR + "Enter your selected Background here: " + Fore.RESET + RESET_VAR).title()

            if BACKGROUND in BACKGROUNDS:
                if BACKGROUND == "Default":
                    itprint("Background set to Default.")
                    sel_bg = ""
                else:
                    sel_bg = BACKGROUNDS[BACKGROUND]
                    itprint(f"Background set to {BACKGROUND}.")
            else:
                print('Background not recognized. Setting background to default.')
                sel_bg = ""
            time.sleep(0.7)
            continue

        elif locker_choice == "3" or locker_choice.lower() == "exit":
            print("\nExiting locker...")
            time.sleep(0.7)
            continue
        else:
            tprint("\nInvalid choice. Returning to main menu...")
            time.sleep(0.7)
            continue


    # === GAME LIST ===
    elif game == 'h':
        clearTerminal()
        itprint('\n == Games == \n')
        for g in GAME:
            tprint(g)
        iinput('\nPress enter to continue....')
        continue


    # === EASTER EGG LIST ===
    elif game == 'eh':
        clearTerminal()
        itprint('\n == Easter Eggs == \n')
        for e in EGG:
            tprint(e)
        iinput('\nPress enter to continue....')
        continue


    # === COUNT GAMES & EASTER EGGS ===
    elif game == 'len':
        clearTerminal()
        iprint('\nThe number of games in this list is: ' + str(len(GAMES) + len(EASTER_EGGS)))
        iinput('\nPress enter to continue....')
        continue


    # === COUNT EASTER EGGS ONLY ===
    elif game == 'lene':
        clearTerminal()
        iprint('\nThe number of easter eggs in this list is: ' + str(len(EASTER_EGGS)))
        iinput('\nPress enter to continue....')
        continue


    # === UNLOCK ALL PROGRESS ===
    elif game == 'grassgod':
        clearTerminal()
        itprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have ascended beyond mortal grass touchers.")

        progress["games_found"] = list(GAMES.keys())
        progress["eggs_found"] = list(EASTER_EGGS.keys())

        tprint("\n\nAll games and easter eggs unlocked!")
        iinput("\nPress Enter to continue...")
        continue


    # == UNLOCK ALL BACKGORUNDS ===
    elif game == 'backgroundgod':
        clearTerminal()
        itprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have unlocked all backgrounds.")

        progress["unlocked_backgrounds"] = list(BACKGROUNDS.keys())
        THEMEs.clear()
        THEMEs.extend(progress["unlocked_backgrounds"])
        themeS.clear()

        tprint("\n\nAll backgrounds unlocked!")
        iinput("\nPress Enter to continue...")
        continue

    # == UNLOCK ALL THEMES ===
    elif game == 'themegod':
        clearTerminal()
        itprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
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
        itprint("\n====== 🌿 SECRET UNLOCKED 🌿 ======")
        tprint("\nYou have discovered the secret to infinite Grass Coins.")

        progress["coins"] += 100

        tprint("\n\n+100 Grass Coins added!")
        iinput("\nPress Enter to continue...")
        continue


    # === GRASS SHOP ===
    elif game == 'shop':
        clearTerminal()
        itprint("\n=== 🌿 GRASS SHOP 🌿 ===")
        iprint(f"You have {progress['coins']} Grass Coins.\n")
        itprint("Available items:")
        iprint("1. Hint (5 coins)")
        iprint("2. Theme (10 coins)")
        iprint("3. Background (10 coins)")
        iprint("4. Exit shop")

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
            if progress["coins"] >= 10: 
                clearTerminal()
                tprint("\nAvailable backgrounds:")
                for t in backgroundS:
                    tprint("- " + t)
                background_choice = iinput("\nEnter the background you want to unlock: ").title()
                if background_choice in BACKGROUNDS and background_choice not in progress["unlocked_backgrounds"]:
                    progress["coins"] -= 10
                    progress["unlocked_backgrounds"].append(background_choice)
                    BACKGROUNDs.append(background_choice)
                    backgroundS.remove(background_choice)
                    tprint(f"\nBackground '{background_choice}' unlocked!")
                else:
                    tprint("\nInvalid background choice or already unlocked.")
                    progress["coins"] += 10  # Refund coins if invalid choice
            else:
                tprint("\nNot enough coins!")

        elif choice == "4":
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
        iprint(f"\nA mysterious seed whispers: Try searching for '{hint}'...")
        iinput("\nPress Enter to continue...")
        continue


    # === GAME FROUND ===
    elif game in GAMES:
        clearTerminal()
        itprint(f'\n == {game.upper()} ==\n')
        oprint(GAMES[game][0])

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
        iprint("\nWhich save slot do you want to save to?")
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
        itprint("\n=== DELETE SAVE SLOT ===")
        tprint("Available saves:")
        for n in SAVES:
            iprint(f"- {n}")

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
        itprint("\n=== YOUR PROGRESS ===")
        tprint("\nGames found:")
        g = len(progress["games_found"])
        iprint(f"- {g}")

        tprint("\nEaster eggs found:")
        e = len(progress["eggs_found"])
        iprint(f"- {e}")

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
        iprint('\nCONGRATULATIONS!!! You have successfully found an easter egg!!!')
        itprint(f'\n == {game.upper()} ==\n')
        tprint(EASTER_EGGS[game][0])

        # If new discovery
        if game not in progress["eggs_found"]:
            iprint("\nWOW! You found this easter egg for the first time!")
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
