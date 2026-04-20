import os
import sys
import cv2
import time
import json
import requests
import numpy as np

from cmd_program.screen_action import (
    tap_screen,
    swipe_screen,
    long_press,
    take_screenshot
)

from core.core import (
    req_ocr,
    req_temp_match,
    tap_on_template,
    req_text
)

from usecases.exploration import(
    claim_exploration_idle_income,
    continue_exploring
)
from usecases.alliance import(
    tech_contribution,
    auto_join,
    collect_chests,
    help
)
from core.recalibrate import recalibrate
from core.change_player import change_account, change_character

from usecases.gather import gather





class Player:
    def __init__(self, name, id, state, email, stamina):
        self.name = name
        self.id = id
        self.state = state
        self.email = email 
        self.stamina = stamina




def init_database():
    global player_data, email_list, player_list
    path = "db/account.json"
    with open(path) as f:
        player_data = json.load(f)
    
    sorted_player_data = sorted(
        player_data.items(),
        key = lambda item: item[1].get("priority", float("inf"))
    )

    player_list = []
    email_list = []

    for email, data in sorted_player_data:
        email_list.append(email)
        for player in data["player"]:
            player_list.append(player["id"])

    player_data = sorted_player_data



def player_initialization():
    recalibrate()
    tap_screen(50, 150)
    time.sleep(2)
    global current_player
    try:
        page_title = req_text("ChiefProfile.Title")[0]
        if page_title.lower() != "Chief Profile".lower():
            print("Failed to load chief profile")
            return None
    except Exception as e:
        print(f"Reading error - {e}, Ending the task")
        return None

    data = req_text(["ChiefProfile.PlayerName", "ChiefProfile.PlayerID", "ChiefProfile.FurnaceLevel", "ChiefProfile.Stamina", "ChiefProfile.State"])
    name, id, furnace, state = (data[0].split(']')[1], data[1].split(':')[1], data[2], data[4].split('#')[1])
    stamina = data[3].split('/')[0]
    
    current_player_id = None
    current_email = None

    for email, info in player_data:
        for player in info["player"]:
            if player.get("id") == id.lower():
                current_player_id = player.get("id")
                current_email = email

    if current_player_id is None or current_email is None:
        print("No player data found for this ID, Exiting this character...")
        return None

    
    current_player = Player(name, id, state, current_email, stamina)
    print(f"    Email: {current_email}\n    Name:{name}\n    ID: {id}\n    Furnace Level: {furnace}\n    Stamina: {stamina}\n    State: {state}")
    
    



init_database()






def run_bot():
    while True:
        player_initialization()

        #----Config----
        current_player_id = current_player.id
        next_player_id = player_list[player_list.index(current_player_id) + 1]
        current_email = current_player.email

        next_email = None
        next_name = None

        for email, info in player_data:
            for player in info["player"]:
                if player.get("id").lower() == next_player_id.lower():
                    next_email = email
                    next_name = player.get("name")

        #----- Task -----
        claim_exploration_idle_income()
        auto_join()
        collect_chests()
        tech_contribution()
        help()
        if current_player_id == "578380047":
            gather(remove_hero=True, equalize=False)
        gather(remove_hero=False, equalize=True)


        #----- Changing Account -----
        current_email_players = None
        for email, info in player_data:
            if email == current_player.email:
                current_email_players = info["player"]
                break
        processed_ids = set()
        processed_ids.add(current_player.id.lower())

        for player in current_email_players:
            if player["id"].lower() not in processed_ids:
                print(f"Switching to sibling character: {player['name']}")

                change_character(player["name"])
                player_initialization()

                processed_ids.add(current_player.id.lower())

                # run tasks again
                claim_exploration_idle_income()
                auto_join()
                collect_chests()
                tech_contribution()
                help()

        if current_player.id == "578380047":
            gather(remove_hero=True, equalize=False)
        gather(remove_hero=False, equalize=True)


        print(f"Progressing to the next email: {next_email}")
        status = change_account(next_email)
        if not status:
            raise RuntimeError("Account changing error")



if __name__=="__main__":
    run_bot()
