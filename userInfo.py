import pymongo
import pprint as pp
import random
import requests
import sys
from pymongo import MongoClient



def parse_dotenv():
    file_content = None
    with open(".env", 'rt') as f:
        file_content = f.read()
        file_content = file_content
    print(file_content)
    return file_content
    



db_url = parse_dotenv()
print(db_url)


client = MongoClient(db_url)
print("***CLIENT****", client)
db = client['animexp']




def get_users_account():
    users = db['users']
    user_account_info = {}
    try:
        for user in users.find():
            userID = user["userId"].strip()
            # pp.pprint(user)
            if (user['userEmail'] == "@gmail.com" or user['userEmail'] == None):
                continue
            else:
                # print("HAS BEEN HIT TWO")
                # print("****USER_ID***", userID)
                # url = f"https://animexp-backend.herokuapp.com/user/{userID}/lists"
                url =f'http://localhost:8002/user/{userID}/lists'
                r = requests.get(url)
                if(r.status_code != 200):
                    print("***STATUS***", r.status_code)
                    continue
                response = r.json()
                
                if('firstName' not in response or 'phoneNumber' not in response):
                    continue
            if(response['firstName'] == None):
                continue
            else:
                # print("HAS BEEN HIT 3")
                # pp.pprint(response['firstName'])
                # pp.pprint(response['phoneNumber'])
                #pp.pprint(response['userAnimeList'])
                index = 0
                random_anime = response['userAnimeList'][index]['animeList']
                if(len(random_anime) == 0 and index <= len(response['userAnimeList'])):
                    index += 1
                    random_anime = response['userAnimeList'][index]['animeList']
                    pp.pprint(random_anime)
                else: 
                    continue


                random_index = random.choice(range(len(random_anime)))
                random_anime_2 = response['userAnimeList'][index]['animeList'][random_index][0]
                user_name = response['firstName']
                userID = response['userId']
                user_account_info[user_name] = [userID, response['phoneNumber'],random_anime_2]
                index = 0
        return user_account_info

    except Exception as error:
        print("ERROR GETTING USER:", error)



if __name__ == "__main__":
    result = get_users_account()
    print(result)
   






