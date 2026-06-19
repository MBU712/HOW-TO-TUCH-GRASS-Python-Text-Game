import random  # Randomizer
import pickle  # For saving and loading progress
import os      # For file handling
import urllib.request  # For downloading content updates
try:
    from colorama import Fore, Style  # For styling text
except Exception as e:
    print("Colorama is not installed. Please install it by typing 'pip install colorama' in the terminal and try again. \nIf that doesn't work, please make sure you have the latest python version installed and it is set as your default Python interpreter.\nIf you are on a mobile device, use the appropriate pip installer for your editor, for example, for Pydroid 3, go into the menu and press the option 'Pip', Then install Colorama from the menu that pops up.\n\nWithout Colorama, all Themes features will not function and cause errors. ")
    exit()


# ====== REMOTE URLs ======
VERSION_URL = "https://raw.githubusercontent.com/MBU712/HOW-TO-TUCH-GRASS-Github-Raw-Package/refs/heads/main/version.txt"
CONTENT_URL = "https://github.com/MBU712/HOW-TO-TUCH-GRASS-Github-Raw-Package/raw/refs/heads/main/content.bin"

# ====== DOWNLOAD LATEST VERSION FILE ======
def get_latest_version():
    try:
        urllib.request.urlretrieve(VERSION_URL, "version.txt")
        with open("version.txt", "r") as f:
            latest = f.read().strip()
        os.remove("version.txt")
        return latest
    except Exception as e:
        print(f"Error occurred while fetching latest version. Refresh your internet and try again.")
        return "0"

# ====== DOWNLOAD CONTENT.BIN ======
def download_content():
    print("\nDownloading content...")
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
        exit()

# ====== STARTUP LOGIC ======
print("\n\nChecking for content updates...")

latest_version = get_latest_version()

if not os.path.exists("content.bin"):
    print("\nNo local content found. Downloading...")
    download_content()
    content = load_content()
else:
    content = load_content()
    local_version = content.get("version", "0")

    if local_version != latest_version:
        print(f"New content version available! Local: {local_version}, Latest: {latest_version}")
        download_content()
        content = load_content()
    else:
        print(f"Content is up to date. Version: {local_version}")

# ====== UNPACK CONTENT ======
GAMES = content["games"]
EASTER_EGGS = content["eggs"]
THEMES = content["themes"]



# Create saves folder if missing
if not os.path.exists("saves"):
    os.makedirs("saves")




# List of save names (without .dat)
SAVES = [f[:-4] for f in os.listdir("saves") if f.endswith(".dat")]




def RS():
    return "\n".join(SAVES)




def load_slot(slot_name):
    #Load progress from a save file.
    try:
        with open(f"saves/{slot_name}.dat", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, pickle.UnpicklingError):
        return {"games_found": [], "eggs_found": [], "coins": 0, "unlocked_themes":['Default']}




def save_slot(slot_name, progress):
    #Save progress to a file.
    with open(f"saves/{slot_name}.dat", "wb") as f:
        pickle.dump(progress, f)



print (Fore.WHITE + f'\n\nSelect a save slot from the following:\n\n{RS()}\n\nOr type "new" to start a new save, or type "q" to exit the game.')
slot = input(Fore.LIGHTRED_EX + '\nType here: ' + Fore.RESET).replace(' ', '').lower()
# New Slot
if slot == "new":
    slot = input(Fore.LIGHTRED_EX + "Enter a name for your new save: " + Fore.RESET).replace(' ', '_').lower()
    SAVES.append(slot)
    progress = {"games_found": [], "eggs_found": [], "coins": 0, "unlocked_themes":['Default']}
# Load a previous slot
elif slot in SAVES:
    progress = load_slot(slot)
# Quit the game
elif slot == "q":
    print("\nGoodbye!!! Go TUCH some grass!\n")
    exit()
# Invalid input
else:
    print("\nInvalid save name. Please choose again.\n")
    print(RS())
    slot = input(Fore.LIGHTRED_EX + "Enter a valid save name or type 'new': " + Fore.RESET).replace(' ', '').lower()




    if slot == "new":
        slot = input(Fore.LIGHTRED_EX + "Enter a name for your new save: " + Fore.RESET).replace(' ', '_').lower()
        SAVES.append(slot)
        progress = {"games_found": [], "eggs_found": [], "coins": 0, "unlocked_themes":['Default']}
    else:
        progress = load_slot(slot)


# Required keys and their default values
REQUIRED_KEYS = {
    "games_found": [],
    "eggs_found": [],
    "coins": 0,
    "unlocked_themes": ["Default"]
}

# Auto-fix missing keys
for key, default_value in REQUIRED_KEYS.items():
    if key not in progress:
        progress[key] = default_value

if "Default" not in progress["unlocked_themes"]:
    progress["unlocked_themes"].append("Default")




def get_completion(progress):
    total_found = len(progress["games_found"]) + len(progress["eggs_found"])
    total_possible = len(GAMES) + len(EASTER_EGGS)
    if total_possible == 0:
        return 0
    return round((total_found / total_possible) * 100, 2)




