import requests
import json
import os
import time


# This a list of all my chess accounts
USERNAMES =["iimo7a", "i-imo7a","l_gnedoy", "m_gnedoy"]

# so we dont get bannded :>
HEADERS ={
"User-Agent": "MyChessBotProject - gathering data for my bot - email: mmalfagih@gmail.com"
}

def get_games_for_all_users():
   
    script_dir = os.path.dirname(os.path.abspath(__file__))
    

    project_root = os.path.dirname(script_dir)
    
    base_folder = os.path.join(project_root, "data", "raw")
    

    os.makedirs(base_folder, exist_ok=True)
    
    for  username in USERNAMES:
        print(f" \n Getting data for {username}  account")

        #create subfolder for the account 
        #we will have each account in folder
        user_folder = os.path.join(base_folder,username)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        #getting each month that have data
        archives_url = f"https://api.chess.com/pub/player/{username}/games/archives"
        res = requests.get(archives_url,headers=HEADERS)

        if res.status_code != 200:
            print(f"Faild to get month lists for account {username}, with error code {res.status_code}")
            continue

        archives = res.json().get("archives", [])
        for month_url in archives:
            # example is "https://api.chess.com/pub/player/iimo7a/games/2021/06"
            # we want to extract 2021 and 06 from each url
            parts = month_url.split("/")
            year, month = parts[-2], parts[-1]
            file_name = os.path.join(user_folder,f"games_{year}_{month}.json")

            if os.path.exists(file_name):
                print(f"file for user {username}, of {year}/{month} already exsists \n skiping this url")
                continue
            print(f"Fetching data for {username}, {year}/{month}")
            month_res = requests.get(month_url,headers=HEADERS)
            #saving data if exists
            if month_res.status_code == 200:
                month_data= month_res.json()
                with open(file_name,"w",encoding='utf-8') as f:
                    json.dump(month_data,f,ensure_ascii=False,indent=4)
            else:
                print(f"faild to get {month_url}, with error code of {month_res.status_code}")
            time.sleep(2)

    print("Done from all accounts")

get_games_for_all_users()