# This function returns a rank based on the percentage of games and easter eggs found. You can customize the ranks and their thresholds as you see fit.
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
        return "GET OUT OF MY LAWN YOU DON'T EVEN HAVE ANY GRASS TOUCHING EXPERIENCE"
    
# A list of secret commands
SECRET_COMMANDS = {
    "grassgod": "Unlocks all games and easter eggs",
    "seed": "Gives a random hint",
    "secret": "Shows this secret menu",
    'len': "Shows the total number of games and easter eggs in the list",
    'len_easter': "Shows the total number of easter eggs in the list",
    'h': "Shows the list of games",
    'eh': "Shows the list of easter eggs"
}

def tprint(text):
    print(sel_theme + text + Style.RESET_ALL)


    
ITALIC_VAR = "\033[3m"
RESET_VAR = "\033[0m"



THEMEs = list()
for value in progress['unlocked_themes']:
    THEMEs.append(value)

themeS = list()
for value in THEMES.keys():
    themeS.append(value)
for value in progress['unlocked_themes']:
    themeS.remove(value)






# These 3 following lines list only the game and easter egg names.
length = 0
GAME = list(GAMES.keys())
EGG = list(EASTER_EGGS.keys())

print("\n\nEnter the theme you would like to use for this game from the following:\n")
for t in THEMEs:
    print("- " + t)
print('\n')
THEME=input(Fore.LIGHTRED_EX + ITALIC_VAR + "Enter your selected Theme here: " + Fore.RESET + RESET_VAR).title()

if THEME in THEMES.keys() and THEME in progress["unlocked_themes"]:
    if THEME == "Default":
        print("Theme set to Default.")
        sel_theme = ""
    elif THEME != "Default" and THEME in progress["unlocked_themes"]:
        print(f"Theme set to {THEME}.")
        sel_theme = THEMES[THEME]
else:
    print('Theme not recognized. Setting theme to default.')

print(sel_theme + ITALIC_VAR + '\n\nHow To TUCH Grass!! \nBased On Your Favorite Games!!!' + RESET_VAR)


# This while loop is the entire functionality of the game.
while True:
    tprint('\nType Your Favorite Video Game or Board Game Here,\nOr type "r" For A Random Game,\nOr "q" To Quit The Game,\nOr "s" to save your progress,\nor "delete" to delete a save slot,\nor "p" to view your progress,\nOr "shop" to visit the grass shop,\nOr "themes" to change themes!!!')
    game: str = input(Fore.LIGHTRED_EX + ITALIC_VAR + '\n\nType here: ' + Fore.RESET + RESET_VAR).replace(' ', '').lower()
    
    # Quit game and save progress option
    if game == 'q':
        tprint("\nWhich save slot do you want to save to?")
        for n in SAVES:
            tprint(f"- {n}")

        save_to = input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nEnter the save name (or type 'none' to skip): " + Fore.RESET + RESET_VAR).replace(' ', '').lower()

        if save_to in SAVES:
            with open(f"saves/{save_to}.dat", "wb") as f:
                pickle.dump(progress, f)
            tprint(f"\nProgress saved to {save_to}!")
        elif save_to == "none":
            tprint("\nProgress not saved.")
        else:
            tprint("\nProgress not saved.")

        tprint("\nGoodbye!!! Go TUCH some grass!\n")
        break

    elif game == 'themes':
        print("\n\nEnter the theme you would like to use for this game from the following:\n")
        for t in THEMEs:
            print("- " + t)
        print('\n')
        THEME=input(Fore.LIGHTRED_EX + ITALIC_VAR + "Enter your selected Theme here: " + Fore.RESET + RESET_VAR).title()

        if THEME in THEMES.keys() and THEME in progress["unlocked_themes"]:
            if THEME == "Default":
                print("Theme set to Default.")
                sel_theme = ""
            elif THEME != "Default" and THEME in progress["unlocked_themes"]:
                sel_theme = THEMES[THEME]
                tprint(f"Theme set to {THEME}.")
            else:
                print('Theme not recognized. Setting theme to default.')

    # Random game (only from GAMES, not easter eggs)
    elif game == 'r':
        name, steps = random.choice(list(GAMES.items()))
        tprint("Note: This won't count towards your progress.")
        tprint(f'\n == {name.upper()} ==\n')
        tprint(steps[0])
        tprint('\nCongratulations!! If you followed the steps, you have OFFICIALLY TUCHED GRASS!!!!!')
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Help menu (list all games)
    elif game == 'h':
        tprint('\n == Games == \n')
        for g in GAME:
            tprint(g)
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Help menu (list all easter eggs)
    elif game == 'eh':
        tprint('\n == Easter Eggs == \n')
        for e in EGG:
            tprint(e)
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Secret menu (list all secret commands)
    elif game == 'secret':
        tprint("\n🌿 SECRET MENU 🌿")
        tprint("These are the hidden commands you have unlocked:\n")

        for cmd, desc in SECRET_COMMANDS.items():
            tprint(f"- {cmd}: {desc}")

        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # Total count (games + easter eggs)
    elif game == 'len':
        tprint('\nThe number of games in this list is: ' + str(len(GAMES) + len(EASTER_EGGS)))
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Easter egg count only
    elif game == 'len_easter':
        tprint('\nThe number of easter eggs in this list is: ' + str(len(EASTER_EGGS)))
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Unlocks all progress
    elif game == 'grassgod':
        tprint("\n🌿 SECRET UNLOCKED 🌿")
        tprint("You have ascended beyond mortal grass touchers.")

        # Unlock everything
        progress["games_found"] = list(GAMES.keys())
        progress["eggs_found"] = list(EASTER_EGGS.keys())

        tprint("All games and easter eggs unlocked!")
        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # The commands powering the grass shop
    elif game == 'shop':
        tprint("\n=== 🌿 GRASS SHOP 🌿 ===")
        tprint(f"You have {progress['coins']} Grass Coins.\n")
        tprint("Available items:")
        tprint("1. Hint (5 coins)")
        tprint("2. Theme (10 coins)")
        tprint("3. Exit shop")

        choice = input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nChoose an option: " + Fore.RESET + RESET_VAR).strip()

        if choice == "1":
            if progress["coins"] >= 5:
                progress["coins"] -= 5
                hint = random.choice(list(GAMES.keys()))
                tprint(f"\n🌱 Your hint: Try searching for '{hint}'.")
            else:
                tprint("\nNot enough coins!")
        elif choice == "2":
            if progress["coins"] >= 10:
                tprint("\nAvailable themes:")
                for t in themeS:
                    tprint("- " + t)
                theme_choice = input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nEnter the theme you want to unlock: " + Fore.RESET + RESET_VAR).title()
                if theme_choice in THEMES and theme_choice not in progress["unlocked_themes"]:
                    progress["coins"] -= 10
                    progress["unlocked_themes"].append(theme_choice)
                    THEMEs.append(theme_choice)
                    themeS.remove(theme_choice)
                    tprint(f"\nTheme '{theme_choice}' unlocked!")
                else:
                    tprint("\nInvalid theme choice or already unlocked.")
            else:
                tprint("\nNot enough coins!")
        elif choice == "3":
            tprint("\nLeaving the shop...")
        else:
            tprint("\nInvalid choice. Leaving the shop...")

        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # Random hint (only from GAMES, not easter eggs, and doesn't count towards your progress')
    elif game == 'seed':
        all_games = list(GAMES.keys())
        hint = random.choice(all_games)
        tprint(f"\nA mysterious seed whispers: Try searching for '{hint}'...")
        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # Game found
    elif game in GAMES:
        tprint(f'\n == {game.upper()} ==\n')
        tprint(GAMES[game][0])

        # If new discovery
        if game not in progress["games_found"]:
            tprint("\nWOW! You found this game for the first time!")
            progress["games_found"].append(game)
            progress["coins"] += 1
            tprint("+1 Grass Coin!")
        tprint('\nCongratulations!! If you followed the steps, you have OFFICIALLY TUCHED GRASS!!!!!')
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Save progress option
    elif game == 's':
        tprint("\nWhich save slot do you want to save to?")
        for n in SAVES:
            tprint(f"- {n}")

        save_to = input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nEnter the save name: " + Fore.RESET + RESET_VAR).replace(" ", "").lower()

        if save_to in SAVES:
            save_slot(save_to, progress)
            tprint(f"\nProgress saved to {save_to}!")
        else:
            tprint("\nInvalid save name. Save cancelled.")

        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # Delete save slot
    elif game == 'delete':
        tprint("\n=== DELETE SAVE SLOT ===")
        tprint("Available saves:")
        for n in SAVES:
            tprint(f"- {n}")

        to_delete = input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nType the name of the save to delete: " + Fore.RESET + RESET_VAR).replace(" ", "").lower()

        if to_delete in SAVES:
            os.remove(f"saves/{to_delete}.dat")
            SAVES.remove(to_delete)
            tprint(f"\nSave '{to_delete}' deleted successfully!")
        else:
            tprint("\nSave not found. Nothing deleted.")

        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # View progress
    elif game == 'p':
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

        input(Fore.LIGHTRED_EX + ITALIC_VAR + "\nPress Enter to continue..." + Fore.RESET + RESET_VAR)
        continue

    # Easter egg found
    elif game in EASTER_EGGS:
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
        input(Fore.LIGHTRED_EX + ITALIC_VAR + '\nPress enter to continue....' + Fore.RESET + RESET_VAR)
        continue

    # Not recognized
    else:
        tprint('\nSorry, game not recognized. Try Again!!!')


# Thank you for viewing the code for HOW TO TUCH GRASS! If you have any suggestions for new games or easter eggs, or any ways you think will improve the game and its code, please let me know.
